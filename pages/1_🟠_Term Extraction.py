# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 17:27:44 2022

@author: Sergio
"""
import streamlit as st
from PIL import Image
from vfunctions import *
import pandas as pd
from pandas import DataFrame
import os.path
import pathlib
import re
import seaborn as sns
import io
import time

st.caption("By **Ser Calvo** :sunglasses: :smile: ")
with st.expander("ℹ️ - About this app", expanded=False):

    st.write(
        """     
-   This app is an easy-to-use interface built in Streamlit that uses [KeyBERT](https://github.com/MaartenGr/KeyBERT) library from Maarten Grootendorst!
-   It uses a minimal keyword extraction technique that leverages multiple NLP embeddings and relies on `Transformers` from Hugging Face 🤗 to extract the most relevant keywords/keyphrases, that is to say, the terms in the text!
-   It also uses `Flair` to help adding a pipeline for the Roberta language model from HuggingFace.
-   And it also integrates `keyphrase-vectorizers` to automatically select the best approach regarding how many n-grams to include.
-   Finally, as a translator would suggest, it also has the option to save the terms in CSV.   
	    """
    )

# A helloworld
st.title(f"	:large_orange_circle: TermXT - Terminology Extraction using NLP :bookmark_tabs:")
st.markdown(f"""
            
            It's simple: extract in seconds an accurate list of keywords from a text. Are they terms too? Well, strictly speaking, not in all cases, but you will definitely get a great bunch of the main phrases according to their relevance within the document.            
            
            """)


# Add a header
st.header("Add your text to extract your terminology candidates")
#st.subheader("Add some text to extract your terminology candidates")
st.write("This app will do the rest, that is to say, tokenize the text, remove stopwords and identify the most relevant candidates terms.")

# get text input from user
input_type = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'])

if input_type == 'Paste text':
    text = st.text_area('Enter text to analyze')
elif input_type == 'Select sample data':
    sample_data = {
        "Text 1 - Simple sentence": "The quick brown fox jumps over the lazy dog.",
        "Text 2 - Philosophy": """Jean-Paul Sartre belongs to the existentialists. For him, ultimately humans are "condemned to be free". There is no divine creator and therefore there is no plan for human beings. But what does this mean for love, which is so entwined with ideas of fate and destiny? Love must come from freedom, it must be blissful and mutual and a merging of freedom. But for Sartre, it isn't: love implies conflict. The problem occurs in the seeking of the lover's approval, one wants to be loved, wants the lover to see them as their best possible self. But in doing so one risks transforming into an object under the gaze of the lover, removing subjectivity and the ability to choose, becoming a "loved one". """,
        "Text 3 - Wind energy": "Wind is used to produce electricity by converting the kinetic energy of air in motion into electricity. In modern wind turbines, wind rotates the rotor blades, which convert kinetic energy into rotational energy. This rotational energy is transferred by a shaft which to the generator, thereby producing electrical energy. Wind power has grown rapidly since 2000, driven by R&D, supportive policies and falling costs. Global installed wind generation capacity – both onshore and offshore – has increased by a factor of 98 in the past two decades, jumping from 7.5 GW in 1997 to some 733 GW by 2018 according to IRENA’s data. Onshore wind capacity grew from 178 GW in 2010 to 699 GW in 2020, while offshore wind has grown proportionately more, but from a lower base, from 3.1 GW in 2010 to 34.4 GW in 2020. Production of wind power increased by a factor of 5.2 between 2009 and 2019 to reach 1412 TWh."
    }
    selected_sample = st.selectbox('Select sample data', list(sample_data.keys()))
    text = sample_data[selected_sample]
else:
    uploaded_file = st.file_uploader('Upload file', type=['txt'])
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    else:
        text = ''
        

num_words = count_words(text)

if text:
    st.subheader('Text to analyze')
    #st.write(text)
    st.markdown(f":orange[{text}]")

    # display term extraction
    st.header("Extract the candidate terms and keywords")  
    df = None
    with st.form('extract'):
        
      
        #preview = st.text_area("**Text Preview**", "", height=150, key="preview")
        st.write(f"""#### The text contains `{num_words}` words. Do you wonder how many terms? 
                 \nLet's try to find some terms and keywords. Magic is one click away... Go for it! :dart: !""")
        
        c1, c2 = st.columns(2)
        with c1:
            hits = st.number_input(label='Select the maximum number of terms', min_value=10)
        with c2:
            st.write("")
        
        
        submit_extract = st.form_submit_button('Extract terms')
    
        
        if submit_extract:
            
            #if text:
             #   placeholder = st.empty()
              #  placeholder.success(" Just a few miliseconds...", icon="⏳")
               # time.sleep(1)
                #placeholder.empty()
            
           # with st.container():
              
                
            #hits = 10
            keywords = verikeybert(text, hits)
            st.subheader("Terminology extraction results\n")    
            
            st.write("##### Please see a list of ", len(keywords)," candidate terms and keywords.")
            
            df = (
            DataFrame(keywords, columns=["Keyword/Keyphrase", "Relevancy"])
            .sort_values(by="Relevancy", ascending=False)
            .reset_index(drop=True)
            )
            
            df.index += 1
            
            # Add styling
            cmGreen = sns.light_palette("green", as_cmap=True)
            cmRed = sns.light_palette("red", as_cmap=True)
            df = df.style.background_gradient(
                cmap=cmGreen,
                subset=[
                    "Relevancy",
                ],
            )
            
            c1, c2, c3 = st.columns([1, 3, 1])
            
            format_dictionary = {
                "Relevancy": "{:.1%}",
            }
            
            df = df.format(format_dictionary)
            
            st.table(df)
            st.balloons()
            
    
            
    if df is not None:
        st.header("3. Save the keywords!")
        df = (
        DataFrame(keywords, columns=["Keyword/Keyphrase", "Relevancy"])
        .sort_values(by="Relevancy", ascending=False)
        .reset_index(drop=True)
        )
        
        
        
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df)
    
    
        st.download_button(
                label="Download data as CSV",
            data=csv,
            file_name='Extracted_keywords.csv',
            mime='text/csv',
        )
    
        st.markdown("**Thanks for using this tool!**")                            
            
                    
        
        
    
        
        
                
    
        
        
        
        
        