import os    # to get values of environment variables
import chainlit as cl  # to create a chatbot interface
import google.generativeai as genai  # to interact with Gemini API
from dotenv import load_dotenv  # to load environment variables from a .env file

load_dotenv()  # load environment variables from .env file

gemini_api_key = os.getenv("GEMINI_API_KEY")  # get the Gemini API key from environment variables

genai.configure(api_key=gemini_api_key)  # configure the Gemini API with the API key

model = genai.GenerativeModel(
   model_name="gemini-2.0-flash"
)                                    # create a model instance for Gemini 2.0 Flash

@cl.on_chat_start                   # decorator to handle the start of a chat session
async def handle_chart_start():
   await cl.Message(content="Hello! I am a Q&A chatbot powered by Gemini 2.0 Flash. How can I assist you today?").send()
   
@cl.on_message                        # decorator to handle incoming messages
async def handle_message(message: cl.Message):
   
   prompt = message.content            # get the content of the incoming message
   
   response = model.generate_content(prompt)      # generate a response using the Gemini model
   
   response_text = response.text if hasattr(response, 'text') else ""      # extract the text from the response object
   
   await cl.Message(content=response_text).send()     # send the response back to the chat interface