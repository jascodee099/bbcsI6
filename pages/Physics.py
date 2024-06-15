import streamlit as st
import pandas as pd
import numpy as np

#cd Desktop


st.set_page_config(page_title="Jiaxin", page_icon="🔥", layout='wide')

st.title("AMA")

st.write("Hello, **Welcome!** :sparkles:")


#st.text_input(label, value="") #add chracter limits
title = st.text_input("Questions you have", value="Please type your questions here")

agree = st.checkbox("Hey there! Before you hit that post button, take a quick peek at the questions below. We've sorted them to help you find similar ones and avoid asking the same question again. Thanks! .")
if agree:
    st.markdown('''
	 :blue-background[Great!]:tulip:''')
    #st.write("Great!")


#selectbox
option = st.selectbox("Subject",
  ["Mathematics", "Physics", "Biology", "Chemistry", "Computing"])


# st.markdown("# Main page 🎈")
# st.sidebar.markdown("# Main page 🎈")
# st.markdown("# Page 2 ❄️")
# st.sidebar.markdown("# Page 2 ❄️")

#tabs
tab1, tab2 = st.tabs(["Questions", "Answered questions"])

with tab1:
   st.header("Questions")
st.image("https://www.annasayce.com/wp-content/uploads/2015/08/intellect-doubts.jpg", width=200)

with tab2:
   st.header("Answered questions")
st.image("https://gifdb.com/images/high/spongebob-yay-meme-dance-38vs6bxghj2oye69.gif", width=200)


#chat inout with send button
prompt = st.chat_input("Ask a question")
if prompt:
	st.write(f"Newest question: {prompt}")
    
#python -m streamlit run main.py

#add widgets slide 26

##help with setting up the page

my_list = [1, 2, 3]        # This is a list
my_tuple = (1, 2, 3)       # This is a tuple

x = 10
if x > 5:
    print("x is greater than 5")

#For example:
#if condition:
    # code to be executed if condition is true

#In this case, the message "x is greater than 5" will be printed because the condition x > 5 is true.


#for i in range(5):
    #print(i)
#In this example, the 'for' loop will print the numbers 0 through 4, one per line.