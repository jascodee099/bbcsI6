# Jiaxin & Kristine combined

import pandas as pd
from PIL import Image
import io
import os
import streamlit as st

# Function to load existing questions and replies (if any)
def load_data():
    if not os.path.exists('questions.csv'):
        questions_df = pd.DataFrame(columns=['Question', 'Image', 'Topic', 'Votes'])
        questions_df.to_csv('questions.csv', index=False)
    else:
        questions_df = pd.read_csv('questions.csv')
        if 'Votes' not in questions_df.columns:
            questions_df['Votes'] = 0  # Add Votes column if it doesn't exist
            questions_df.to_csv('questions.csv', index=False)

    if not os.path.exists('replies.csv'):
        replies_df = pd.DataFrame(columns=['Question_ID', 'Reply', 'Image', 'Video'])
        replies_df.to_csv('replies.csv', index=False)
    else:
        replies_df = pd.read_csv('replies.csv')

    return questions_df, replies_df

# Function to save new question
def save_question(question, image, topic):
    questions_df, _ = load_data()
    new_question = pd.DataFrame({'Question': [question], 'Image': [image], 'Topic': [topic], 'Votes': [0]})
    questions_df = pd.concat([questions_df, new_question], ignore_index=True)
    questions_df.to_csv('questions.csv', index=False)

# Function to save a reply
def save_reply(question_id, reply='-', image=None, video=None):
    _, replies_df = load_data()

    if image is not None:
        image_bytes = image.read()
        image_data = io.BytesIO(image_bytes)
        img = Image.open(image_data)
        if not os.path.exists('reply_images'):
            os.makedirs('reply_images')
        img.save(f"reply_images/{image.name}")
        image_path = f"reply_images/{image.name}"
    else:
        image_path = None

    if video is not None:
        video_bytes = video.read()
        if not os.path.exists('reply_videos'):
            os.makedirs('reply_videos')
        with open(f"reply_videos/{video.name}", 'wb') as f:
            f.write(video_bytes)
        video_path = f"reply_videos/{video.name}"
    else:
        video_path = None

    new_reply = pd.DataFrame({'Question_ID': [question_id], 'Reply': [reply], 'Image': [image_path], 'Video': [video_path]})
    replies_df = pd.concat([replies_df, new_reply], ignore_index=True)
    replies_df.to_csv('replies.csv', index=False)

# Function to save a vote
def save_vote(question_id):
    questions_df, _ = load_data()
    questions_df.at[question_id, 'Votes'] += 1
    questions_df.to_csv('questions.csv', index=False)

# Load existing questions and replies
questions_df, replies_df = load_data()

# Initialize session state
if 'show_confirm_question' not in st.session_state:
    st.session_state.show_confirm_question = False

if 'show_confirm_response' not in st.session_state:
    st.session_state.show_confirm_response = [False] * len(questions_df)

if 'popup_message' not in st.session_state:
    st.session_state.popup_message = ""

# Function to filter questions based on topic and keyword
def filter_questions(questions_df, topic_filter, keyword_filter):
    if topic_filter != "All Topics":
        questions_df = questions_df[questions_df['Topic'] == topic_filter]
    if keyword_filter:
        questions_df = questions_df[questions_df['Question'].str.contains(keyword_filter, case=False, na=False)]
    return questions_df

# Function to display a popup message
def show_popup(message):
    st.session_state.popup_message = message
    st.experimental_rerun()

st.title("Anonymous Question Posting")

# Create a container for the filters
with st.container():
    st.markdown('<div class="section-border">', unsafe_allow_html=True)
    st.write("### Filters")
    # Create a row for the filters
    col1, col2 = st.columns([1, 2])

    # Topic filter
    with col1:
        topic_filter = st.selectbox('Filter by Topic', ["All Topics"] + [f'Topic {i}' for i in range(1, 11)])

    # Keyword filter
    with col2:
        keyword_filter = st.text_input('Filter by Keyword')

    # Filter button
    if st.button('Apply Filters'):
        st.session_state.filtered_questions = filter_questions(questions_df, topic_filter, keyword_filter)
    else:
        st.session_state.filtered_questions = questions_df

    # Display the selected filters
    st.write(f'**Selected Topic for Filter:** {topic_filter}')
    st.write(f'**Entered Keyword for Filter:** {keyword_filter}')
    st.markdown('</div>', unsafe_allow_html=True)

separator = '<hr style="border: none; height: 10px; background-color: #FFDAB9; margin: 20px 0;">'

# Input fields for question and image
question = st.text_area("Ask your question here:")
image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
topic_selection = st.selectbox('Select Topic for Question', [f'Topic {i}' for i in range(1, 11)])

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
        save_question(question, image_path, topic_selection)
        st.success("Your question has been posted!")
        st.balloons()  # Display pop-up notification
    else:
        st.error("Please enter a question before submitting.")

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

        st.write(f"**Topic:** {row['Topic']}")
        if pd.notna(row['Image']):
            st.image(row['Image'])

        st.write(f"**Votes:** {row['Votes']}")

        # Display replies
        st.write("**Replies:**")
        question_replies = replies_df[replies_df['Question_ID'] == index]
        for _, reply_row in question_replies.iterrows():
            st.write(f"💡 {reply_row['Reply']}")
            if pd.notna(reply_row['Image']):
                st.image(reply_row['Image'])
            if pd.notna(reply_row['Video']):
                st.video(reply_row['Video'])

        new_reply = st.text_area(f"Your reply to Question {index + 1}:", key=f"reply_{index}")
        new_reply_image = st.file_uploader(f"Upload an image for Question {index + 1} (optional)", type=["jpg", "jpeg", "png"], key=f"image_{index}")
        new_reply_video = st.file_uploader(f"Upload a video for Question {index + 1} (optional)", type=["mp4", "avi", "mov"], key=f"video_{index}")

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            if st.button(f"Post Reply to Question {index + 1}", key=f"reply_button_{index}"):
                if new_reply or new_reply_image or new_reply_video:
                    save_reply(index, new_reply, new_reply_image, new_reply_video)
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

            st.write(f"**Topic:** {row['Topic']}")
            if pd.notna(row['Image']):
                st.image(row['Image'])
            st.write(f"**Votes:** {row['Votes']}")

            # Display replies
            st.write("**Replies:**")
            question_replies = replies_df[replies_df['Question_ID'] == index]
            for _, reply_row in question_replies.iterrows():
                st.write(f"💡 {reply_row['Reply']}")
                if pd.notna(reply_row['Image']):
                    st.image(reply_row['Image'])
                if pd.notna(reply_row['Video']):
                    st.video(reply_row['Video'])

            new_reply = st.text_area(f"Your reply to Question {index + 1}:", key=f"reply_starred_{index}")
            new_reply_image = st.file_uploader(f"Upload an image for Question {index + 1} (optional)", type=["jpg", "jpeg", "png"], key=f"image_starred_{index}")
            new_reply_video = st.file_uploader(f"Upload a video for Question {index + 1} (optional)", type=["mp4", "avi", "mov"], key=f"video_starred_{index}")

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                if st.button(f"Post Reply to Question {index + 1}", key=f"reply_button_starred_{index}"):
                    if new_reply or new_reply_image or new_reply_video:
                        save_reply(index, new_reply, new_reply_image, new_reply_video)
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


#jx & kristine combined but star function doesnt work (unless dont refresh)

#python -m streamlit run main.py
#boby ps is 69