import streamlit as st
import chatbot_backend as chatbot
import speech_to_text as stt

INIT_MESSAGE = {
    "role": "assistant",
    "text": "Hi! I'm your AI Assistant. How may I help you?",
}

# st.title("Chatbot Assistant")
st.set_page_config(page_title="Chatbot Assistant")
st.markdown("<h1 style='text-align: center;'>Chatbot Assistant</h1>", unsafe_allow_html=True)
st.markdown("""
<style>
.st-emotion-cache-czk5ss.e16jpq800
{
            visibility: hidden;
}
.st-emotion-cache-ch5dnh.ef3psqc5
{
            visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

options = ["what is purpose of the document?",
           "how to close the emergency door in ramp mode?",
           "where is horn push button?",
           "what is TRS?"]

if 'memory' not in st.session_state:
    st.session_state.memory = chatbot.chat_memory()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [INIT_MESSAGE]

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])



def input_chat(input_text):
    with st.chat_message("user"):
        st.markdown(input_text)

    st.session_state.chat_history.append({"role":"user", "text":input_text})

    chat_response = chatbot.chat_conversation(input_text=input_text, memory=st.session_state.memory)

    with st.chat_message("assistant"):
        st.markdown(chat_response)

    st.session_state.chat_history.append({"role":"assistant", "text":chat_response})

input_text = st.chat_input("Your Message")
if input_text:
    input_chat(input_text)


def btn_click(input_text):
    input_chat(input_text)

# st.sidebar.subheader("Frequently Asked Questions")
st.sidebar.markdown("<h1 style='text-align: center;'>Frequently Asked Questions</h1>", unsafe_allow_html=True)

for faq in options:
    if st.sidebar.button(faq):
        btn_click(faq)

# st.sidebar.subheader("Voice to Text")
st.sidebar.markdown("<h1 style='text-align: center;'>Voice to Text</h1>", unsafe_allow_html=True)
mic_list = stt.get_mic_list()
select_mic = st.sidebar.selectbox("Choose your microphone", mic_list)
voiceinput = st.sidebar.button("Press to Speak")
if voiceinput:
    with st.spinner("Listening"):
        textRec = stt.recogStart(mic_list.index(select_mic))
    if textRec:
        input_chat(textRec)
