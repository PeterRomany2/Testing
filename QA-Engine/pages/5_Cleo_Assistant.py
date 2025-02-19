import os
import re
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Set streamlit page configuration
st.set_page_config(layout="wide")

# Check if the user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to access this page.")
    st.stop()  # Stop further execution of the page

# Set up API Key for GROQ (load from config.json)

GROQ_API_KEY = "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"

# Set the API key as an environment variable for the session
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize the GROQ client
client = Groq()

# Set up model name
model = 'llama-3.3-70b-versatile'  # Update to your model of choice

# Embed Lottie animation in Streamlit with top-left positioning using inline CSS
lottie_html = """
<div style="text-align: center;">
<h1 style="color:#0FFF50;">AI Cleo Assistant<br>Your Way to Better Business Decisions</h1>
</div>
<div style="position: fixed; top: 0; right: 0;">
<script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script><lottie-player src="https://lottie.host/3e8ec22e-eb1b-4a61-8b78-5550fe0b94b8/AK7Vjkbjxk.json" background="##FFFFFF" speed="1" style="width: 300px; height: 300px" loop  autoplay direction="1" mode="normal"></lottie-player>
</div>
"""
components.html(lottie_html, height=250)


# Function to interact with the chat model via GROQ
def chat(message):
    user_message = [{
        'role': 'user',
        'content': fr"""
        use: df = pd.read_excel('Peter Assessment.xlsx', sheet_name='Escalation Sheet')
             df.drop(df[df['Total Order Amount'].isnull()].index,inplace=True)
             df.drop(df[df['Total Order Amount']=="visa"].index,inplace=True)
             mismatch_features = ['Total Order Amount']
             df[mismatch_features] = df[mismatch_features].astype(int)
             
and use: column names of this df:['Timestamp', 'Email Address', 'The Brand name', 'Complaint Type',
       'Gift/Exchange order number', 'Priorty', 'Channel', 'OLD Order Number',
       'Total Order Amount', 'Attach file', 'Comment about case',
       'Items with issue Blankie', 'Items with issue cleo',
       'Items with issue  Dermatique', 'Item with issue skin side',
       'Comment by Moderators', 'Back office name', 'Follow up date',
       'Feedback/ last update', 'Gift Order status', 'Ticket number',
       'Customer satisfaction', 'Whole case Status']
your task is: {message} (perform this task in python and show results in streamlit code with plotly)(write only the required code)
"""
    }]

    try:
        # Send the message to GROQ's chat model for completion
        response = client.chat.completions.create(
            model=model,  # Use the model specified
            messages=user_message
        )

        # Extract the response content from the model
        answer = response.choices[0].message.content
        return answer

    except Exception as e:
        st.error(f"Error with GROQ API: {e}")
        return None


# Function to execute the generated Python code
def execute_code(code):
    try:
        exec(code)

    except SyntaxError as e:
        st.write(f"Syntax error in the generated code: {str(e)}")
    except Exception as e:
        st.write(f"Error executing code: {str(e)}")


# Function to extract Python code from the model's response
def extract_python_code(response):
    match = re.search(r'```python(.*?)```', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


# Custom button style for Streamlit UI
st.markdown("""
    <style>
        .stButton>button {
            background-color: green;
            color: white;
        }
        .stButton>button:hover {
            background-color: darkgreen;
        }
    </style>
""", unsafe_allow_html=True)

# User input for asking questions
user_input = st.text_input("Ask your question:")
if st.button("Generate Answer"):
    if user_input:
        # Get the generated response from the model
        generated_response = chat(user_input)

        if generated_response:
            # Extract Python code from the response
            generated_code = extract_python_code(generated_response)

            if generated_code:
                with st.expander("Expand to view generated Python code"):
                    st.write(f"### Generated Python Code:\n```python\n{generated_code}\n```")

                # Execute the generated Python code
                execute_code(generated_code)

            else:
                st.write("Error: No valid Python code extracted from the response.")














# import ollama
# import re
# import streamlit as st
# import streamlit.components.v1 as components

# st.set_page_config(layout="wide")

# if "logged_in" not in st.session_state or not st.session_state.logged_in:
#     st.warning("You need to log in to access this page.")
#     st.stop()  # Stop further execution of the page









# model = 'llama3.1'

# # Embed Lottie animation in Streamlit with top-left positioning using inline CSS
# lottie_html = """

# <div style="text-align: center;">
# <h1 style="color:#0FFF50;">AI Cleo Assistant<br>Your Way to Better Business Decisions</h1>
# </div>
# <div style="position: fixed; top: 0; right: 0;">
# <script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script><lottie-player src="https://lottie.host/3e8ec22e-eb1b-4a61-8b78-5550fe0b94b8/AK7Vjkbjxk.json" background="##FFFFFF" speed="1" style="width: 300px; height: 300px" loop  autoplay direction="1" mode="normal"></lottie-player>
# </div>
# """
# # <div style="position: fixed; bottom: 0; left: 0;">
# # <script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script><lottie-player src="https://lottie.host/a0ebc27b-5ef0-4da2-8ff3-d04dbc033263/W7H2wmEBC3.json" background="##FFFFFF" speed="1" style="width: 300px; height: 300px" loop  autoplay direction="1" mode="normal"></lottie-player>
# # </div>
# components.html(lottie_html, height=250)


# def chat(message):

#     user_message = [{
#         'role': 'user',
#         'content': fr"""
#         use: df = pd.read_csv(r"C:\Users\beter\PycharmProjects\QA-Engine\Cleo_Data.csv")
# and use: column names of this df:['DATE', 'SALES', 'ORDERS', 'CUSTOMER_REVIEWS']
# your task is: {message} (perform this task in python and show results in streamlit code with plotly)(write only the required code)
# """
#     }]

#     response = ollama.chat(model=model, messages=[user_message[0]])
#     answer = response['message']['content']
#     return answer


# def execute_code(code):
#     try:
#         exec(code)

#     except SyntaxError as e:
#         st.write(f"Syntax error in the generated code: {str(e)}")
#     except Exception as e:
#         st.write(f"Error executing code: {str(e)}")


# def extract_python_code(response):
#     match = re.search(r'```python(.*?)```', response, re.DOTALL)
#     if match:
#         return match.group(1).strip()
#     return None


# st.markdown("""
#     <style>
#         .stButton>button {
#             background-color: green;
#             color: white;
#         }
#         .stButton>button:hover {
#             background-color: darkgreen;
#         }
#     </style>
# """, unsafe_allow_html=True)

# user_input = st.text_input("Ask your question:")
# if st.button("Generate Answer"):
#     if user_input:
#         generated_response = chat(user_input)

#         generated_code = extract_python_code(generated_response)

#         if generated_code:
#             with st.expander("Expand to view generated Python code"):

#                 st.write(f"### Generated Python Code:\n```python\n{generated_code}\n```")

#             execute_code(generated_code)

#         else:
#             st.write("Error: No valid Python code extracted from the response.")
