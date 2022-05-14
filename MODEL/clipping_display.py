# streamlit run clipping_display.py
import streamlit as st
from io import StringIO 
import pandas as pd
import os
import random
from libreria import clip_parser
from filters import title_recognition
from filters import quote_recognition
from filters import quote_similarity
from filters import topic_author_match
from doc2vecmodel import doc2vec_model
from ldamodel import lda_model

# SET UP
container = st.expander("Settings")
with container:
# Uploading the file
    last_user = st.checkbox('I was the last user')
    if last_user:
        placeholder = st.empty()
        placeholder2 = st.empty()
        name = placeholder.text_input("What is your name?")
        surname = placeholder2.text_input("What is your surname?")
        if len(name) != 0:
            if len(surname) != 0:
                full_name = name + '_' + surname
                with open(f'tempDir/name.txt', 'w') as f:
                            f.write(full_name)
    if not last_user:
        uploaded_files = st.file_uploader("Upload your clippings!", accept_multiple_files=True)
        if len(uploaded_files)!= 0:
            for uploaded_file in uploaded_files:
                placeholder = st.empty()
                placeholder2 = st.empty()
                name = placeholder.text_input("What is your name?")
                surname = placeholder2.text_input("What is your surname?")
                if len(name) != 0:
                    if len(surname) != 0:
                        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                        string_data = stringio.read()
                        full_name = name + '_' + surname
                        with open(f'tempDir/{full_name}_Clippings.txt', 'w') as f:
                            f.write(string_data)
                        with open(f'tempDir/name.txt', 'w') as f:
                            f.write(full_name)
        if st.button('Set Up'):
            with st.spinner('Setting Up...'):
                doc2vec_model(full_name = full_name)
                lda_model(full_name = full_name)
                
# UPLOADING DATA
my_clippings = clip_parser()

if 'full_name' in locals():
    title_name = full_name.replace('_', ' ')
    st.title(f"Kindle Clipping Reader - {title_name}")
else:
    st.title("Set Up Before Starting")

### SIDEBAR - Query Info
## initialize variables
title = ''
author = ''
topic = ''
quotequery = ''
similarquotes = ''

# Setting up variables
whatyouwant = st.sidebar.multiselect('What do you want to query?', ['Book Title', 'Book Author', 'Topic', 'Query', 'Similarity', 'Analytics'])
if 'Book Title' in whatyouwant:
    title = st.sidebar.text_input("Title")
if 'Book Author' in whatyouwant:
    author = st.sidebar.text_input("Author")
if 'Query' in whatyouwant:
    quotequery = st.sidebar.text_input("Quote Query")
if 'Similarity' in whatyouwant:
    quotes = my_clippings['citazione']
    if len(title) != 0 and len(quotequery) != 0:
        supraquotes = title_recognition (query= title).reset_index()
        quotes = quote_recognition (query= quotequery, data = supraquotes).reset_index()['citazione']
    if len(title) != 0 and len(quotequery) == 0:
        quotes = title_recognition (query= title).reset_index()['citazione']
    if len(title) == 0 and len(quotequery) != 0:
        quotes = quote_recognition (query= quotequery).reset_index()['citazione']
    initializer = pd.Series([''])
    quotes = initializer.append(quotes)
    similarquotes = st.sidebar.selectbox("Similar Quotes", quotes)
if 'Analytics' in whatyouwant:
    analytics = st.sidebar.button("Analytics")

if 'Topic' in whatyouwant:
    quotetopic = my_clippings['citazione']
    if len(title) != 0 and len(quotequery) != 0:
        zuppaquote = title_recognition (query= title).reset_index()
        quotetopic = quote_recognition (query= quotequery, data = zuppaquote).reset_index()['citazione']
    if len(title) != 0 and len(quotequery) == 0:
        quotetopic = title_recognition (query= title).reset_index()['citazione']
    if len(title) == 0 and len(quotequery) != 0:
        quotetopic = quote_recognition (query= quotequery).reset_index()['citazione']
    initializer = pd.Series([''])
    quotetopic = initializer.append(quotetopic)
    topic = st.sidebar.selectbox("Authors with Similar Topics", quotetopic)

quantity = st.sidebar.select_slider('How many random quotes do you want to see?', options= range(1,100), value = 20)

# setting up scenarios
scenario_1 = len(title) != 0 and len(quotequery) != 0 
scenario_2 = len(title) != 0 and len(quotequery) == 0 
scenario_3 = len(title) == 0 and len(quotequery) != 0 


## Similarity (cause its the last thing that comes)
if len(similarquotes) != 0: 
    st.subheader('"' + similarquotes+ '"')
    quote_recognized = quote_similarity(quote = similarquotes).reset_index()
    if st.button('Random Choice'):
        selected = random.sample(range(0, len(quote_recognized)), quantity)
        for index in selected:
            st.write(quote_recognized['citazione'][index])
            st.markdown('**' + quote_recognized['autore'][index] + '**' + ' - ' + '**' +  quote_recognized['titolo'][index] + '**')
    else:
        quote_recognized = quote_recognized.head(quantity)
        for index in range(len(quote_recognized)):
            st.write(quote_recognized['citazione'][index])
            st.markdown('**' + quote_recognized['autore'][index] + '**' + ' - ' + '**' +  quote_recognized['titolo'][index] + '**')

if len(topic) != 0:
    authors_recognized = topic_author_match(quote = topic, full_name=full_name)
    st.subheader('Here are some authors that treat similar topics')
    for index in range(len(authors_recognized)):
            st.markdown('**' + authors_recognized[index] + '**')

# then title, query, and the two combined
elif scenario_1:
    title_recognized = title_recognition (query= title).reset_index()
    st.subheader(title_recognized['autore'][0]+ ' - ' + title_recognized['titolo'][0])
    quote_recognized = quote_recognition (query= quotequery, data = title_recognized).reset_index()
   # similarquotes = st.sidebar.selectbox("Similar Quotes", quote_recognized)
    if st.button('Random Choice'):
        selected = random.sample(range(0, len(quote_recognized)), quantity)
        for index in selected:
            st.write(quote_recognized['citazione'][index])
            st.markdown('**' + quote_recognized['autore'][index] + '**' + ' - ' + '**' +  quote_recognized['titolo'][index] + '**')
    else:
        quote_recognized = quote_recognized.head(quantity)
        for index in range(len(quote_recognized)):
            st.write(quote_recognized['citazione'][index])
            st.markdown('**' + quote_recognized['autore'][index] + '**' + ' - ' + '**' +  quote_recognized['titolo'][index] + '**')

elif scenario_2: 
    title_recognized = title_recognition (query= title).reset_index()
    st.subheader(title_recognized['autore'][0]+ ' - ' + title_recognized['titolo'][0])
    if st.button('Random Choice'):
        selected = random.sample(range(0, len(title_recognized)), quantity)
        for index in selected:
            st.write(title_recognized['citazione'][index])
    title_recognized = title_recognized.head(quantity)
    for index in range(len(title_recognized)):
        st.write(title_recognized['citazione'][index])

elif scenario_3: 
    st.subheader('"' + quotequery+ '"')
    quote_recognized = quote_recognition (query= quotequery).reset_index()
   # similarquotes = st.sidebar.selectbox("Similar Quotes", quote_recognized)
    if st.button('Random Choice'):
        selected = random.sample(range(0, len(quote_recognized)), quantity)
        for index in selected:
            st.write(quote_recognized['citazione'][index])
            st.markdown('**' + quote_recognized['autore'][index] + '**' + ' - ' + '**' +  quote_recognized['titolo'][index] + '**')
    else:
        quote_recognized = quote_recognized.head(quantity)
        for index in range(len(quote_recognized)):
            st.write(quote_recognized['citazione'][index])
            st.markdown('**' + quote_recognized['autore'][index] + '**' + ' - ' + '**' +  quote_recognized['titolo'][index] + '**')







    



