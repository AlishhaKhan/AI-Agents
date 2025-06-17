import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

agent = Agent(
    name="Greeting Agent",
    instructions="You are a greeting agent. Your task is to greet the user with a friendly message, when someone says hello or hi you've reply back with salam from Alisha Khan. If someone says bye then say Allah Hafiz from Alisha. And If someone talks beyond greetings, say: Alisha is here just for greetings.",
    model=model,
)

user_question = input("Please enter your question: ")

result = Runner.run_sync(agent, user_question)
print(result.final_output)    