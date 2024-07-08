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
import spacy


import os
from os import path

st.set_page_config(
    page_title="LocNLP23Lab - Wordcloud",
    page_icon="img//V-Logo-icon48.png",
)


# Function to generate word cloud with basic contour
def generate_better_wordcloud(data, title, mask=None):
    cloud = WordCloud(scale=3,
                      max_words=150,
                      colormap='tab20c',
                      #colormap='RdYlGn',
                      mask=mask,
                      background_color='white',
                      stopwords=stop_words,
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
st.write("This app will do the rest, that is to say, tokenize the text, remove stopwords and count the most relevant words.")


# Load the Spanish and English models
nlp_en = spacy.load("en_core_web_md")
nlp_es = spacy.load("es_core_news_sm")


# Use the st.radio function to create a radio button for the user to choose between Spanish and English
language = st.radio("Choose a language:", ("English", "Spanish"))

# Use an if statement to select the appropriate language model based on the user's selection
if language == "English":
    nlp = nlp_en
    sample_data = {
        "Sample text 1 - Simple sentence": "The quick brown fox jumps over the lazy dog.",
        "Sample text 2 - Philosophy": """Jean-Paul Sartre belongs to the existentialists. For him, ultimately humans are "condemned to be free". There is no divine creator and therefore there is no plan for human beings. But what does this mean for love, which is so entwined with ideas of fate and destiny? Love must come from freedom, it must be blissful and mutual and a merging of freedom. But for Sartre, it isn't: love implies conflict. The problem occurs in the seeking of the lover's approval, one wants to be loved, wants the lover to see them as their best possible self. But in doing so one risks transforming into an object under the gaze of the lover, removing subjectivity and the ability to choose, becoming a "loved one". """,
        "Sample text 3 - Wind energy": "Wind is used to produce electricity by converting the kinetic energy of air in motion into electricity. In modern wind turbines, wind rotates the rotor blades, which convert kinetic energy into rotational energy. This rotational energy is transferred by a shaft which to the generator, thereby producing electrical energy. Wind power has grown rapidly since 2000, driven by R&D, supportive policies and falling costs. Global installed wind generation capacity – both onshore and offshore – has increased by a factor of 98 in the past two decades, jumping from 7.5 GW in 1997 to some 733 GW by 2018 according to IRENA’s data. Onshore wind capacity grew from 178 GW in 2010 to 699 GW in 2020, while offshore wind has grown proportionately more, but from a lower base, from 3.1 GW in 2010 to 34.4 GW in 2020. Production of wind power increased by a factor of 5.2 between 2009 and 2019 to reach 1412 TWh."
    }
    stop_words = set(nltk.corpus.stopwords.words('english'))
    modal_verbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would']
    # Set the text for the sample pres word cloud
    textito = "Create a word cloud with the text of a lovely book?"
    
elif language == 'Spanish':
    nlp = nlp_es
    sample_data = {
        "Sample text 1": "Chuck Norris no cree que haya 50 estados en Estados Unidos. Sólo hay uno: Estado de emergencia. Allá por donde pasa es una emergencia. Chuck Norris hace el desayuno de los campeones. Literalmente. Se comió a Fernando Alonso, Tiger Woods y a Roger Federer en una sola comida.",
        "Sample text 2": "La inteligencia artificial es la gran apuesta de las principales compañías tecnológicas, y Google acaba de dejar claro que está dispuesta a sacarle el mayor provecho. En su conferencia anual Google I/O en Mountain View, California, el CEO de la Alphabet, Sundar Pichai, habló del objetivo de la compañía para hacer la inteligencia artificial «útil para todos», presentando varios ejemplos de cómo esta tecnología mejorará varios de sus productos."
    }
    stop_words = set(nltk.corpus.stopwords.words('spanish'))
    modal_verbs = ['poder', 'puede', 'podría', 'deber', 'debe']
    # Set the text for the sample pres word cloud
    textito = "Crea una nube de palabras con el texto de un libro maravilloso."
else:
    stop_words = set()
    modal_verbs = []

# Add or update stopwords with modal verbs
stop_words.update(modal_verbs)


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


#texto = ""


# Use function to generate wordcloud
generate_better_wordcloud(textito, 'A book in a wordcloud\n', mask=mask)

wordcloud = None
if not text:
    st.pyplot(plt)



if text:
    st.subheader('Text to save in a cloud')
    #st.write(text)
    # En verde
    ###st.markdown(f":green[{text}]") # En verde
    # Todas las palabras
    ###st.markdown(f'<div style="height: 300px; overflow-y: scroll;">{text}</div>', unsafe_allow_html=True) # Todas las palabras
    # Solo 1000 palabras para mostrar
    st.caption("Showing only first 1000 words in the text")
    words = text.split()[:1000]
    limited_text = ' '.join(words)
    st.markdown(f'<div style="height: 300px; overflow-y: scroll;">{limited_text}</div>', unsafe_allow_html=True)

# Upload a file
#file = st.file_uploader("Choose a file", label_visibility="collapsed")


# Open the file


    # Create the word cloud and display it
    st.title("Your Wordcloud")
    #st.markdown(text)
    # Create a word cloud object
    #texto = open_file(file)
    
    
    #############################################################
    if text:
        
        title = st.text_input("Hey! Enter a nice title for your cloud")
        if title:
            def generate_wordcloud(text, title, png):
            
                def top999_words(text):
                    # Tokenize the text
                    tokens = nltk.word_tokenize(text)
                
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
                #stopwords = set(STOPWORDS)
                #stopwords.add("says")
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
                    colormap='Set2', 
                    collocations=False, 
                    stopwords = stop_words,
                    contour_color='LightGray',
                    contour_width=1,
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
                
            
            generate_wordcloud(text, title,"img//clouds.png")
            finished = st.pyplot(plt)
            
            with open("news.png", "rb") as file:
                btn = st.download_button(
                        label="Download image",
                        data=file,
                        file_name="A cloud from Sergio.png",
                        mime="image/png"
                      )
                            
    
