from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    name="code_agent",
    model="gemini-3.5-flash",
    description="An assistant that solves problems by writing and running Python code.",
    instruction="""
    You are a precise problem solver.
    For anything involving calculations, counting, dates, or data, write Python code and run it
    instead of answering from memory. Check your result, then explain the answer in plain language.
    """,
    # Lets Gemini write Python, run it in Google's sandbox, and use the real output.
    code_executor=BuiltInCodeExecutor(),
)
