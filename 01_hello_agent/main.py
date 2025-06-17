import chainlit as cl
from dotenv import load_dotenv  # method/function
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel  # fixed spelling

def main():
    MODEL_NAME = "gemini-2.0-flash"
    load_dotenv()  # Load environment variables from .env file
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Create external client for Gemini API
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Initialize the OpenAIChatCompletionsModel with the external client
    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )

    # RunConfig setup (assuming you're using Agents SDK)
    config = RunConfig(
        model=model,
        # Add other config params here if needed
    )

    # Create an assistant (Agent must be imported properly)
    assistant = Agent(
        name="Assistant",
        instructions="Your job is to resolve queries",
        model=model
    )

    # Run the assistant
    result = Runner.run_sync(
        assistant,
        "Tell me something interesting about Pakistan",
        runconfig=config
    )
    print(result.final_output)

if __name__ == "__main__":
    main()
