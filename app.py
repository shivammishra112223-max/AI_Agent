from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from datetime import datetime
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
import os
import requests
from langgraph.checkpoint.memory import InMemorySaver

# Define Agent Goal
# Choose LLM
# Create System Prompt
# Create Tools
# Connect APIs
# Create Agent
# Tool Calling
# Decision Making
# Memory / State
# Agent Workflow
# Error Handling
# Testing
# UI / Backend Integration
# Deployment
# Monitoring & Logging


load_dotenv()

memory = InMemorySaver()



llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# Add tool 

# 1 calculator tool
@tool
def Calculator(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# 2 date time tool
@tool
def Date_time() -> str:
    """ current data time """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3 Web search
Search_tool = TavilySearchResults(max_results=3)


# 4Train tool


@tool
def train_info(train_number: int) -> str:
    """Get train details."""

    try:
        api_key = os.getenv("QRAIL_API_KEY")

        if not api_key:
            return "QRAIL_API_KEY missing."

        url = "https://api.qrail.in/api/v1/trains/details"

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={"train": train_number},
            timeout=10
        )

        response.raise_for_status()

        return response.text

    except requests.exceptions.RequestException as e:
        return f"Train API error: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"


tools=[Calculator,Date_time,Search_tool,train_info]

# Agent Execute.Agent ko actual question par run/execute karne ke liye Agent Executor banate hain.

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful AI Agent. Use tools when needed.",
    checkpointer=memory
)

questions = [
    "10 + 20 kitna hai?",
    
]

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

for question in questions:
    
    try:


     response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
          config
          )
     print("\nUser:", question)
     print("Agent:", response["messages"][-1].content)



    except Exception as e:
        print("Agent error",e)