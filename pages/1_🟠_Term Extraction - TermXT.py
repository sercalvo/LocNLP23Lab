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
import os
from os import path
import random
import re

# Define the global DataFrame variable
df = None

def get_random_context(keyword, text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    keyword_sentences = [sentence for sentence in sentences if keyword.lower() in sentence.lower()]
    
    if len(keyword_sentences) >= 2:
        first_sentence = random.choice(keyword_sentences)
        remaining_sentences = [sentence for sentence in keyword_sentences if sentence != first_sentence]
        second_sentence = random.choice(remaining_sentences) if remaining_sentences else "No other sentence"
    elif len(keyword_sentences) == 1:
        first_sentence = keyword_sentences[0]
        second_sentence = "No other sentences found"
    else:
        first_sentence = "No other sentences found"
        second_sentence = "No other sentences found"
    
    return first_sentence, second_sentence






def show_term_extraction_results(text, hits):
    global df  # Use the global DataFrame variable
    
    keywords = verikeybert(text, hits)
    st.subheader("Terminology extraction results\n")    
    
    st.write("##### Please see a list of ", len(keywords)," candidate terms and keywords.")
    
    df = (
        DataFrame(keywords, columns=["Keyword/Keyphrase", "Relevancy"])
        .sort_values(by="Relevancy", ascending=False)
        .reset_index(drop=True)
    )
    
    if add_POS:
        df.insert(1, "POS", df["Keyword/Keyphrase"].apply(lambda x: " ".join(get_pos(word) for word in x.split())))

    if add_lemma:
        #df.insert(2, "lemma", df['Keyword/Keyphrase'].apply(get_lemma))
        df.insert(2, "Lemma", df["Keyword/Keyphrase"].apply(lambda x: " ".join(get_lemma(word) for word in x.split())))
    if add_definition:
        # Add columns for WordNet and Merriam-Webster definitions
        df.insert(3, "WordNet Definition", df["Keyword/Keyphrase"].apply(get_wordnet_definition) )
        df.insert(4, "Merriam-Webster Definition", df["Keyword/Keyphrase"].apply(get_merriam_webster_definition) )
    if add_context:
        df.insert(3, "Context Sentence 2", df["Keyword/Keyphrase"].apply(lambda x: get_random_context(x, text)[1]))
        df.insert(3, "Context Sentence 1", df["Keyword/Keyphrase"].apply(lambda x: get_random_context(x, text)[0]))
        
    # Adjust the index to start at 1
    df.index += 1


        
    
    
    # Add styling
    cmGreen = sns.light_palette("green", as_cmap=True)
    styled_df = df.style.background_gradient(
        cmap=cmGreen,
        subset=[
            "Relevancy",
        ],
    )
    
    c1, c2, c3 = st.columns([1, 3, 1])
    
    format_dictionary = {
        "Relevancy": "{:.1%}",
    }
    
    styled_df = styled_df.format(format_dictionary)
    
    st.table(styled_df)
    st.balloons()
    
    if df is not None:
        st.header("Save the terms")
        
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
    
        return styled_df, df
    
def get_term_definitions():
    global df  # Use the global DataFrame variable
    
    st.header("Generate definitions")
    selected_terms = st.multiselect(
        "Select terms to generate definitions for",
        df["Keyword/Keyphrase"].tolist(),
        default=st.session_state.get("selected_terms", [])
    )
    st.session_state["selected_terms"] = selected_terms
    
    if selected_terms:
        definitions = get_term_definitions(selected_terms)
        if definitions:
            st.table(definitions)
        else:
            st.write("No definitions found for the selected terms.")


st.set_page_config(
    page_title="LocNLP23Lab - Term Extraction",
    page_icon="img//V-Logo-icon48.png",
)

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
st.header("Add your text to extract term candidates")
#st.subheader("Add some text to extract your terminology candidates")
st.write("This app will do the rest, that is to say, tokenize the text, remove stopwords and identify the most relevant candidates terms.")

# get text input from user
input_type = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'], help="Only clean text format (.txt file)")

if input_type == 'Paste text':
    text = st.text_area('Enter text to analyze')
elif input_type == 'Select sample data':
    sample_data = {
        "Sample text 1 - Audio interfaces": "An interface allows one thing to interact with another. One of our most common uses of the word is in computing; a human requires a “user interface” to interact with a computer. Likewise, an “audio interface” is a device capable of passing multiple channels of audio to and from a computer in real time. That definition is intentionally broad – many units also contain microphone preamplifiers, basic mixing capabilities, onboard processing, and other features. Smaller interfaces typically carry four channels or less, and are often “bus-powered,” meaning that the USB (or similar) cable from the computer supplies both data and power connectivity. Most larger interfaces carry at least eight channels and require their own power supply.",
        "Sample text 2 - Philosophy": """Jean-Paul Sartre belongs to the existentialists. For him, ultimately humans are "condemned to be free". There is no divine creator and therefore there is no plan for human beings. But what does this mean for love, which is so entwined with ideas of fate and destiny? Love must come from freedom, it must be blissful and mutual and a merging of freedom. But for Sartre, it isn't: love implies conflict. The problem occurs in the seeking of the lover's approval, one wants to be loved, wants the lover to see them as their best possible self. But in doing so one risks transforming into an object under the gaze of the lover, removing subjectivity and the ability to choose, becoming a "loved one". """,
        "Sample text 3 - Wind energy": "Wind is used to produce electricity by converting the kinetic energy of air in motion into electricity. In modern wind turbines, wind rotates the rotor blades, which convert kinetic energy into rotational energy. This rotational energy is transferred by a shaft which to the generator, thereby producing electrical energy. Wind power has grown rapidly since 2000, driven by R&D, supportive policies and falling costs. Global installed wind generation capacity – both onshore and offshore – has increased by a factor of 98 in the past two decades, jumping from 7.5 GW in 1997 to some 733 GW by 2018 according to IRENA’s data. Onshore wind capacity grew from 178 GW in 2010 to 699 GW in 2020, while offshore wind has grown proportionately more, but from a lower base, from 3.1 GW in 2010 to 34.4 GW in 2020. Production of wind power increased by a factor of 5.2 between 2009 and 2019 to reach 1412 TWh.",
        "Sample text 4 - Electronics": "In electronics and telecommunications, modulation is the process of varying one or more properties of a periodic waveform, called the carrier signal, with a separate signal called the modulation signal that typically contains information to be transmitted.[citation needed] For example, the modulation signal might be an audio signal representing sound from a microphone, a video signal representing moving images from a video camera, or a digital signal representing a sequence of binary digits, a bitstream from a computer."
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
    st.caption("Showing only first 1000 words in the text")
    words = text.split()[:1000]
    limited_text = ' '.join(words)
    st.markdown(f'<div style="height: 300px; overflow-y: scroll;">{limited_text}</div>', unsafe_allow_html=True)

    # display term extraction
    st.header("Extract the candidate terms")  

    with st.form('extract'):
        
      
        #preview = st.text_area("**Text Preview**", "", height=150, key="preview")
        st.write(f"""#### The text contains `{num_words}` words. Do you wonder how many terms? 
                 \nLet's try to find some terms and keywords. Magic is one click away... Go for it! :dart: !""")
        
        c1, c2 = st.columns(2)
        with c1:
            hits = st.number_input(label='Select the maximum number of terms', min_value=10)
            submit_extract = st.form_submit_button('Extract terms')
        with c2:
            st.caption("**Add metadata fields**")
            # Use st.checkbox() to create checkboxes for enabling stop word removal and lemmatization
            add_POS = st.checkbox(":green[Add POS tags]", help="It will add the Part Of Speech to each term.")
            add_lemma = st.checkbox(":green[Add lemma]", help="It will add the lemma or cannonical form of the word.")
            add_definition = st.checkbox(":green[Add definition]", help="It will add Merriam-Webster and WordNet definitions to each term.")
            add_context = st.checkbox(":green[Add context sentences]", help="It will add random context sentences to each term.")

        
        
    
    
    if submit_extract:
        styled_df, df = show_term_extraction_results(text, hits)
        st.session_state['df'] = df

    
        
            
                              
            
                    
        
        
    
        
        
                
    
        
        
        
        
        