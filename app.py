import streamlit as st
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import tweepy
import requests
import streamlit.components.v1 as components


@st.cache(allow_output_mutation = True) 
def get_model() :
    tweet_l = []
    
    model_embedd = SentenceTransformer('bert-base-nli-mean-tokens')
    df = pd.read_csv(r"C:\Users\soora\Downloads\SIH\Streamlit\dataset.csv")
    
    user_id = 1562940172672864257
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAA%2B0aAEAAAAAozXmO8HEuPdcaYkoBtdInrsc%2Bh0%3DKWkwSxFOuYwDwPMWP76vDmzQFLiF9dTtoDh9ZUAAtS9cNlqaWo"
    api = tweepy.Client(bearer_token)
 
    for tweet in tweepy.Paginator(api.get_users_tweets, user_id, exclude='retweets', max_results=100).flatten(limit=100) :
        res = " ".join(str(tweet).split())
        tweet_l.append([res, tweet.id])
        
    moea_replacement = ['external affairs minister','foreign affairs minister','minister of external affairs','foreign minister','subrahmanyam jaishankar']
    moea_regex = re.compile('|'.join(map(re.escape, moea_replacement)))

    govi_replacement = ['the government of india','indian government','govt of i','goi','central government']
    govi_regex = re.compile('|'.join(map(re.escape, govi_replacement)))

    health_replacement = ['minister of health', 'Dr. Bharati Pravin Pawar ','dr. pravin pawar','dr. pawar', 'health minister','health and welfare minister']
    hwmi_regex = re.compile('|'.join(map(re.escape, health_replacement)))

    finance_replacement = ['minister of finance', 'finance minister ','Vitt Mantrī','Smt Nirmala Sitharaman', 'Nirmala Sitharaman']
    fmi_regex = re.compile('|'.join(map(re.escape, finance_replacement)))

    ind_replacement = ['india', 'India' ,'bharat','Bharat']
    ind_regex = re.compile('|'.join(map(re.escape, ind_replacement)))
    
    replacement = ['modi', 'modiji', 'pmoi', 'Modi', 'Modiji', 'pmo', 'prime minister of india', 'narendra modi','pm modi']
    modi_regex = re.compile('|'.join(map(re.escape, replacement)))
        
    return model_embedd, df, tweet_l, moea_regex, govi_regex, hwmi_regex, fmi_regex, ind_regex, modi_regex

def theTweet(tweet_url):
    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    res = response.json()["html"]
    return res

model_embedd, df, tweet_l, moea_regex, govi_regex, hwmi_regex, fmi_regex, ind_regex, modi_regex = get_model()

st.title("FAKE  NEWS  FLAGGING  SYSTEM")
st.text(" ")

def result( tweet_inp ) :
    for j in tweet_inp :
        max_sim = 0
        flag = True
        
        tweet_inp = j[0]
        tweet_inp = fmi_regex.sub("fmi", tweet_inp)
        tweet_inp = hwmi_regex.sub("hwmi", tweet_inp)
        tweet_inp = govi_regex.sub("govi", tweet_inp)
        tweet_inp = moea_regex.sub("moea", tweet_inp)
        tweet_inp = ind_regex.sub("ind", tweet_inp)
        tweet_inp = modi_regex.sub("pmoi", tweet_inp)
        
        for i in df.content : 
            sim = round(cosine_similarity([model_embedd.encode(tweet_inp)], [model_embedd.encode(i)])[0][0], 3)
            max_sim = max(max_sim, sim)
            if sim > 0.69 :
                flag = False
                break
            
        if flag :
            url = 'https://twitter.com/CheatcodesInc/status/' + str(j[1])
            st.write(str(max_sim*100))
            components.html(theTweet(url), height = 400 )
            
        
result(tweet_l)