# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 22:31:33 2022

@author: Sergio
"""

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st
import vfunctions
from vfunctions import open_file
import numpy as np
from PIL import Image
import os
from os import path
import nltk
import time


# Function to generate word cloud with basic contour
def generate_better_wordcloud(data, title, mask=None):
    cloud = WordCloud(scale=3,
                      max_words=150,
                      colormap='tab20c',
                      #colormap='RdYlGn',
                      mask=mask,
                      background_color='white',
                      stopwords=None,
                      collocations=True,
                      contour_color='LightGray',
                      contour_width=1).generate_from_text(data)
    plt.figure(figsize=[10,10])
    plt.imshow(cloud)
    plt.axis('off')
    plt.title(title)
    plt.show()

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()



# read the mask image taken from
mask = np.array(Image.open(path.join(d, "img//clouds.png")))

# adding movie script specific stopwords
stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")


# Set the title
st.title(":large_yellow_circle: :partly_sunny: A book in a wordcloud :cloud: ")
st.subheader("Have time for a quick magic moment? :sparkles:")
st.write("Pick up a book of your choice in plain text format. If not an easy thing at this moment, you can download one from the awesome [Project Gutenberg](https://www.gutenberg.org/browse/scores/top).")

# Add a header
st.subheader("Add some text to create your word cloud")
# Upload a file
file = st.file_uploader("Choose a file", label_visibility="collapsed")

# Set the text for the sample pres word cloud
text = "Create a word cloud with the text of a lovely book?"
# Use function to generate wordcloud
generate_better_wordcloud(text, 'A book in a wordcloud\n', mask=mask)



texto = ""
wordcloud = None
if not file:
    st.pyplot(plt)


# Open the file

else:

    # Create the word cloud and display it
    st.title("Your Word Cloud")
    #st.markdown(text)
    # Create a word cloud object
    texto = open_file(file)
    
    
    #############################################################
    if text:
        title = ""
        def generate_wordcloud(text, title, png):
        
            def top999_words(text):
                
                import spacy
                import nltk
            
                nlp = spacy.load("en_core_web_sm")
            
                # Tokenize the text
                tokens = nltk.word_tokenize(text)
                # Remove stopwords
                stop_words = set(nltk.corpus.stopwords.words('english'))
            
                # Remove modal verbs
                modal_verbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would']
                #stop_words.difference_update(modal_verbs)
                stop_words.update(modal_verbs)
            
                # Create a list of filtered tokens
                filtered_tokens = []
            
                # Process the text with spacy
                doc = nlp(text)
            
                # Lemmatize the verbs and add them to the list of filtered tokens
                for token in doc:
                    if token.pos_ == "VERB":
                        filtered_tokens.append(token.lemma_)
                    else:
                        filtered_tokens.append(token.text)
            
                # Remove stopwords from the list of filtered tokens
                filtered_tokens = [token for token in filtered_tokens if token.isalpha() and token.lower() not in stop_words]
                # Get frequency of each word
                word_freq = nltk.FreqDist(filtered_tokens)
                # Create a list of the 1000 most frequent words with their frequency
                most_common = word_freq.most_common(1000)
                return most_common
        
            palabras_limpias = (top999_words(text))
        
        
        
            # adding movie script specific stopwords
            stopwords = set(STOPWORDS)
            stopwords.add("says")
            #print(stopwords)
        
            # Generate a word cloud image
            mask = np.array(Image.open(path.join(d, png))) 
            wordcloud = WordCloud(
                scale=3,
                max_words=150,
                #width = 3000, 
                #height = 2000, 
                #random_state=1, 
                background_color='white', 
                colormap='gist_stern', 
                collocations=False, 
                stopwords = stopwords,
                #contour_color='LightGray',
                #contour_width=1,
                mask=mask,).generate_from_frequencies(dict(palabras_limpias))
        
            # create coloring from image
            #image_colors = ImageColorGenerator(mask)
            plt.figure(figsize=[10,10])
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title(title)
            # store to file
            plt.savefig("news.png", format="png") 
            plt.show()
            
        
        generate_wordcloud(texto,"Una nube de palabras de prueba","img//clouds.png")
        finished = st.pyplot(plt)
            
    
