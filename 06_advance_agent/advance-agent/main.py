import os
import chainlit as cl
from dotenv import load_dotenv
from typing import Optional, Dict
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Correct model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # Make sure this name is supported by the backend
    openai_client=provider
)

@function_tool("get_weather")
def get_weather(Location: str, unit: str = "C") -> str:
    return f"The weather in {Location} is 22 degree {unit}"

agent = Agent(
    name="Greeting Agent",
    instructions="You are a greeting agent. Your task is to greet the user with a friendly message. When someone says hello or hi, you reply back with 'Salam from Alisha Khan'. If someone says bye, then say 'Allah Hafiz from Alisha'. If someone talks beyond greetings, say: 'Alisha is here just for greetings.'",
    model=model,
    tools=[get_weather]
)

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

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Hello! I'm your Gemini-powered assistant. How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})

    try:
        # ✅ Use the agent with Runner.run_sync (correct way)
        result = await cl.make_async(Runner.run_sync)(agent, input=message.content)
        response_text = result.final_output

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
        return

    await cl.Message(content=response_text).send()

    # Save response in session history
    history.append({"role": "model", "content": response_text})
    cl.user_session.set("history", history)
