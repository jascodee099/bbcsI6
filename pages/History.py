import streamlit as st
import pandas as pd
from PIL import Image
import io
import os

# Function to load existing questions and replies (if any)
def load_data():
    if not os.path.exists('questions.csv'):
        questions_df = pd.DataFrame(columns=['Question', 'Image', 'Votes'])
        questions_df.to_csv('questions.csv', index=False)
    else:
        questions_df = pd.read_csv('questions.csv')
        if 'Votes' not in questions_df.columns:
            questions_df['Votes'] = 0  # Add Votes column if it doesn't exist
    
    if not os.path.exists('replies.csv'):
        replies_df = pd.DataFrame(columns=['Question_ID', 'Reply'])
        replies_df.to_csv('replies.csv', index=False)
    else:
        replies_df = pd.read_csv('replies.csv')
    
    return questions_df, replies_df

# Function to save new question
def save_question(question, image):
    questions_df, _ = load_data()
    new_question = pd.DataFrame({'Question': [question], 'Image': [image], 'Votes': [0]})
    questions_df = pd.concat([questions_df, new_question], ignore_index=True)
    questions_df.to_csv('questions.csv', index=False)

# Function to save a reply
def save_reply(question_id, reply):
    _, replies_df = load_data()
    new_reply = pd.DataFrame({'Question_ID': [question_id], 'Reply': [reply]})
    replies_df = pd.concat([replies_df, new_reply], ignore_index=True)
    replies_df.to_csv('replies.csv', index=False)

# Function to save a vote
def save_vote(question_id):
    questions_df, _ = load_data()
    questions_df.at[question_id, 'Votes'] += 1
    questions_df.to_csv('questions.csv', index=False)

# Load existing questions and replies
questions_df, replies_df = load_data()

st.title("Anonymous Question Posting")

# Input fields for question and image
question = st.text_area("Ask your question here:")
image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

if st.button("Post Question"):
    if question:
        # Save image if uploaded
        if image:
            image_bytes = image.read()
            image_data = io.BytesIO(image_bytes)
            img = Image.open(image_data)
            if not os.path.exists('images'):
                os.makedirs('images')
            img.save(f"images/{image.name}")
            image_path = f"images/{image.name}"
        else:
            image_path = None

        # Save question
        save_question(question, image_path)
        st.success("Your question has been posted!")
        st.balloons()  # Display pop-up notification
    else:
        st.error("Please enter a question.")

# Initialize session state for stars
if 'starred' not in st.session_state:
    st.session_state.starred = [False] * len(questions_df)

# Display questions with tabs
st.subheader("Questions:")
tab1, tab2 = st.tabs(["All Questions", "Starred Questions"])

separator = '<hr style="border: none; height: 10px; background-color: #FFDAB9; margin: 20px 0;">'

with tab1:
    st.subheader("All Questions")
    questions_df = questions_df.sort_values(by='Votes', ascending=False).reset_index(drop=True)
    for index, row in questions_df.iterrows():
        st.write(separator, unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background-color: #E6F7FF; padding: 10px; border-radius: 5px;">
                <p><strong>Question {index + 1}:</strong> {row['Question']}</p>
            </div>
        """, unsafe_allow_html=True)
        if pd.notna(row['Image']):
            st.image(row['Image'])
        
        st.write(f"**Votes:** {row['Votes']}")

        # Display replies
        st.write("**Replies:**")
        question_replies = replies_df[replies_df['Question_ID'] == index]
        for _, reply_row in question_replies.iterrows():
            st.write(f"💡 {reply_row['Reply']}")

        new_reply = st.text_area(f"Your reply to Question {index + 1}:", key=f"reply_{index}")

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            if st.button(f"Post Reply to Question {index + 1}", key=f"reply_button_{index}"):
                if new_reply:
                    save_reply(index, new_reply)
                    st.success("Your reply has been posted!")
                    st.experimental_rerun()
                else:
                    st.error("Please enter a reply.")
        with col2:
            if st.button(f"Upvote {index + 1}", key=f"upvote_{index}"):
                save_vote(index)
                st.experimental_rerun()
        with col3:
            star_label = "⭐" if st.session_state.starred[index] else "☆"
            if st.button(star_label + f" Star {index + 1}", key=f"star_{index}"):
                st.session_state.starred[index] = not st.session_state.starred[index]
                st.experimental_rerun()

with tab2:
    st.subheader("Starred Questions")
    for index, starred in enumerate(st.session_state.starred):
        if starred:
            row = questions_df.iloc[index]
            st.write(separator, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background-color: #E6F7FF; padding: 10px; border-radius: 5px;">
                    <p><strong>Question {index + 1}:</strong> {row['Question']}</p>
                </div>
            """, unsafe_allow_html=True)
            if pd.notna(row['Image']):
                st.image(row['Image'])
            st.write(f"**Votes:** {row['Votes']}")

            # Display replies
            st.write("**Replies:**")
            question_replies = replies_df[replies_df['Question_ID'] == index]
            for _, reply_row in question_replies.iterrows():
                st.write(f"💡 {reply_row['Reply']}")

            new_reply = st.text_area(f"Your reply to Question {index + 1}:", key=f"reply_starred_{index}")

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                if st.button(f"Post Reply to Question {index + 1}", key=f"reply_button_starred_{index}"):
                    if new_reply:
                        save_reply(index, new_reply)
                        st.success("Your reply has been posted!")
                        st.experimental_rerun()
                    else:
                        st.error("Please enter a reply.")
            with col2:
                if st.button(f"Upvote {index + 1}", key=f"upvote_starred_{index}"):
                    save_vote(index)
                    st.experimental_rerun()
            with col3:
                star_label = "⭐" if st.session_state.starred[index] else "☆"
                if st.button(star_label + f" Unstar {index + 1}", key=f"unstar_{index}"):
                    st.session_state.starred[index] = not st.session_state.starred[index]
                    st.experimental_rerun()


#upload images
#balloon
#qn-ans 
##with votes
#w stars
#w tabs for starred and all
#w qn highlighted in pale blue
# 3 buttons all of the same level
#w orange bars


#python -m streamlit run main.py