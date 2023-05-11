# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 02:24:01 2022

@author: Sergio
"""
import streamlit as st
import pandas as pd
import spacy
import matplotlib.pyplot as plt
import io
import altair as alt
import nltk
#import Counter
from collections import Counter

# Load the English language model in SpaCy
nlp = spacy.load("en_core_web_sm")

# Define a function to tokenize, lemmatize, and extract dependencies, POs, and ents
def process_text(text):
    # Tokenize and lemmatize the text
    doc = nlp(text)
    tokens = [token.text for token in doc]
    lemmas = [token.lemma_ for token in doc]

    # Extract dependencies, POs, and ents
    dependencies = [token.dep_ for token in doc]
    part_of_speech = [token.pos_ for token in doc]
    entities = [token.ent_type_ for token in doc]

    # Create a dataframe with the processed text
    df = pd.DataFrame(
        {
            "token": tokens,
            "lemma": lemmas,
            "dependency": dependencies,
            "part_of_speech": part_of_speech,
            "entity": entities,
        }
    )
    return df

# Define a function to display the dataframe in the app
def show_table(df):
    # Get the list of columns in the dataframe
    columns = list(df.columns)

    col1, col2 = st.columns([1,2])
    with col1:
        st.caption(":orange[The Magic NLP Dataframe]")
        # Allow the user to select which columns to display
        selected_columns = st.multiselect("**Select columns to display**", columns)   
    with col2:
        # Set the maximum width for the text in the dataframe
        pd.set_option("display.max_colwidth", 200)
    
        # Display the selected columns in the table
        st.write(df[selected_columns])
        
    
    


# Define a function to visualize the data: columns
def show_visualizations_1(df):
    # Calculate the counts of each part of speech
    pos_counts = df["part_of_speech"].value_counts()

    # Plot the part of speech counts as a bar chart
    st.bar_chart(pos_counts)

    
# Define a function to visualize the data: pie
def show_visualizations_2(df):
    # Calculate the counts of each category
    counts = df["part_of_speech"].value_counts()
    
    # Get the labels and sizes for the pie chart
    labels = counts.index
    sizes = counts.values
    
    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    ax.axis("equal")
    
    # Show the pie chart in the app
    st.pyplot(fig)

# Define a function to visualize the data: scatter
def show_visualizations_3(df):
    # Create a dataframe with the lemma counts
    lemma_counts = df["lemma"].value_counts()
    lemma_df = pd.DataFrame({"lemma": lemma_counts.index, "count": lemma_counts.values})
    
    # Create the scatter chart
    chart = (
        alt.Chart(lemma_df)
        .mark_circle()
        .encode(x="lemma", y="count")
    )
    
    # Display the scatter chart in the app
    st.altair_chart(chart, use_container_width=True) 
    
def show_visualizations_4(df):
    import plotly.express as px
    import streamlit as st
    
    df = px.data.gapminder()
    
    fig = px.scatter(
        df.query("year==2007"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
    )
    
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        # Use the native Plotly theme.
        st.plotly_chart(fig, theme=None, use_container_width=True)
    
# Define a function to create a dataframe with linguistic statistics
def create_linguistic_df(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Count the tokens
    token_counts = Counter(tokens)

    # Calculate the token frequencies
    total_tokens = len(tokens)
    token_frequencies = {token: count / total_tokens for token, count in token_counts.items()}

    # Create a dataframe with the token counts, frequencies, lengths, and part-of-speech tags
    df = pd.DataFrame({"token": list(token_counts.keys()), "count": list(token_counts.values()), "frequency": list(token_frequencies.values()), "length": [len(token) for token in token_counts.keys()], "pos_": [nltk.pos_tag([token])[0][1] for token in token_counts.keys()]})
    
    return df
def create_linguistic_df2(text):
    import spacy
    
    # Load the English model
    nlp = spacy.load("en_core_web_sm")
    
    # Tokenize and tag the text
    doc = nlp(text)
    
    # Create a dataframe with the tokens and their POS tags
    data = []
    for token in doc:
        data.append({"token": token.text, "pos": token.pos_})
    df = pd.DataFrame(data)
    return df

def show_visualizations_5(df):
    import plotly.express as px
    import streamlit as st
    

    
    # Create the scatter chart using the dataframe
    fig = px.scatter(
        df,
        x="frequency",
        y="count",
        size="length",
        color="token",
        hover_name="token",
        log_x=True,
        size_max=60,
    )
    
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:    
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        # Use the native Plotly theme.
        st.plotly_chart(fig, theme=None, use_container_width=True)
        
def show_visualizations_6(df):
    import plotly.express as px
    import streamlit as st
    
    # Calculate the word density
    df["density"] = df["count"] / df["length"]
    
    # Create the scatter chart using the dataframe
    fig = px.scatter(
        df,
        x="frequency",
        y="density",
        size="count",
        color="token",
        hover_name="token",
        log_x=True,
        size_max=60,
    )
    
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:    
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        # Use the native Plotly theme.
        st.plotly_chart(fig, theme=None, use_container_width=True)
        
def calculate_tfidf(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Count the tokens
    token_counts = Counter(tokens)

    # Calculate the token frequencies
    total_tokens = len(tokens)
    token_frequencies = {token: count / total_tokens for token, count in token_counts.items()}

    # Create a dataframe with the token counts, frequencies, lengths, and part-of-speech tags
    df = pd.DataFrame({"token": list(token_counts.keys()), "count": list(token_counts.values()), "frequency": list(token_frequencies.values()), "length": [len(token) for token in token_counts.keys()], "pos_": [nltk.pos_tag([token])[0][1] for token in token_counts.keys()]})
        
    # Load the English model
    nlp = spacy.load("en_core_web_sm")
    
    # Tokenize and tag the text
    doc = nlp(text)
    
    # Create a dataframe with the tokens and their POS tags
    #data = []
    for token in df["token"]:
        df.append({"pos": token.pos_})
    #df = pd.DataFrame(data)
    
    
    # Calculate the TF-IDF for each word in the text
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names()
    
    # Create a new column in the dataframe for the TF-IDF values
    df['tfidf'] = [tfidf_matrix[i, j] for i, j in enumerate(df['token'].index)]
    return df

def show_visualizations_7(df):
    import plotly.express as px
    import streamlit as st
    
    # Create the scatter chart using the dataframe
    fig = px.scatter(
        df,
        x="frequency",
        y="count",
        size="length",
        color="token",
        hover_name="token",
        log_x=True,
        size_max=60,
    )
    
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:    
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        # Use the native Plotly theme.
        st.plotly_chart(fig, theme=None, use_container_width=True)



# Define the main function
def main():
    
    #Title
    st.title(":large_blue_circle: Text Overview using NLP :mag_right: ")
    
    # Get some sample text
    example_text = "The the quick brown fox jumps over the lazy dog."
    
    text = ""
    
    # Allow the user to paste a text, use the example text, or upload a file
    option = st.radio("Select an option", ("Paste text", "Use example text", "Upload file"))
    if option == "Paste text":
        text = st.text_area("Paste your text here")
    elif option == "Use example text":
        text = example_text
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
        
    # Display the selected text
    st.subheader("Selected text to analyze")
    #st.write(string_data)
    st.markdown(f"**:green[{text}]**")
    ##st.info(f":blue[{text}]")
    #st.success(text)

    
    # Process the text
    df = process_text(text)
    
    # Show the dataframe as a table
    st.subheader("The Magic Dataframe :smile:")
    st.markdown("""This a simple and powerful dataframe. It includes several NLP applications at the distance of one click: :blue[**tokenizer**], :green[**lemmatizer**], :orange[**name entity recognition**], :violet[**grammatical dependencies**] and :red[**part of speech**] analysis. Isn't it magic?""")
    show_table(df)

    # Add a submit button
    if st.button("Submit"):
        # Show the visualizations
        st.write("Visualizations:")
        #with st.columns(2):    
        col1, col2 = st.columns(2)
        with col1:   
            show_visualizations_1(df)
        with col2:
            show_visualizations_2(df)
        show_visualizations_3(df)
        show_visualizations_4(df)
        show_visualizations_5(create_linguistic_df(text))
        show_visualizations_6(create_linguistic_df(text))
        show_visualizations_7(calculate_tfidf(text))


# Run the main function
if __name__ == "__main__":
    main()
   

