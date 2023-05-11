# -*- coding: utf-8 -*-

import spacy
import streamlit as st
import spacy
from annotated_text import annotated_text

nlp = spacy.load("en_core_web_sm")

import streamlit as st
import spacy
from annotated_text import annotated_text


def generate_annotated_text(text, pos_options, pos_select):
    doc = nlp(text)
    annotated_text_list = []
    for token in doc:
        if token.pos_ in pos_select:
            annotated_text_list.append((token.text, token.pos_, pos_options[token.pos_]))
        else:
            annotated_text_list.append(token.text + ' ')
    annotated_text_list[-1] = annotated_text_list[-1].rstrip()  # remove trailing space
    return annotated_text_list


nlp = spacy.load('en_core_web_sm')

# define the selectable part of speech tags and their corresponding colors
pos_options = {
    'NOUN': '#ABD8E4',    # light purple
    'VERB': '#D5E8D4',    # light green
    'ADJ': '#FFE0B2',     # light orange
    'ADV': '#EDC8C8',     # light yellow-green
    'PRON': '#ECC8ED'     # light yellow-green (for pronouns)
}


# Add a page title for the app
st.title(':large_green_circle: Text Annotation :female-detective:')
st.markdown(
    'This app makes use of `Spacy` and `st-annotated-text` libraries to provide nice visualizations of words per part of speech.')

# Add a header for the first section: Select text
st.header("Add your text to analyze and annotate")

# get text input from user
input_type = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'])

if input_type == 'Paste text':
    text = st.text_area('Enter text to analyze')
elif input_type == 'Select sample data':
    sample_data = {
        "Text 1": "Chuck Norris doesn't churn butter. He roundhouse kicks the cows and the butter comes straight out. When the Boogeyman goes to sleep every night, he checks his closet for Chuck Norris CNN was originally created as the 'Chuck Norris Network' to update Americans with on-the-spot ass kicking in real-time.",
        "Text 2": "The quick brown fox jumps over the lazy dog."
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
    #st.write(text)
    st.markdown(f"**:green[{text}]**")

    # display the annotated text
    st.header('Select Part of Speech to show')
    
    # define the selectable options for part of speech annotation
    pos_select = st.multiselect('Select part of speech for automatic annotation', list(pos_options.keys()), default=[])
    
    # generate the annotated text as a list of tuples based on the selected part of speech options
    annotated_text_list = generate_annotated_text(text, pos_options, pos_select)

    st.write('The available part of speech tags are:', list(pos_options.keys()))

    # add color selection options
    use_advanced_colors = st.checkbox('Advanced color selection')
    if use_advanced_colors:
        for pos in pos_options:
            pos_options[pos] = st.color_picker(f'Select color for {pos}', pos_options[pos])
        
    # format the annotated text based on the selected part of speech options and colors
    formatted_text = []
    for token in annotated_text_list:
        if isinstance(token, tuple):
            if use_advanced_colors:
                formatted_text.append((token[0], token[1], pos_options[token[1]]))
            else:
                formatted_text.append((token[0], token[1]))
        else:
            formatted_text.append(token)
    formatted_text[-1] = formatted_text[-1].rstrip()  # remove trailing space

    st.subheader('Annotated text')
    st.write(annotated_text(*formatted_text))

    
