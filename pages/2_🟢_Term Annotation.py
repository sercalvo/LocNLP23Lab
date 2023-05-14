# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 00:58:36 2022

@author: Sergio
"""

# Import the necessary libraries
import streamlit as st
import re
import spacy
from spacy import displacy
from spacy.tokens import Span
import pandas as pd
from pandas import DataFrame
import time
from vfunctions import verikeybert

import os
from os import path

st.set_page_config(
    page_title="LocNLP23Lab - Term Annotation",
    page_icon="img//V-Logo-icon48.png",
)

def annotate_keyphrases(text, phrases):
    # Load the English language model from spaCy
    nlp = spacy.load("en_core_web_sm")

    # Create a spaCy doc object from the text
    doc = nlp(text)

    # Initialize a list to store the positions and part-of-speech tags of the phrases
    phrase_list = []

    # Use the re.finditer method to find the phrases in the text
    for match in re.finditer(r"\b(" + "|".join(phrases) + r")\b", text):
        # Get the matched phrase
        phrase = match.group()
        # Get the start and end positions of the phrase in the text
        start_pos = match.start()
        end_pos = match.end()
        # Initialize the spans
        spans = []
        # Use the doc.char_span method to get the tokens in the span of the matched phrase
        def find_spans(doc, phrases):
            for phrase in phrases:
                start = doc.text.find(phrase)
                end = start + len(phrase)
                span = doc.char_span(start, end)
                if span is not None:
                    # Add the phrase, its start and end positions, and its part-of-speech tag to the phrase list spans
                    spans.append(Span(doc, span.start, span.end, "TERM"))
            return spans

        # Compile the spans for displacy span visualization
        doc.spans["sc"] = find_spans(doc, phrases)

    # Get the text of the document
    final_text = doc.text

    # Replace the matched phrases with their annotated versions
    for phrase in phrases:
        #final_text = final_text.replace(phrase, "<atg>{}</tag>".format(phrase))
        final_text = final_text.replace(phrase, f"`<term>`**{phrase}**`</term>`")

    # Print to screen the annotated texts
    st.subheader("Term mark-up using Displacy spans")
    st.success("This visualization uses Spacy and the visualizer Displacy to mark up the terms given the list.")
    options = {"ents": ["TERM"], "colors": {"TERM": "#fabc02"}}
    ent_html = displacy.render(doc, style="span", options=options, jupyter=False)
    # Display the entity visualization in the browser:
    st.markdown(ent_html, unsafe_allow_html=True)

    st.write("## Tagged text")
    st.success("This visualization provides a markup with tags `<term>`text`</term>` using Python.")
    st.caption('This is a string that explains something above.')
    # Print the final text and the phrase list
    st.markdown(final_text)

@st.cache_data
def load_term(chorradas):
    st.write("Extract keywords")
    prueba = verikeybert(chorradas, 10)
    df = DataFrame(prueba, columns=["Keyword", "Relevancy"])
    st.dataframe(df)
    terms = [x for x in df['Keyword']]
    st.write(prueba)
    return terms

@st.cache_data
def extract_10_terms(text):
    prueba = verikeybert(text, 10)
    df = DataFrame(prueba, columns=["Keyword", "Relevancy"])
    terms = [x for x in df['Keyword']]
    return terms

# Store the initial value of widgets in session state
if "checkbox" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state["disabled"] = False

# Add a page title for the app
st.title(':large_green_circle: Term Annotation :male-detective:')
st.markdown('This app makes use of `Spacy` library to provide nice visualizations of terms and keywords.')

# Add a header for the first section: Select text
st.header("Add your text and terms to annotate")

# Define session_state function to later hide the checkbox if pasted text is passed in or clear the fields
def clear_form():
    st.session_state["my_input_area"] = ""
    st.session_state["my_input_kw_area"] = ""
    st.session_state["disabled"] = False
    st.session_state["checkbox"] = False

# get text input from user
input_type = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'])
if input_type == 'Paste text':
    text = st.text_area('Enter text to analyze')
elif input_type == 'Select sample data':
    sample_data = {
        "Sample text 1": "The quick brown fox jumps over the lazy dog.",
        "Sample text 2": "Chuck Norris doesn't churn butter. He roundhouse kicks the cows and the butter comes straight out. When the Boogeyman goes to sleep every night, he checks his closet for Chuck Norris CNN was originally created as the 'Chuck Norris Network' to update Americans with on-the-spot ass kicking in real-time.",
        "Sample text 3": "Wind is used to produce electricity by converting the kinetic energy of air in motion into electricity. In modern wind turbines, wind rotates the rotor blades, which convert kinetic energy into rotational energy. This rotational energy is transferred by a shaft which to the generator, thereby producing electrical energy."
    }
    selected_sample = st.selectbox('Select sample data', list(sample_data.keys()))
    text = sample_data[selected_sample]
else:
    uploaded_file = st.file_uploader('Upload file', type=['txt'])
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    else:
        text = ''

if text:
    st.subheader('Text to analyze')
    st.markdown(f":green[{text}]")

# display the annotated text
terms = []

# Add a form for the user to paste a text
with st.form(key='my_annotation'):
    # Section header for terms the annotated text
    st.subheader('Add your terms to annotate')
    input_phrases = "".join(st.text_input('Add your own keywords, phrases or terms separated by comma', 'sample term', key="my_input_kw_area", help="Use comma without space to separate the terms like: electrical energy,kinetic energy,modern wind turbines,rotational energy,wind,rotor blades,motion,generator")).split(sep=",")

    # Create two columns for two buttons
    f1, f2 = st.columns(2)
    with f1:
        # Button to send text and phrases to print on screen
        gettext_button = st.form_submit_button(label='Annotate terms in the text')

    with f2:
        agree = st.checkbox(':orange[Extract terms automatically]', help="Automatic terminology extraction will extract the best 10 candidates using several algorithms to identify the most relevant collocations or single words.")

        if agree:
            st.write('Great!')
            terms = extract_10_terms(text)

def ui_message(message):
    placeholder = st.empty()
    placeholder.success(f'{message}')
    time.sleep(1)
    placeholder.empty()
    return

def ui_warning(message):
    placeholder = st.empty()
    placeholder.warning(f'{message}')
    time.sleep(1)
    placeholder.empty()
    return

if gettext_button:
    if agree == False and input_phrases == "":
        ui_warning("Hey, no term! Mark at least the automatic extraction :smile:")
    elif text == "":
        ui_warning("No text, my friend!")
    else:
        st.subheader("Preview text and terms ")
        st.write('**The text to be processed :point_down:**')
        c5, c6 = st.columns([1, 3])
        with c5:
            st.write(pd.DataFrame({'Keyphrases': input_phrases + terms })) 
        with c6:
            st.markdown(f":green[{text}]")
        
        final_phrases = input_phrases + terms
            
        st.header("Visualize and annotate the text")
        annotate_keyphrases(text, final_phrases)


