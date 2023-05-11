# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 12:59:10 2022

@author: Sergio
"""

import streamlit as st
import time
import os
from os import path

st.set_page_config(
    page_title="LocNLP LAB",
    page_icon="img\\V-Logo-icon48.png",
)
from PIL import Image

# A helloworld
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#page_logo = Image.open(path.join(d, "..\\img\\LocNLP23.png"))
page_logo = Image.open('img\\LocNLP23.png')
st.image(page_logo) 


with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



st.markdown(
    """
    # NLP and Localization LAB
    \n**Welcome to the place where I test different NLP applications**
    \nYou will find some kind of magic. I'm sharing a few examples of how using Python and some available libraries and resources, a few things can be done. 
    I built this app using Streamlit, an open-source app framework built specifically for
    Machine Learning and Data Science projects.And of course, it includes many othe libraries like Spacy, NLTK, Transformers, Pandas, scikit-learn, Beautiful Soup, TextBlob, Gensim, PyTorch...
    \nEnjoy the ride! 
    \n:smiley: Sergio Calvo
    \n
    \n### Want to learn more?
    \n**👈 Select a demo from the sidebar** to see some examples
    of NLP apps!
"""
)