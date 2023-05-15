# -*- coding: utf-8 -*-
"""
Created on Sun May 14 18:05:33 2023

@author: Sergio
"""

import streamlit as st
import spacy
import re
import io

st.set_page_config(
    page_title="LocNLP23Lab - Sentiment & Subjectivity",
    page_icon="img//V-Logo-icon48.png",
)

# Load the 'en_core_web_sm' model
nlp = spacy.load('en_core_web_sm')

# Create a Streamlit app
st.title(":red_circle: Feature Extraction :magnet:")
st.markdown("""This app makes use of `Spacy`, `re` and `Streamlit` libraries to extract relevant information from a text. Feature extraction involves reducing the number of elements required to understand large datasets for text analysis, statistics and information extraction.""")

# Header
st.header("Add a text for analysis")
# Allow the user to paste a text, use the example text, or upload a file
option = st.radio("Select an option:", ("Paste text", "Use sample text", "Upload file"))
if option == "Paste text":
    text = st.text_area("Paste your text here", "")
elif option == "Use sample text":
    sample_data = {
        "Sample text 1": "John Smith works for Google in Mountain View, California. He can be reached at john.smith@gmail.com.",
        "Sample text 2": "Chuck Norris doesn't churn butter. He roundhouse kicks the cows and the butter comes straight out. When the Boogeyman goes to sleep every night, he checks his closet for Chuck Norris CNN was originally created as the 'Chuck Norris Network' to update Americans with on-the-spot ass kicking in real-time.",
        "Sample text 3": """Dear Hiring Manager, Your job posting on Craigslist for an Assistant Communications Director piqued my interest. Your description of the work responsibilities for the Assistant Director role closely matches my experience, and I am excited to submit my resume to you for your consideration. In my position as an Assistant Communications Director for ABC Company, I wrote articles for the company website, edited and posted contributed articles, managed the company's social media presence, and wrote and sent out a weekly email newsletter to subscribers. I also implemented an automated email tool that grew the company's subscriber base by 40% within six months. While Assistant Communications Director for Assemblyperson Janet Brown, I researched, drafted, and amended legislation, wrote press releases, and was responsible for office communications and correspondence. My resume is attached. If I can provide you with any further information on my background and qualifications, please let me know. I look forward to hearing from you. Thank you for your consideration. Sincerely, Joseph Green Joseph.Green@email.com 202-555-5252""",
    }
    selected_sample = st.selectbox('Select sample data', list(sample_data.keys()))
    text = sample_data[selected_sample]
elif option == "Upload file":
    file = st.file_uploader("Choose a file")
    # Get the contents of the file as a string
    if file:
        
        # To convert to a string based IO:
        stringio = io.StringIO(file.getvalue().decode("utf-8"))    
        # To read file as string:
        string_data = stringio.read()
        text = " ".join(string_data.split()) 
        #text = st.io.get_value(file)
    else:
        text = ''
        

if text:
    # Display the selected text
    st.subheader("Text to analyze")
    #st.write(string_data)
    st.markdown(f":green[{text}]")
    ##st.info(f":blue[{text}]")
    #st.success(text)

# Process the text
if st.button("Extract information from text"):
    doc = nlp(text)

    # Extract features
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    unique_names = set()
    unique_organizations = set()
    unique_locations = set()
    
    for entity, label in entities:
        if label == "PERSON":
            unique_names.add(entity)
        elif label == "ORG":
            unique_organizations.add(entity)
        elif label == "GPE":
            unique_locations.add(entity)
    
    names_list = list(unique_names)
    organization_list = list(unique_organizations)
    location_list = list(unique_locations)


    

    # Find emails using regular expression
    email_list = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text) or []

    # Display the results
    st.header("Information extraction results")
    if names_list:
        st.markdown("**:orange[Person Names:]**")
        for name in names_list:
            st.write("- " + name)
    else:
        st.caption(":red[**No person names** found in the text]")

    if organization_list:
        st.write("**:green[Organizations:]**")
        for organization in organization_list:
            st.write(" - " + organization)
    else:
        st.caption(":red[**No organizations** found in the text]")

    if location_list:
        st.write("**:blue[Locations:]**")
        for location in location_list:
            st.write("- " + location)
    else:
        st.caption(":red[**No locations** found in the text]")

    if email_list:
        st.write("**:violet[Emails:]**")
        for email in email_list:
            st.write("- " + email)
    else:
        st.caption(":red[**No emails** found in the text]")
