# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 15:35:03 2022

@author: ACER
"""

import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import requests
import difflib

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path    
 
st.header("MOVIE RECOMMENDATION ENGINE")

    
df=pd.read_csv("movies.csv")

selected_feature = ['genres','keywords','tagline','cast','director']

for feature in selected_feature:
    df[feature] = df[feature].fillna('')
    
combi_feature = df['genres']+' '+df['keywords']+' '+df['tagline']+' '+df['cast']+' '+df['director']

vec= TfidfVectorizer()
feature_vec=vec.fit_transform(combi_feature)

similarity= cosine_similarity(feature_vec)

movie_name = st.text_input("Enter the movie")
bb = st.button("SUBMIT")

recommended_movies = []
movie_photos = []

col1, col2, col3, col4, col5 = st.columns(5)

if bb is True:
    #st.write("Recommended Movies Are:")
    

    list_of_all_movies = df["title"].tolist()
    
    close_match =difflib.get_close_matches(movie_name,list_of_all_movies)

    if len(close_match) == 0:
        st.write("***SORRY No Matching movies***")

    else:



    
        close_match_new = close_match[0]
        
        index_movie =df[ df.title == close_match_new]['index'].values[0]
        
        similarity_score = list(enumerate(similarity[index_movie]))
        
        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse=True)
        #st.subheader("Recommended Movies Are:")
    
        i=1
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = df[df.index==index]['title'].values[0]
            movie_id = df[df.index==index]['id'].values[0]
            if (i<6):
                #st.write(title_from_index,movie_id)
                
                images = fetch_poster(movie_id)
                if i == 1:
                    with col1:
                        st.image(images)
                        st.write(title_from_index)
                elif i == 2:
                    with col2:
                        st.image(images)
                        st.write(title_from_index)
                elif i == 3:
                    with col3:
                        st.image(images)
                        st.write(title_from_index)
                elif i == 4:
                    with col4:
                        st.image(images)
                        st.write(title_from_index)

                elif i == 5:
                    with col5:
                        st.image(images)
                        st.write(title_from_index)



                #recommended_movies.append(title_from_index)
                #movie_photos.append(images)

                i+=1

#st.image(images)

    


