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
    page_title="LocNLP23Lab",
    page_icon="img//V-Logo-icon48.png",
)
from PIL import Image

# A helloworld
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#page_logo = Image.open(path.join(d, "..\\img\\LocNLP23.png"))
page_logo = Image.open('img//LocNLP23lab.png')


with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.image(page_logo) 
st.markdown(
    """
    # NLP and Localization LAB
    \n### Welcome to the place where I test my NLP apps ideas!
    \nYou will find some kind of magic, but it's a matter of believing or not. I do believe in the magic of computational linguistics and natural language processing.
    \nI'm sharing a few examples of how using Python and some available libraries and resources, a few things can be done. 
    I have built this app using `Streamlit`, an open-source app framework built specifically for
    Machine Learning and Data Science projects. Behind, there's a full range of libraries and Python code, of course. I am not an expert, but do take advantage of libraries like `Spacy`, `NLTK`, `Transformers`, `Pandas`, `scikit-learn`, `Beautiful Soup`, `TextBlob`, `Gensim`, `PyTorch` and other libraries.
    \nThe goal? Unveil the secrets of languages, no matter if they are meant for humans or computers.
    \nEnjoy the ride! 	:bike:
    \n:smiley: Sergio Calvo
"""
)

with st.expander("About Sergio"):
    st.write("""Translator, reviewer and computational linguist with 20+ years of experience in multiple translation and localization areas, NLP (Natural Language Processing) and localization engineering. He is passionate for going deep in the entrails of any language, either spoken by humans or computer machines, to unveil the beauty of communicating.
             \n Get more info at [www.veriloquium.com](https://www.veriloquium.com)""")

st.markdown(
    """
   \n
   \n### Want to learn more?
   \n**👈 Select a demo from the sidebar** to see some NLP app examples!
   """
   )