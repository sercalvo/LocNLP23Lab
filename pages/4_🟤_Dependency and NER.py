# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 00:32:37 2022

@author: Sergio
"""

import streamlit as st  
import spacy
from spacy import displacy

import spacy
from spacy import displacy

import os
from os import path

st.set_page_config(
    page_title="LocNLP23Lab - Dependency & NER",
    page_icon="img//V-Logo-icon48.png",
)


st.title(":large_brown_circle: Dependency & Entity Analyzer :curly_loop: ")
st.markdown("Perform real-time analysis of a text to extract features and see a magical visualization of syntactical dependencies and named entities.")
# Load the English model in Spacy
#nlp = spacy.load("en_core_web_sm")

# Load the Spanish and English models
nlp_en = spacy.load("en_core_web_md")
nlp_es = spacy.load("es_core_news_sm")

# Add a header for the first section: Select text
st.header("Add your text to analyze")


# Use the st.radio function to create a radio button for the user to choose between Spanish and English
language = st.radio("Choose a language:", ("English", "Spanish"))

# Use an if statement to select the appropriate language model based on the user's selection
if language == "English":
    nlp = nlp_en
    sample_data = {
        "Sample text 1 - Chuch Norris": "Chuck Norris doesn't churn butter. He roundhouse kicks the cows and the butter comes straight out. When the Boogeyman goes to sleep every night, he checks his closet for Chuck Norris CNN was originally created as the 'Chuck Norris Network' to update Americans with on-the-spot ass kicking in real-time.",
        "Sample text 2 - Google": "Google announced a host of new artificial intelligence features coming to its products and services at the company’s annual I/O developer conference yesterday (May 10), where CEO Sundar Pichai mentioned the term “A.I.” 27 times during his 15-minute keynote, per Observer’s count. (Other executives mentioned “A.I.” about 100 additional times over the two-hour event.)"
    }
else:
    nlp = nlp_es
    sample_data = {
        "Sample text 1 - Chuck Norris": "Chuck Norris no cree que haya 50 estados en Estados Unidos. Sólo hay uno: Estado de emergencia. Allá por donde pasa es una emergencia. Chuck Norris hace el desayuno de los campeones. Literalmente. Se comió a Fernando Alonso, Tiger Woods y a Roger Federer en una sola comida.",
        "Sample text 2 - Google": "La inteligencia artificial es la gran apuesta de las principales compañías tecnológicas, y Google acaba de dejar claro que está dispuesta a sacarle el mayor provecho. En su conferencia anual Google I/O en Mountain View, California, el CEO de la Alphabet, Sundar Pichai, habló del objetivo de la compañía para hacer la inteligencia artificial «útil para todos», presentando varios ejemplos de cómo esta tecnología mejorará varios de sus productos."
    }


# get text input from user
input_type = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'], help="Only clean text format (.txt file)")

if input_type == 'Paste text':
    text = st.text_area('Enter text to analyze')
elif input_type == 'Select sample data':
    
    selected_sample = st.selectbox('Select sample data', list(sample_data.keys()))
    text = sample_data[selected_sample]
else:
    uploaded_file = st.file_uploader('Upload file', type=['txt'])
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    else:
        text = ''


doc = nlp(text)


if text:
    st.subheader('Text to analyze')
    st.caption("Showing only first 1000 words in the text")
    words = text.split()[:1000]
    limited_text = ' '.join(words)
    st.markdown(f'<div style="height: 300px; overflow-y: scroll;">{limited_text}</div>', unsafe_allow_html=True)
    
    # Add a section header:
    st.header("Named Entity Recognition visualizer")
    # Take the text from the input field and render the entity html.
    # Note that style="ent" indicates entities.
    ent_html = displacy.render(doc, style="ent", jupyter=False)
    # Display the entity visualization in the browser:
    st.markdown(ent_html, unsafe_allow_html=True)
    
    st.write(" ")
    # Display a section header:
    st.header("Dependency parse visualizer")
    # Use spacy's render() function to generate SVG.
    # style="dep" indicates dependencies should be generated.
    dep_svg = displacy.render(doc, style="dep", jupyter=False)
    st.image(dep_svg, width=400, use_column_width="never")


