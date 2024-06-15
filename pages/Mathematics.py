import streamlit as st
import pandas as pd
import numpy as np

st.markdown('''
	:red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
	:gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Here's a bouquet &mdash;\        	:tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

st.title("What is a coordinate system? :sparkles:")
st.video("https://www.youtube.com/watch?v=fNk_zzaMoSs", start_time=85, end_time=275, loop=False)

col1, col2 = st.columns(2)

with col1:
   st.header("Questions")
   st.image("https://www.annasayce.com/wp-content/uploads/2015/08/intellect-doubts.jpg")

with col2:
   st.header("Answered Questions")
   st.image("https://gifdb.com/images/high/spongebob-yay-meme-dance-38vs6bxghj2oye69.gif")


with st.container():
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))



