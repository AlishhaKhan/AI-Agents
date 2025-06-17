from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Gemini API Key (correctly)
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup AsyncOpenAI-like provider with Gemini endpoint
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Setup model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

# Define run configuration
config = RunConfig(model=model)

# Define the agent with model
agent_one = Agent(
    name="Frontend Expert",
    instructions="You are a frontend expert who provides detailed, helpful, and accurate answers related to HTML, CSS, JS, React, and modern frontend development.",
    model=model
)

# Run the agent synchronously
result = Runner.run_sync(
    agent_one,
    input="What are the latest CSS features in 2025, give short answer?",
    run_config=config
)

# Print the final output
print(result.final_output)
