# -*- coding: utf-8 -*-
"""
Created on Sun May 14 06:09:37 2023

@author: Sergio
"""

import streamlit as st
import pandas as pd
from vfunctions import *
from pandas import DataFrame
import streamlit as st
import pandas as pd
import wikipediaapi
from pandas import DataFrame
from translate import Translator

# Instantiate Wikipedia API client
wiki_api = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)','en')

def create_df(terms):
    # Perform term extraction using your preferred method
    # Replace this with your actual term extraction code
    keywords = list(term for term in terms)  # Dummy list of extracted terms
    
    # Combine terms into a DataFrame
    df = pd.DataFrame({"Term": keywords})
    
    # Sort DataFrame by term in ascending order
    df = df.sort_values(by="Term", ascending=True).reset_index(drop=True)
    
    # Adjust the index to start at 1
    df.index += 1
    
    return df

def retrieve_definitions(terms, target_language="en"):
    # Retrieve definitions for the selected terms
    # Replace this with your actual definition retrieval code
    definitions = pd.DataFrame(terms, columns=["Term"]).sort_values(by="Term", ascending=False).reset_index(drop=True)
    
    # Add additional columns based on user preferences
    if add_POS:
        definitions["POS"] = definitions["Term"].apply(lambda x: " ".join(get_pos(word) for word in x.split()))
    
    if add_lemma:
        definitions["Lemma"] = definitions["Term"].apply(lambda x: " ".join(get_lemma(word) for word in x.split()))

    if add_translation:
        definitions["Translation"] = definitions["Term"].apply(lambda x: translate_term(x, target_language))
    
    if add_Wikipedia_context:
        #definitions["Context Sentence 1"] = definitions["Term"].apply(lambda x: get_random_context(x, text)[0])
        #definitions["Context Sentence 2"] = definitions["Term"].apply(lambda x: get_random_context(x, text)[1])
        
        # Retrieve context sentences from Wikipedia
        definitions["Wikipedia Context"] = definitions["Term"].apply(get_wikipedia_context)
    
    if add_WordNet_definition:
        definitions["WordNet Definition"] = definitions["Term"].apply(get_wordnet_definition)
    if add_Merriam_definition:
        definitions["Merriam-Webster Definition"] = definitions["Term"].apply(get_merriam_webster_definition)
    if add_Wiktionary_definition:
        definitions["Wiktionary Definition"] = definitions["Term"].apply(get_wiktionary_definition)
    ##if add_Google_definition:
     ##   definitions["Google Definition"] = definitions["Term"].apply(get_google_definition)
    ##if add_Oxford_definition:
      ##  definitions["Oxford Definition"] = definitions["Term"].apply(get_oxford_definition)
    
    # Adjust the index to start at 1
    definitions.index += 1
    
    return definitions

def get_oxford_definition(term):
    # Retrieve definition from Oxford Dictionary
    # Replace with your code to fetch definition from Oxford Dictionary API
    return "Definition of " + term + " from Oxford Dictionary"

from bs4 import BeautifulSoup

import re

def get_wiktionary_definition(term):
    # Retrieve definition from Wiktionary
    # Replace with your code to fetch definition from Wiktionary API
    url = f"https://en.wiktionary.org/wiki/{term}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the definition section on the page
        definition_section = soup.find('div', {'class': 'mw-parser-output'})
        
        if definition_section:
            # Extract the first paragraph within the definition section
            first_paragraph = definition_section.find('p')
            
            if first_paragraph:
                # Clean the text by removing HTML tags and extra whitespaces
                cleaned_definition = ' '.join(first_paragraph.stripped_strings)
                cleaned_definition = re.sub(r'\s+([.,!?])', r'\1', cleaned_definition)
                return cleaned_definition.strip()
    
    return "Definition of '" + term + "' not found in Wiktionary"



def get_wikipedia_context(term):
    # Retrieve context sentence from Wikipedia
    page = wiki_api.page(term)
    
    if page.exists():
        return page.summary[0:350]  # Extract the first 200 characters from the Wikipedia summary
    
    return ""

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


import requests
from bs4 import BeautifulSoup

def get_google_definition(term):
    # Retrieve definition from Google search using "define:" operator
    query = f"define:{term}"
    url = f"https://www.google.com/search?q={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div containing the definition
        definition_div = soup.find('div', {'class': 'BNeawe iBp4i AP7Wnd'})
        
        if definition_div:
            definition = definition_div.get_text(separator=' ')
            return definition.strip()
    
    return "Definition of " + term + " from Google"

def translate_term(term, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(term)
    return translation


# Streamlit app code
st.title(":large_orange_circle: Metadata generation for term harvesting 	:face_with_monocle:")
st.write("This app aims at providing contextual information for term harvesting. It retrieves a range of details for the terms, such as grammatical information, context sentences and several definitions from diferent sources.")

# Terms input for metadata populating
st.subheader('Add your terms for metadata generation')
input_terms= "".join(st.text_area('Add your own keywords, phrases or terms separated by comma', 'terminology, term', key="my_input_kw_area", help="Use comma without space to separate the terms like: electrical energy,kinetic energy,modern wind turbines,rotational energy,wind,rotor blades,motion,generator")).split(sep=",")

# Term extraction settings
#hits = st.number_input("Maximum number of terms", min_value=1, value=5)

# Perform term extraction
if st.button("Load terms for analysis"):
    if input_terms:
        with st.expander("See table with terms"):
            df_terms = create_df(input_terms)
            st.write("Terms provided:")
            st.table(df_terms)
            #st.success("Term extraction completed")
        
        # Store df_terms in session state
        st.session_state.df_terms = df_terms
    else:
        st.warning("Please enter text to extract terms")
        
    

# Select terms for definition retrieval
if "df_terms" in st.session_state:
    
    st.subheader("**Add metadata fields**")
    target_language_code = "en"
    c1, c2 = st.columns(2)
    with c1:
        # Use st.checkbox() to create checkboxes for enabling stop word removal and lemmatization
        add_POS = st.checkbox(":green[Add POS tags]", help="It will add the Part Of Speech to each term.")
        add_lemma = st.checkbox(":green[Add lemma]", help="It will add the lemma or cannonical form of the word.")
        
        add_translation = st.checkbox(":green[Add Translation]", help="It will add the translation of each term to the selected language.")
        if add_translation:
            target_language = st.selectbox("Select Target Language", ["English", "French", "Spanish", "German"])
            target_language_code = "en"  # Default to English
        
            # Map target language to language code
            language_mapping = {
                "English": "en",
                "French": "fr",
                "Spanish": "es",
                "German": "de"
            }

            target_language_code = language_mapping.get(target_language, target_language_code)

        
        
    with c2:
        add_Wikipedia_context = st.checkbox(":green[Add Wikipedia context sentence]", help="It will add Wikipedia context sentences to each term.")
        add_WordNet_definition = st.checkbox(":green[Add WordNet definition]", help="It will add a WordNet definition to each term.")
        add_Merriam_definition = st.checkbox(":green[Add Merriam-Webster Definition]", help="It will add a Merriam-Webster definition to each term.")
        add_Wiktionary_definition = st.checkbox(":green[Add Wiktionary definition]", help="It will add a Wiktionary definition to each term.")
        #add_Google_definition = st.checkbox(":green[Add Google 'define:']", help="It will add random context sentences to each term.")

    selected_terms = st.multiselect("Select terms for metadata generation", st.session_state.df_terms["Term"].tolist())

    # Retrieve definitions for selected terms
    if selected_terms:
        #df_definitions = retrieve_definitions(selected_terms)
        df_definitions = retrieve_definitions(selected_terms, target_language_code)

        st.write("Term Definitions:")
        st.table(df_definitions)
