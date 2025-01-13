'''
This is the main streamlit app that fetches responses to users query of
a blog named Stuff You Look . 
Steps to run this app:
1. Maintain the dirctory structure files and folders in proper way
2. In Prompt (like Anaconda prompt) change directory to the working folder using cd "path to the folder of this script"
3. run "streamlit run main_app.py" in the prompt which will launch the app as localhost in browser
4. To stop the app use 'ctrl+C' to stop the running app

I suggest to create a new environment with the necessary libraries/packages using the requirement.txt provided in the folder.
For this (before running the main app)
1. create a new environment in prompt/terminal using "conda create -n your_env_name" for ex: "conda create -n syl_chatbot"
2. For Installing dependencies you need to navigate to the folder where the requirement text file is available using command
    cd "path_to_the folder_where_requrments_txt_file_is_present"
3. after cd, run "pip install -r requirements.txt" in the prompt/terminal
'''

# Importing the necessary libraries
import streamlit as st
from streamlit_chat import message
import streamlit.components.v1 as components
from PIL import Image

#Importing the python script that will fetch the responses
import llm_response as llm_script

# Creating a sidebar for the application
with st.sidebar:
    st.title("What is this App?")
    link = "https://stuffyoulook.blogspot.com/p/ceed-exam.html"
    st.write(f'<a href="{link}"> Stuff you look</a>', unsafe_allow_html=True)
    st.markdown("This is an AI (GPT) powered chatbot that can answer your design exam related queries. The responses are fetched from a blog named Stuff You Look (SYL).")
 # add_vertical_space(5)
    
    st.write(" ")

    col1, col2 = st.sidebar.columns([1,3])
    with col1: 
        st.write("from: ")
    with col2:
        image = Image.open('syl_logo.jpg') 
        st.image(image, width=100)
        
    #st.write(" ")
    st.write(" ")

# Defining the main function, which will have a dropdown list of questions for the user to select and also provides a search textbox at the bottom of the UI
def main():
    #Title of the App
    st.header("Design Exam chatbot")

    # Session_state are like cache memory to store some values/variables that might be needed in the later part of the code
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # Defining some predefined questions for the user to choose from
    predefined_ques=['','How to prepare and what to practice for CEED exam?',
                   'How to prepare and what to practice for UCEED exam?',
                   'How to prepare and what to practice for NID exam?',
                   'What are the priority topics for CEED exam preparation',
                   'What are the priority topics for UCEED exam preparation',
                   'What are the priority topics for NID exam preparation',
                   'Is coaching required for CEED and design exams?',
                   'What are the priority topics for last minute CEED'  ]
    #st.session_state.custom_question =""

    # creating two columns so that both the dropdown menu and the submit button are on the same line
    col1, col2 = st.columns([4.5,1])
    with col1:
        st.empty()
        user_input=st.selectbox("Choose a predefined question", predefined_ques)
    with col2: 
        st.write('')
        st.write('')
        submit=st.button("Submit")

    # Fetching response for the asked predefined qustion and storimg the question-response in session-state    
    if submit:
        with st.spinner("Please wait while I fetch the answer . . ."):
            st.session_state.past.append(user_input)
            app_reply = llm_script.generate_response(user_input)
            st.session_state.generated.append(app_reply)

    # Adding a textbox to the app for enabling user to write and ask custom questions
    col1, col2 = st.columns([4.5,1])
    custom_question = col1.text_input("Ask your custom question here...", key="custom_question", placeholder ="write and click submit button...")

    with col2:
        st.write('')
        st.write('')
        submit_button = col2.button("Submit", key="submit_button")

    # Fetching response for the asked custom question and storing the question-response in session-state
    if submit_button and custom_question:
        with st.spinner("Please wait while I fetch the answer . . ."):
            st.session_state.past.append(custom_question)
            app_reply = llm_script.generate_response(custom_question)
            st.session_state.generated.append(app_reply)

    # Displaying the question and responses of asked questions as a chat feature 
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user' + str(len(st.session_state['generated'])))
            message(st.session_state["generated"][i], key=str(i)+str(len(st.session_state['generated'])))

if __name__=="__main__":
    main()