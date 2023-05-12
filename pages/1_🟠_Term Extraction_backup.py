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


st.header("1. Pick up your text")



#with st.form('upload'):
file = st.file_uploader("Choose a file", label_visibility="collapsed")
            
    #submitted = st.form_submit_button('Enviar')

num_words = 0

if file is not None:
        
    #bytes_data = file.getvalue()
    data = file.getvalue().decode('utf-8').splitlines(False)         
    st.session_state["preview"] = ''
    for i in range(0, min(5, len(data))):
        st.session_state["preview"] += data[i]
    
    
    stringio = io.StringIO(file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    clean_text = " ".join(string_data.split()) 
    
    # Define the regex pattern for splitting the text into words
    pattern = re.compile(r'\w+')        
    # Use the findall() method to split the text into a list of words
    words = pattern.findall(clean_text)
    # Use the len() function to get the number of words in the list
    num_words = len(words)  

    if file:
        placeholder = st.empty()
        placeholder.success(f" Uploading the file \"{file.name}\" for term extraction.", icon="✅")
        time.sleep(2)
        placeholder.empty()

    st.header("2. Extract the candidate terms and keywords")  
    df = None
    with st.form('extract'):
      
        preview = st.text_area("**Text Preview**", "", height=150, key="preview")
        st.write(f"""#### The text contains `{num_words}` words. Do you wonder how many terms? 
                 \nLet's try to find some terms and keywords. Magic is one click away... Go for it! :dart: !""")
        
        c1, c2 = st.columns(2)
        with c1:
            hits = st.number_input(label='Select the maximum number of terms', min_value=10)
        with c2:
            st.write("")
            #st.write("Magic is one click away... Go for it! :dart: !")
            #hits = st.slider(label='Select the maximum number of terms', min_value=0, max_value=100, key=4)
            ##st.write(f"There will be `{hits}` term candidates on screen in a few seconds.")
            
        # To convert to a string based IO:
        stringio = io.StringIO(file.getvalue().decode("utf-8"))
        #st.write(stringio)
    
        # To read file as string:
        string_data = stringio.read()
        clean_text = " ".join(string_data.split()) 
        
        file_extract = st.form_submit_button('Extract keywords')
    
        
        if file_extract:
            
            if file:
                placeholder = st.empty()
                placeholder.success(" Just a few miliseconds...", icon="⏳")
                time.sleep(1)
                placeholder.empty()
            
           # with st.container():
              
                
            #hits = 10
            keywords = verikeybert(clean_text, hits)
            st.subheader("Keyword extraction results\n")    
            
            st.write("##### Please see the top ", len(keywords)," keywords.")
            
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
            
                    
        
        
    
        
        
                
    
        
        
        
        
        