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

st.title(":large_brown_circle: Dependency & Entity Analyzer :curly_loop: ")
st.markdown("Perform real-time analysis of a text to extract features and see a magical visualization of syntactical dependencies and named entities.")
# Load the English model in Spacy
#nlp = spacy.load("en_core_web_sm")

# Load the Spanish and English models
nlp_en = spacy.load("en_core_web_md")
nlp_es = spacy.load("es_core_news_sm")

# Use the st.radio function to create a radio button for the user to choose between Spanish and English
language = st.radio("**Choose a language**", ("English", "Spanish"))

# Use an if statement to select the appropriate language model based on the user's selection
if language == "English":
    nlp = nlp_en
else:
    nlp = nlp_es



# Create a dictionary containing example text in Spanish and English
examples = {
    "Spanish": "¡Hola! Me llamo Sergio. Vivo en España y trabajo como traductor, pero lo que realmente me encanta es investigar en PLN.",
    "English": "Hello, my name is Sergio. I live in Spain and I work as a translator, but my real passion is researching in NLP.",
}

# Use the st.checkbox function to create a checkbox that the user can use to load example data
if st.checkbox("Load example data"):
    # Set the text in the text area to the example text for the selected language
    text = examples[language]
else:
    # Otherwise, allow the user to enter their own text
    text = st.text_area("Enter some text:")


# st.text_input takes a label and default text string:
#input_text = st.text_input("Text string to analyze:", "On April 23d, when Brian Blinking-Eye, the Big Love Company CEO, was signing an agreement to share 3 million love cards with the world, they met in Paris for the G-23 Conference. That morning, they agreed to meet around 11pm at night, to enjoy a great concert featuring Bagus & Giulia Rock where they got lost in the crowd.")
# Send the text string to the SpaCy nlp object for converting to a 'doc' object.
doc = nlp(text)

if text:
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


