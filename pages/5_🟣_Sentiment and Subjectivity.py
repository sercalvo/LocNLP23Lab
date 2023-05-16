# -*- coding: utf-8 -*-
"""
Created on Wed May 10 00:07:36 2023

@author: Sergio
"""

import streamlit as st
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import plotly.graph_objects as go

import os
from os import path

st.set_page_config(
    page_title="LocNLP23Lab - Sentiment & Subjectivity",
    page_icon="img//V-Logo-icon48.png",
)

# Download necessary NLTK packages and corpora
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Define an official taxonomy of text types and subject matter
taxonomy = {
    'Type': {
        'News': ['Breaking News', 'Local News', 'International News'],
        'Opinion': ['Editorials', 'Op-eds', 'Commentaries'],
        'Feature': ['Human Interest', 'Lifestyle', 'Travel']
    },
    'Subject': {
        'Politics': ['National Politics', 'International Relations', 'Election Coverage'],
        'Business': ['Stock Market', 'Corporate News', 'Economy'],
        'Technology': ['Gadgets', 'Apps', 'Social Media'],
        'Science': ['Environment', 'Space', 'Health']
    }
}

# Create a Streamlit app
st.title(':large_purple_circle: Sentiment Analysis and Subjectivity :zipper_mouth_face:')
st.markdown('This app makes use of `Streamlit`, `NLTK`, `sumy`, `textblob` and `plotly` libraries to provide a rough analysis on polarity and subjectivity.')

# Add a header for the first section: Select text
st.header("Add your text to analyze")
# get text input from user
input_type = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'], help="Only clean text format (.txt file)")
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

    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    # Remove stop words and stem the remaining words
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    filtered_words = [stemmer.stem(word.lower()) for word in words if word.lower() not in stop_words]
    
    # Use TextBlob library to determine the sentiment of the text
    text_blob = TextBlob(text)
    polarity = text_blob.sentiment.polarity
    subjectivity = text_blob.sentiment.subjectivity
    
    # Use Sumy library to summarize the text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count=3)
    
    # Join the summary sentences into a string
    summary_str = " ".join([str(sentence) for sentence in summary])
    
    # Use NLTK library to determine the parts of speech in the text
    pos_tags = nltk.pos_tag(filtered_words)
    noun_count = sum([1 for word, pos in pos_tags if pos.startswith('N')])
    verb_count = sum([1 for word, pos in pos_tags if pos.startswith('V')])
    adj_count = sum([1 for word, pos in pos_tags if pos.startswith('J')])
    adv_count = sum([1 for word, pos in pos_tags if pos.startswith('R')])
    
    # Use TextBlob library to categorize the text according to the official taxonomy
    classifier_data = []
    for k, v in taxonomy.items():
        for kk, vv in v.items():
            for vvv in vv:
                classifier_data.append((vvv, k + '.' + kk))
    classifier = NaiveBayesClassifier(classifier_data)
    category = classifier.classify(text)
    
    # Display the results to the user
    st.header('Analysis results')
    
    st.subheader('Text Analysis')
    if polarity > 0:
        st.markdown(f'**Polarity: :green[{polarity} - Positive sentiment]**')
    elif polarity < 0:
        st.markdown(f'**Polarity: :red[{polarity} - Negative sentiment]**')
    elif subjectivity == 0:
        st.markdown(f'**Polarity: {polarity} - Neutral**')
    else:
        st.markdown(f'**Polarity: {polarity}**')
    st.caption("**Polarity refers to the sentiment expressed in the text**. A positive polarity indicates a positive sentiment, while a negative polarity indicates a negative sentiment. A polarity of 0 indicates a neutral sentiment.")
    
    if subjectivity > 0.5:
        st.markdown(f'**Subjectivity: :red[{subjectivity} - Highly subjective]**')
    elif 0.01 <= subjectivity <=  0.5:
        st.markdown(f'**Subjectivity: :orange[{subjectivity} - Moderately subjective]**')
    elif subjectivity == 0.0:
        st.markdown(f'**Subjectivity: {subjectivity} - Neutral**')
        
    else:
        st.markdown(f'**Subjectivity: {subjectivity}**')

    st.caption("**Subjectivity refers to how subjective or objective the text is**. A high subjectivity score indicates that the text is subjective and contains personal opinions, while a low subjectivity score indicates that the text is objective and presents factual information.")
    
    st.subheader('Text Categorization')
    st.write(f'**Category:** {category}')
    st.subheader('Text Summary')
    st.write(summary_str)

    st.header("How polarity and subjectivity are represented by POS categories")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader(f'Nouns: :green[{noun_count}]')
        st.subheader(f'Verbs: :green[{verb_count}]')
        st.subheader(f'Adjectives: :green[{adj_count}]')
        st.subheader(f'Adverbs: :green[{adv_count}]')
    with col2:
        fig = go.Figure(data=[go.Pie(labels=['Nouns', 'Verbs', 'Adjectives', 'Adverbs'], 
                                     values=[noun_count, verb_count, adj_count, adv_count],
                                     hole=.3)])
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    




