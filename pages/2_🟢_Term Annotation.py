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

    # Printo to screen the annotated texts
    st.subheader("Term mark-up using Displacy spans")
    st.success("This visualization uses Spacy and the visualizer Displacy to mark up the terms given the list.")
    options = {"ents": ["TERM"],
               "colors": {"TERM": "#fabc02"}}

    ent_html = displacy.render(
        doc, style="span",  options=options, jupyter=False)
    # Display the entity visualization in the browser:
    st.markdown(ent_html, unsafe_allow_html=True)

    st.write("## Tagged text")
    st.write("This visualization provides a mark up with tags `<term>`text`</term>` using Python.")
    st.caption('This is a string that explains something above.')
    # Print the final text and the phrase list
    st.markdown(final_text)
    # print(phrase_list)

    return


@st.cache_data
def load_term(chorradas):
    
    ###########################################################################
    st.write("Extract keywords")
    
    prueba = verikeybert(chorradas, 10)
    df = (
    DataFrame(prueba, columns=["Keyword", "Relevancy"]))
    st.dataframe(df)
    terms = [x for x in df['Keyword']]
    #st.write("This are the terms: ", str(terms))
    st.write(prueba)
    ##################################################################
    terms
    return terms

@st.cache_data
def extract_10_terms(texto):
        
    prueba = verikeybert(texto, 10)
    df = (
    DataFrame(prueba, columns=["Keyword", "Relevancy"]))
    #st.dataframe(df)
    terms = [x for x in df['Keyword']]
    #st.write("This are the terms: ", str(terms))
    #st.write(prueba)
    ##################################################################
    #terms
    return terms
    
    
    
    
    
# Store the initial value of widgets in session state
if "checkbox" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state["disabled"] = False
    #st.session_state["checkbox"] = False

# Initialization
# if 'key' not in st.session_state:
 #   check_state = st.session_state['check'] = False
  #  st.write(check_state)


# Add a page title for the app
st.title(':large_green_circle: Term Annotation :male-detective:')
st.markdown(
    'This app makes use of `Spacy` library to provide nice visualizations of terms and keywords.')

# Add a header for the first section: Select text
st.header("Add your text and terms to annotate")

# Define session_state function to later hide the checkbox if pasted text is passed in or clear the fields


def clear_form():
    st.session_state["my_input_area"] = ""
    st.session_state["my_input_kw_area"] = ""
    st.session_state["disabled"] = False
    st.session_state["checkbox"] = False

terms = []
# Add a form for the user to paste a text
with st.form(key='my_annotation'):
    input_text = st.text_area(
        "Copy and paste your text to annotate", "Wind is used to produce electricity by converting the kinetic energy of air in motion into electricity. In modern wind turbines, wind rotates the rotor blades, which convert kinetic energy into rotational energy. This rotational energy is transferred by a shaft which to the generator, thereby producing electrical energy.", height=150, key="my_input_area", max_chars=501)
    input_phrases = "".join(st.text_input('Add your own keywords, phrases or terms separated by comma', 'sample term',
                                  key="my_input_kw_area", help="Use comma without space to separate the terms like: electrical energy,kinetic energy,modern wind turbines,rotational energy,wind,rotor blades,motion,generator")).split(sep=",")
    #input_phrases = input_phrases.split()
    agree = st.checkbox('Extract terms automatically', help="Automatic terminology extraction will extract the best 10 candidates using several algorithms to identify the most relevant collocations or single words.")    
    # Create two columns for two buttons
    f1, f2 = st.columns(2)
    with f1:     
        # Button to send text and phrases to print on screen
        gettext_button = st.form_submit_button(
            label='Send text and phrases for annotation', )
        # Button to clear the form using the function with session state
        #run_keybert = st.form_submit_button(label="Extract terms automatically", on_click=extract_10_terms(input_text))
        
        
        if agree:
            st.write('Great!')
            terms = extract_10_terms(input_text)
        # Send a message out of the form when the Clear fields button is pressed
        
    with f2:
        # Button to clear the form using the function with session state
        clear = st.form_submit_button(label="Clear form", on_click=clear_form)
        # Send a message out of the form when the Clear fields button is pressed


# Add the option to use sample data to test the app
sample_text_checkbox = st.checkbox("Load sample text", False, help="Use demo example text",
                    disabled=st.session_state.disabled, key="checkbox")



#testing automatic extraction
#chorradas = st.text_input("Paste your text and press Enter to automatically extract the terms", "", max_chars=501)
#terms = load_term(chorradas)

#st.subheader("Add your terms")
#input_phrases = "".join(st.text_input('Add your own keywords, phrases or terms separated by comma', 'electrical energy,kinetic energy,modern wind turbines,rotational energy,wind,rotor blades,motion,generator',
#                              key="my_input_kw_area2", help="Use comma without space to separate the terms")).split(sep=",")

#annotate_keyphrases(input_text, str(input_phrases))  
  
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

if clear:
    ui_message("Eres un crack")


# If the submit button was clicked, the checkbox dissapears
#else:
 #   st.session_state["checkbox"] = False


        

# If the submit button has not been clicked so far, the checkbox shows up
sample_text = ""
sample_phrases = ""
#st.session_state["disabled"] = False
if sample_text_checkbox:
    st.header("Preview text and terms")
    # Define the text to be processed
    sample_text = "Wind is used to produce electricity by converting the kinetic energy of air in motion into electricity. In modern wind turbines, wind rotates the rotor blades, which convert kinetic energy into rotational energy. This rotational energy is transferred by a shaft which to the generator, thereby producing electrical energy."
    # Define the phrases to be found and annotated in the text
    sample_phrases = ["Wind", "electricity", "kinetic energy",
               "wind turbines", "rotor blades", "rotational energy", "shaft", "generator", "electrical energy"]
    # Preview the text and phrases to be annotated
    st.write('**The text to be processed :point_down:**')

    # Create two columns to preview the texts
    c3, c4 = st.columns([1,3])
    with c3:
        st.write(pd.DataFrame({'Keyphrases': sample_phrases}))
    with c4:
        #st.success(sample_text)
        st.markdown(f"**:green[{sample_text}]**")

#phrases_list = []
#input_phrases = ""
# If the user clicks on the button...
if gettext_button:
    st.session_state.disabled = True
    #st.session_state["checkbox"] = False
    if agree == False and input_phrases == "":
        ui_warning("Hey, no term! Mark at least the automatic extraction :smile:")
    elif input_text != "" and input_phrases == "":
        st.error("Oops... no term provided :smile:")
    elif input_text == "" and input_phrases != "":
        st.warning(":question: Knock-knock... where is the text? ")
    else:
        st.subheader("Preview text and terms ")
        st.write('**The text to be processed :point_down:**')
        #input_phrases = input_phrases.split(sep=",")
        c5, c6 = st.columns([1, 3])
        with c5:
           st.write(pd.DataFrame({'Keyphrases': input_phrases + terms })) 
           #pd.DataFrame({'Keyphrases': input_phrases.split(sep=",")})
           #st.write(phrases)
           #input_phrases = pd.DataFrame(
            #    {'Keyphrases': input_phrases.split(sep=",")})
           #phrases_list = [x for x in phrases_to_list["Keyphrases"]]
           #terms = [x for x in df['Keyword']]
           #phrasesX
        with c6:
            #text = st.info(input_text)
            text = st.markdown(f"**:green[{input_text}]**")



#st.write("SAMPLE_TEXT CONTENT:", sample_text)
#st.write("INPUT_TEXT CONTENT:", input_text)

#st.write("SAMPLE_PHRASES CONTENT:", sample_phrases)
#st.write("INPUT_PHRASES CONTENT:", input_phrases)

#if gettext_button or sample_text_checkbox == True:

if sample_text_checkbox == True:
    text = sample_text
    final_phrases =  sample_phrases
else:
    text = input_text
    final_phrases = input_phrases + terms
    
#to check what is contained in each variable
#st.write("TEXT CONTENT:", text)
#st.write("PHRASES CONTENT:", phrases)
#st.write("TERMS CONTENT:", terms)
#st.write("TERMS AND PHRASES CONTENT:", terms + phrases)


   
#if gettext_button or sample_text_checkbox:
button1 = st.button("Annotate the text", key="button1")
# If gettext_button or sample_text_checkbox:

    
if button1:
    st.header("Visualize and annotate the text")
    annotate_keyphrases(text, final_phrases)

    
    
        
