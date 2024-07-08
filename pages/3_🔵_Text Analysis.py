# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 01:01:59 2022

@author: Sergio
"""
from vfunctions import *
import streamlit as st
import spacy
from spacy import displacy
import io

import os
from os import path

st.set_page_config(
    page_title="LocNLP23Lab - Text Analysis",
    page_icon="img//V-Logo-icon48.png",
)

# Load the English language model in SpaCy
nlp = spacy.load("en_core_web_sm")


# Define the main function

def main():
    
    #Title
    st.title(":large_blue_circle: Text Analysis using NLP :mag_right: ")
    st.markdown(
        'This app makes use of `Spacy`, `NLTK`, `Pandas` or `Matplotlib` libraries to provide text analysis, statistics and nice visualizations.')
    
    # Get some sample text
    sample_text = """
    The the quick brown fox jumps over the lazy dog. 
    """
    
    text = ""
    
    # Header
    st.header("Add a text for analysis")
    
    # Allow the user to paste a text, use the example text, or upload a file
    option = st.radio('Choose input type:', ['Paste text', 'Select sample data', 'Upload file'], help="Only clean text format (.txt file)")
    if option == "Paste text":
        text = st.text_area("Paste your text here", "")
    elif option == "Select sample data":
        sample_data = {
            "Sample text 1 - Chuck Norris": "If an EMP were to go off within a close proximity of Chuck Norris, he would be rendered useless for a short period of time, because over 500 years ago, he traded the ability to see the future to Nostradamus for cybernetic arms, legs, and heart.",
            "Sample text 2 - The fox": "The quick brown fox jumps over the lazy dog.",
            "Sample text 3 - Huckleberry Fin": """I felt good and all washed clean of sin for the first time I had ever felt so in my life, and I knowed I could pray now. But I didn't do it straight off, but laid the paper down and set there thinking--thinking how good it was all this happened so, and how near I come to being lost and going to hell. And went on thinking. And got to thinking over our trip down the river; and I see Jim before me all the time: in the day and in the night-time, sometimes moonlight, sometimes storms, and we a-floating along, talking and singing and laughing. But somehow I couldn't seem to strike no places to harden me against him, but only the other kind. I'd see him standing my watch on top of his'n, 'stead of calling me, so I could go on sleeping; and see him how glad he was when I come back out of the fog; and when I come to him again in the swamp, up there where the feud was; and such-like times; and would always call me honey, and pet me and do everything he could think of for me, and how good he always was; and at last I struck the time I saved him by telling the men we had small-pox aboard, and he was so grateful, and said I was the best friend old Jim ever had in the world, and the ONLY one he's got now; and then I happened to look around and see that paper.
                        It was a close place. I took it up, and held it in my hand. I was a-trembling, because I'd got to decide, forever, betwixt two things, and I knowed it. I studied a minute, sort of holding my breath, and then says to myself: All right, then, I'll GO to hell --and tore it up. 
                        Mark Twain, The Adventures of Huckleberry Finn""",
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
                                       """,
            "Sample text 5 - San Francisco": "San Francisco has reversed its decision to authorise police to use robots equipped with lethal weapons.The proposal, which was passed last week by the city's legislators, the board of supervisors, would have allowed police to access robots that can kill. It had faced fierce criticism from civil liberties groups. After voting unanimously to pause the proposal on Tuesday, the board sent the issue to committee for further review. The measure would have allowed the San Francisco Police Department (SFPD) to kill suspects with robots in extreme situations. The vote came following a new California law requiring city police forces to keep inventories of military-grade equipment and seek approval for their use. Dr Catherine Connolly, from the group Stop Killer Robots, told the BBC the move was a 'slippery slope' that could distance humans from killing. Protesters and several dissenting board members gathered on the steps of city hall to call for the city to reverse its decision. In a secondary vote, usually reserved to rubber-stamp board decisions, they decided to overturn their vote. The original proposal will now be refined or entirely scrapped. Police have argued that the robots would only be used in extreme circumstances. A spokesperson for SFPD said 'robots could potentially be equipped with explosive charges to breach fortified structures containing violent, armed, or dangerous subjects'. They also said robots could be used to 'incapacitate, or disorient violent, armed, or dangerous suspects who pose a risk of loss of life'. This type of lethal robot is already in use in other parts of the US. In 2016, police in Dallas, Texas, used a robot armed with C-4 explosive to kill a sniper who had killed five officers and injured several more."
  
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
            
            


    if text != "":
            
        # Display the selected text
        st.caption("Showing only first 1000 words in the text")
        words = text.split()[:1000]
        limited_text = ' '.join(words)
        st.markdown(f'<div style="height: 300px; overflow-y: scroll;">{limited_text}</div>', unsafe_allow_html=True)
    
        
        # Process the text
        df = process_text(text)
        
        st.divider() 
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)  
        
        # Show the dataframe as a table
        st.subheader("The Magic NLP Dataframe :smile:")
        st.caption("It looks simple, but it is powerful")
        st.markdown("""This dataframe or table includes several NLP applications at the distance of one click: :blue[**tokenizer**], :green[**lemmatizer**], :orange[**named entity recognition**], :violet[**grammatical dependencies**] and :red[**part of speech**] analyzer. Isn't it magic to have all these NLP applications in one single dataframe?""")
        show_magic_dataframe(df)

        st.divider()  

        # Add a submit button
        st.header("Complete linguistic analysis")
        st.write("Get a text overview and some statistics, just for the sake of it.")
        submit_button = st.button("Run linguistic analysis")    
        
        if submit_button:        
            
            # Show the rough statistical analysis
            analyze_text(text, nlp)
            
            


# Define a function to analyze a text and print the results
def analyze_text(text, nlp):
    # Process the text with the spacy model
   
    doc = nlp(text)

    st.subheader("A rough statistical analysis of the text")

    
    with st.container():
               
        # Print the number of words in the text
        st.success(f"The text contains **{count_words(text)}** words. These words are grouped into **{len((list(doc.sents)))}** sentences. Not all sentences have the same length. The sentences in this text range from **{num_words_shortest_sentence(text)}** to **{num_words_longest_sentence(text)}** words per sentence. The average of words per sentence in this text is **{avg_num_words_per_sentence(text)}**, which shows its density.")
        # Print the number of sentences
        
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)     
        col1, col2, col3 = st.columns(3)
        col1.metric("Word count", count_words(text), "Valid words ")
        col2.metric("Sentences", len((list(doc.sents))), "Units of communication")
        col3.metric("Average words/sentence", avg_num_words_per_sentence(text), "Density")

       
    with st.container():
        # Cache the dataframe so it's only loaded once
        @st.cache_data
        def load_data():
            return pd.DataFrame(
                {
                    "Category": [1, 2, 3, 4],
                    "second column": [10, 20, 30, 40],
                }
            )
        load_data()
        
    with st.container():        
        # Count the POSs
                       
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.write("#### Top nouns") # should print ["dog", "fox", "The"]
            df = pd.DataFrame.from_dict(most_repeated_nouns(text, nlp), orient='index', columns=["Reps"])
            df
            
        with col5:
            st.write("#### Top verbs")
            df = pd.DataFrame.from_dict(most_repeated_verbs(text, nlp), orient='index', columns=["Reps"])
            df

        with col6:
            st.write("#### Top adjectives")
            df = pd.DataFrame.from_dict(most_repeated_adjectives(text, nlp), orient='index', columns=["Reps"])
            df

        with col7:
            st.write("#### Top adverbs")
            df = pd.DataFrame.from_dict(most_repeated_adverbs(text, nlp), orient='index', columns=["Reps"])
            df

        # Process the text
        df = process_text(text)        
        
        col8, col9 = st.columns(2)
        with col8:   
            
            st.write("#### Named entity counts")
            show_visualizations_1_NER(df)
            # Count and print the number of named entities
            ner_counts = count_ner(doc)
            for ner, count in ner_counts.items():
                st.write(" - ", ner, ": ", count)
                

            
        with col9:
            
            st.write("#### Part of speech counts")
            show_visualizations_2(df)
            # Count and print the number of each part of speech
            pos_counts = count_pos(doc)
            for pos, count in pos_counts.items():
                st.write(" - ", pos,": ", count)
        
        
    with st.container():
        # Display a section header:
        st.header("Named entities in the text")
        # Print a visualization of named entities
        st.write(visualize_ner(doc))
    
        # Display a section header:
        st.header("Dependency analysis for the first sentence")
        # Print a visualization of a dependency parse
        st.write(visualize_dep(list(doc.sents)[0]))





    # Process the text
    df = process_text(text)


# Add a submit button
#if st.button("Submit2"):        
    # Show the visualizations
    st.write("Visualizations")

    #show_visualizations_4(df)
    #show_visualizations_5(create_linguistic_df(text))
    show_visualizations_6(create_linguistic_df(text))
    #show_visualizations_7(calculate_tfidf(text))
    #create_linguistic_df(text)
    
    


# Run the main function
if __name__ == "__main__":
    main()
    
    
    
