import streamlit as st
import time
import os

# Title of the app
st.title('NBA Commentary generation from play-by-play data')

# Create a section for the video
st.header('Get ready from some AI generated commentary!')

# Add a video player with an iframe
iframe_code = '<iframe width="700" height="315" src="//ok.ru/videoembed/7207924992598" frameborder="0" allow="autoplay" allowfullscreen></iframe>'
st.markdown(iframe_code, unsafe_allow_html=True)

#Add an audio player
audio_file = open('music.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')

# Placeholder for the generated text
generated_text_placeholder = st.empty()




# Store the last modification time
if 'last_update' not in st.session_state:
    if os.path.exists('src/commentary.txt'):
        st.session_state['last_update'] = os.path.getmtime('src/commentary.txt')
    else:
        st.session_state['last_update'] = None

# Store the lines of text
if 'lines' not in st.session_state:
    st.session_state['lines'] = []

while True:
    # Check if the file has been updated
    current_update = os.path.getmtime('src/commentary.txt')
    if current_update != st.session_state['last_update']:
        with open('src/commentary.txt', 'r') as file:
            st.session_state['lines'] = file.readlines()
        st.session_state['last_update'] = current_update

    # Only keep the last 3 lines
    lines = st.session_state['lines'][-3:]
    # Use markdown to increase the size of the text
    generated_text_placeholder.markdown('\n'.join(f'<p style="font-size:20px">{line}</p>' for line in lines), unsafe_allow_html=True)
    time.sleep(0.1)