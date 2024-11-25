from dotenv import load_dotenv
load_dotenv()

# DEFINE TOOLS
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode

# SETUP PHASE: 
# we define our tools, which are functions that can be called by ToolNode and works well with it.
@tool
def get_weather(location: str):
    """Call to get current weather in a given location"""
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degree and foggy"
    else:
        return "It's 90 degrees and sunny"
    
@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return "nyc, sf"

# Then, we create a list of our tools to pass it to the ToolNode
tools = [get_weather, get_coolest_cities]
tool_node = ToolNode(tools)

# EXECUTION PHASE: MANUALLY CALL ToolNode
# Tell our ToolNode which tool to run and with what arguments
message_with_single_tool_call = AIMessage(
    content="",
    tool_calls = [{
        "name": "get_weather", # Which tool to run
        "args": {"location": "sf"}, #Arguments to pass to the tool
        "id": "tool_call_id1",
        "type": "tool_call"
    },
    {
        "name": "get_coolest_cities",
        "args": {},
        "id": "tool_call_id2"
    }
    ]
)

# INVOKE tools and get THE TOOLS RETURNS RESULTS 
a = tool_node.invoke({
    "messages": [message_with_single_tool_call]
})

print("------------")
print("------------")
print(a)



# USING WITH CHAT MODELS
from typing import Literal
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

model_with_tools = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0.0
)

# to use chat models with tool calling, we need to ensure that the llm model is aware of the available tools. 
# We do this by calling .bind_tools  method on the llm model.
model_with_tools.bind_tools(tools)

