from pydantic import BaseModel
from typing import Optional,List,Annotated

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage,AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START,END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver


from dotenv import load_dotenv
import os
from system_prompt import get_system_prompt



load_dotenv()

os.getenv("OPENAI_API_KEY")


# set up the state
class AgentState(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages]

# Initiate LLM
def initiate_llm(
        tools : Optional[List] = None,
        model : str = "gpt-4",
        temperature : float = 0.1
):
    tools=tools
    llm=ChatOpenAI(model=model,temperature=temperature).bind_tools(tools)
    return llm

# Build Agent and Graph

def build_agent(
    name: str,    
    llm : ChatOpenAI,
    tools : Optional[List] = None,
    system_prompt : str = get_system_prompt()
):
    """
    Build and compile StateGraph for the agent flow
    """
    tools=tools

    # define agent

    def agent_node(state: AgentState) -> AgentState:
        # Add system message if not already present
        messages = state.messages
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages
        
        response = llm.invoke(messages)
        return {"messages": [response]}
    
    # define router/ routing conditions  
    def router(state: AgentState) -> str:
        last_message = state.messages[-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        else:
            return END
        
    # building graph
    builder = StateGraph(AgentState)

    # adding nodes
    builder.add_node("Crstl", agent_node)
    builder.add_node("tools",ToolNode(tools))

    # adding edges
    builder.add_edge(START, "Crstl")
    builder.add_conditional_edges("Crstl", router)
    builder.add_edge("tools", "Crstl")


    # compiling the agent
    app=builder.compile(checkpointer=MemorySaver())
    graph=app
   
    return app, graph.get_graph().draw_mermaid_png()






    
