import os
from typing import Optional, Dict

import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# OAuth callback (if you're using GitHub/Google login)
@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: Optional[str],
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    print(f"Provider: {provider_id}")
    print(f"User Data: {raw_user_data}")
    return default_user

# Run when chat starts
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Hello! I'm your Gemini-powered assistant. How can I help you today?").send()

# Run when a message is sent by the user
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history", [])

    # Add user's message to memory
    history.append({"role": "user", "content": message.content})

    # Format history for Gemini API
    formatted_history = [
        {"role": msg["role"], "parts": [{"text": msg["content"]}]}
        for msg in history
    ]

    try:
        # Show typing indicator
        await cl.Message(content="💬 Thinking...").send()

        # Get Gemini's response
        response = model.generate_content(formatted_history)
        response_text = response.text.strip() if hasattr(response, "text") else "⚠️ No response received."

        # Save assistant's response to memory
        history.append({"role": "model", "content": response_text})
        cl.user_session.set("history", history)

        # Send response to user
        await cl.Message(content=response_text).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
