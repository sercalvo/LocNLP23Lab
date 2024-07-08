# -*- coding: utf-8 -*-

import spacy
import streamlit as st
from annotated_text import annotated_text
import random
import colorsys
import re

st.set_page_config(
    page_title="LocNLP23Lab - Text Annotation",
    page_icon="img//V-Logo-icon48.png",
)

# Load the Spacy model
nlp = spacy.load("en_core_web_sm")



# Function to generate annotated text for part of speech (POS)
def generate_annotated_text(text, pos_options, pos_select):
    doc = nlp(text)
    annotated_text_list = []
    for token in doc:
        if token.pos_ in pos_select:
            annotated_text_list.append((token.text, token.pos_, pos_options[token.pos_]))
        else:
            annotated_text_list.append(token.text + ' ')
    annotated_text_list[-1] = annotated_text_list[-1].rstrip()  # Remove trailing space
    return annotated_text_list


# Add a page title for the app
st.title(':large_green_circle: Text Annotation :female-detective:')
st.markdown('This app uses `Spacy`, `st-annotated-text`, `random` and `re` libraries to visualize words per part of speech.')

# Add a header for the first section: Select text
st.header("Add your text to analyze and annotate")

# get text input from user
input_type = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'], help="Only clean text format (.txt file)")

if input_type == 'Paste text':
    text = st.text_area('Enter text to analyze')
elif input_type == 'Select sample data':
    sample_data = {
        "Sample text 1 - Chuck Norris": "If an EMP were to go off within a close proximity of Chuck Norris, he would be rendered useless for a short period of time, because over 500 years ago, he traded the ability to see the future to Nostradamus for cybernetic arms, legs, and heart.",
        "Sample text 2 - The fox": "The quick brown fox jumps over the lazy dog.",
        "Sample text 3 - Bonucci": "Bonucci, whose contract expires next season, began his career at Inter Milan in 2005, where he won his first Serie A title in 2005-06. The defender also had spells at Treviso, Pisa, Genoa and Bari before joining Juventus in 2010, becoming part of a famous Juve backline along with Andrea Barzagli, Giorgio Chiellini and goalkeeper Gianluigi Buffon that dominated Italian football for a decade. The Turin giants won nine successive titles between 2011-12 and 2019-20, with Bonucci claiming eight of those after spending one season at AC Milan in 2017-18. Bonucci made his Italy debut in March 2010 and captained the side for the first time four years later. He represented the Azzurri at two World Cups and three European Championships, finishing runner-up at Euro 2012 before lifting the trophy nine years later following a penalty shootout win over England at Wembley.",
        "Sample text 4 - Shakespeare": """
                                Shall I compare thee to a summer’s day?
                                Thou art more lovely and more temperate:
                                Rough winds do shake the darling buds of May,
                                And summer’s lease hath all too short a date;
                                Sometime too hot the eye of heaven shines,
                                And often is his gold complexion dimm'd;
                                And every fair from fair sometime declines,
                                By chance or nature’s changing course untrimm'd;
                                But thy eternal summer shall not fade,
                                Nor lose possession of that fair thou ow’st;
                                Nor shall death brag thou wander’st in his shade,
                                When in eternal lines to time thou grow’st:
                                So long as men can breathe or eyes can see,
                                So long lives this, and this gives life to thee.
                                Sonnet 18: Shall I compare thee to a summer’s day?
                                BY WILLIAM SHAKESPEARE
        
        """
    }
    selected_sample = st.selectbox('Select sample data', list(sample_data.keys()))
    text = sample_data[selected_sample]
else:
    uploaded_file = st.file_uploader('Upload file', type=['txt'])
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    else:
        text = ''

max_words = 1000  # Maximum number of words to process
words = text.split()
if len(words) > max_words:
    st.warning(f"The input text has more than {max_words} words. Only the first {max_words} words will be processed.")
    words = words[:max_words]  # Keep only the first `max_words` words
    text = ' '.join(words)  # Reconstruct the text with the limited number of words



if text:
    # Process the text with Spacy
    doc = nlp(text)
    
    # Define the selectable part of speech tags and their corresponding colors
    pos_options = {
        'NOUN': '#ABD8E4',    # light purple
        'VERB': '#D5E8D4',    # light green
        'ADJ': '#FFE0B2',     # light orange
        'ADV': '#EDC8C8',     # light pink
        'PRON': '#ECC8ED',     # light violet
    }

    # Iterate over the tokens in the document
    for token in doc:
        # Check if the POS tag is already in the pos_options dictionary
        if token.pos_ not in pos_options:
            # If not, generate a random color similar to the existing colors
            hue = random.uniform(0, 1)
            saturation = random.uniform(0.5, 1)
            lightness = random.uniform(0.5, 1)
            rgb_color = colorsys.hls_to_rgb(hue, lightness, saturation)
            hex_color = '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb_color)

            # Assign the color to the POS tag
            pos_options[token.pos_] = hex_color

    # Get the unique part-of-speech tags from the document
    pos_tags = set([token.pos_ for token in doc])


    with st.expander("Advanced color configuration"):
        # Check if the advanced color configuration is enabled
        use_advanced_colors = st.checkbox('Change colors for POS')
        # Color configuration for POS tags
        if use_advanced_colors:
            for pos_tag in pos_options:
                hex_color = pos_options[pos_tag].lstrip('#')  # Remove the '#' character from the color string
                pos_options[pos_tag] = st.color_picker(f'Select color for {pos_tag}', '#' + hex_color)  # Add the '#' character back to the color string
   
        
    tab1, tab2, = st.tabs(["Part of Speech Annotation", "Named Entity Annotation"])
    
    with tab1:           
        ######################################################################
        # POS
        ##############################
        
        # Display the annotated text
        st.header('Highlight words by Part Of Speech')
        
        # Define the selectable options for part of speech annotation
        pos_select = st.multiselect('Select POS types for annotation', list(pos_options.keys()), default=[])
        
        # Generate the annotated text as a list of tuples based on the selected part of speech options
        annotated_text_list = generate_annotated_text(text, pos_options, pos_select)
        
        # Format the annotated text based on the selected part of speech options and colors
        formatted_text = []
        for token in annotated_text_list:
            if isinstance(token, tuple):
                if use_advanced_colors:
                    formatted_text.append((token[0], token[1], pos_options[token[1]]))
                else:
                    formatted_text.append((token[0], token[1]))
            else:
                formatted_text.append(token)
        formatted_text[-1] = formatted_text[-1].rstrip()  # Remove trailing space
        
        # Display the annotated text
        st.subheader('Annotated text with highlighted POS')
        annotated_text(*formatted_text)
        
        # Generate the annotated POS tags
        def generate_pos_tags(text, pos_select):
            doc = nlp(text)
            pos_tags = [token.text for token in doc if token.pos_ in pos_select]
            return pos_tags
        # Generate and display the annotated POS tags
        pos_tags = generate_pos_tags(text, pos_select)
        st.subheader('Annotated POS')
        if pos_tags:
            st.write(', '.join(pos_tags))
        else:
            st.info('Please select a POS type to highlight in the text.')
        
        st.divider()
     
        
    with tab2:       
        ###########################################################################
        # NER
        ########################
        
        # Generate the annotated NER entities
        def generate_ner_entities(text, ner_select):
            doc = nlp(text)
            ner_entities = [ent.text for ent in doc.ents if ent.label_ in ner_select]
            return ner_entities
        
        
        
        # Get the unique named entity labels from the document
        ner_labels = set([ent.label_ for ent in doc.ents])
        
        # Define the colors for named entity labels
        ner_colors = {
            label: color
            for label, color in zip(ner_labels, ['#EDC8C8', '#FFE0B2', '#D5E8D4', '#ABD8E4', '#ECC8ED'])
        }
        
        # Iterate over the tokens in the document
        for token in doc:
            # Check if the POS tag is already in the pos_options dictionary
            if token.ent_type_ not in ner_colors:
                # If not, generate a random color similar to the existing colors
                hue = random.uniform(0, 1)
                saturation = random.uniform(0.5, 1)
                lightness = random.uniform(0.5, 1)
                rgb_color = colorsys.hls_to_rgb(hue, lightness, saturation)
                hex_color = '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb_color)

                # Assign the color to the POS tag
                ner_colors[token.ent_type_] = hex_color
        
        def generate_ner_annotated_text(text, ner_select):
            doc = nlp(text)
            annotated_text = ''
            for token in doc:
                if token.ent_type_ in ner_select:
                    ner_label = token.ent_type_
                    ner_color = ner_colors.get(ner_label, '#FFFFFF')
                    annotated_text += f'<span style="display: inline-flex; flex-direction: row; align-items: center; background: {ner_color}; border-radius: 0.5rem; padding: 0.25rem 0.5rem; overflow: hidden; line-height: 1;">' \
                                      f'{token.text} <span style="border-left: 1px solid; opacity: 0.1; margin-left: 0.5rem; align-self: stretch;"></span>' \
                                      f'<span style="margin-left: 0.5rem; font-size: 0.75rem; opacity: 0.5;">[{ner_label}]</span></span> '
                else:
                    annotated_text += token.text_with_ws
            
            # Remove spaces before punctuation
            annotated_text = re.sub(r"\s+([.,!?;:])", r"\1", annotated_text)
            
            return annotated_text.strip()
        
        
        
        if ner_labels:
            # Add a header for the NER section
            st.header('Highlight words by Named Entity')
        
            # Define the selectable options for named entity recognition (NER)
            ner_select = st.multiselect('Select entity types for annotation', list(ner_labels), default=[])
        
            # Generate the annotated text for named entities
            ner_annotated_text = generate_ner_annotated_text(text, ner_select)
        
            # Display the annotated text for named entities
            st.subheader('Annotated text with highlighted entities')
            st.markdown(ner_annotated_text, unsafe_allow_html=True)
        
        
            # Generate and display the annotated NER entities
            ner_entities = generate_ner_entities(text, ner_select)
            st.subheader('Annotated Named Entities')
            if ner_entities:
                st.write(', '.join(ner_entities))
            else:
                st.info('Please select a NER type to highlight in the text.')
        
        st.divider()
    
    
        # Add a footer for the app
        st.markdown('**Note:** This is a basic text annotation app using `Spacy`, `st-annotated-text`, `random` and `re` libraries.')
    


