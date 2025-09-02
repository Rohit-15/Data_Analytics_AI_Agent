import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StdioConnection
from config.database import db_config
from config.logging import setup_logging, get_logger
from agent import initiate_llm, build_agent, AgentState

from dotenv import load_dotenv
import os
from system_prompt import get_system_prompt
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

load_dotenv()

os.getenv("OPENAI_API_KEY")

async def invoke_graph_response(
        input: AgentState, graph, config: dict = {}
        ) -> str:
    """
    Invoke the graph and return the full response.

    Args:
        input: The input for the graph.
        graph: The compiled graph to run.
        config: The config to pass to the graph.

    Returns:
        The processed string from the graph's response.
    """
    try:
        result = await graph.ainvoke(
            input=input,
            config=config
        )
        
        
        messages = None
        if hasattr(result, 'messages'):
            messages = result.messages
        elif isinstance(result, dict) and 'messages' in result:
            messages = result['messages']
        
        if messages:
            # Look for the final AI response (after tool execution)
            for message in reversed(messages):
                # Check if this is an AI message with content
                if (hasattr(message, 'content') and 
                    message.content and 
                    message.content.strip() and
                    message.__class__.__name__ == 'AIMessage'):
                    # Skip messages that only have tool calls and no content
                    if hasattr(message, 'tool_calls') and message.tool_calls and not message.content.strip():
                        continue
                    return message.content
        
        return "No response generated from the agent."
        
    except Exception as e:
        return f"Error during graph execution: {str(e)}"



async def connect_and_list_mcp():
    """Connect to MySQL MCP server and list available tools."""
    
    # Set up logging
    logger = setup_logging()
    
    # Suppress MCP server startup messages from console
  
    import sys
    from contextlib import redirect_stderr
    from io import StringIO
    
    try:
        # Validate database configuration before proceeding
        db_config.validate()
        logger.info(f"Using database configuration: {db_config.host}:{db_config.port}/{db_config.database}")
   
        
    except ValueError as e:
        logger.error(f"Database configuration error: {e}")
    
        return
    
    # Create MCP client for MySQL server
    client = MultiServerMCPClient({
        "mysql": {
            "command": "mysql_mcp_server",
            "args": [],
            "transport": "stdio",
            "cwd": None,
            "encoding": "utf-8",
            "env": db_config.to_env_dict()
        }
    })
    
    try:
        logger.info("Connecting to MySQL MCP server...")
        
        # Suppress MCP server stderr output to keep user interface clean
        stderr_buffer = StringIO()
        
        # Try to connect to MCP server and get tools
        tools = []
        try:
            with redirect_stderr(stderr_buffer):
                tools = await client.get_tools(server_name="mysql")
            logger.info(f"Connected successfully. Available tools: {[tool.name for tool in tools]}")
        except Exception as mcp_error:
            logger.warning(f"MCP server connection failed: {mcp_error}")
            logger.warning("Cannot proceed without MCP tools")

        # Check if we got MCP tools
        if not tools:
            logger.error("No MCP tools available.")
            return
        
        logger.info(f"Initializing LLM with {len(tools)} MCP tools")
        llm = initiate_llm(model="gpt-4", tools=tools)
        agent, graph_png = build_agent("Crstl", llm, tools=tools, system_prompt=get_system_prompt())

        # creating a config thread to retain memory
        graph_config={
            "configurable": {
                "thread_id": "1"
            }
        }

        print("\n" + "="*50)
        print("AI Agent Ready! Type quit or exit or bye or stop to stop.")
        print("="*50)

        while True:
            try:
                user_input = input("\n\nUSER: ")
                if user_input.lower() in ["quit", "exit", "bye", "stop"]:
                    break

                # Log the user input for debugging
                logger.info(f"User query: {user_input}")

                # Create initial state with user message
                initial_state = AgentState(messages=[HumanMessage(content=user_input)])
                
                response = await invoke_graph_response(
                    input=initial_state,
                    graph=agent, 
                    config=graph_config
                )
                
                # Log the response for debugging
                logger.info(f"Agent response: {response}")
                
                # Only show the clean answer to the user
                print(f"\n{response}\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nExiting...")
                break
       
        
        # Log detailed information about tools
        if tools:
            logger.info("Available tools details:")
         
            for tool in tools:
                logger.info(f"Tool: {tool.name}")
           
                if hasattr(tool, 'description') and tool.description:
                    logger.info(f"  Description: {tool.description}")
            
                if hasattr(tool, 'parameters'):
                    logger.info(f"  Parameters: {tool.parameters}")
             
        
        # Log connection summary
        logger.info(f"MCP Server Connection Complete - Tools: {len(tools)}, Status: SUCCESS")
      
            
    except Exception as e:
        logger.error(f"Connection error: {e}")
        logger.error("Troubleshooting tips logged - check mysql_mcp_server installation, process startup, client configuration")
      
    finally:
        # Close MCP client connection
        try:
            if 'client' in locals():
                # MCP client cleanup is handled automatically
                logger.info("MCP client cleanup completed")
        except Exception as e:
            logger.warning(f"Error during MCP client cleanup: {e}")
        
        logger.info("MCP client operations completed")

if __name__ == "__main__":
    asyncio.run(connect_and_list_mcp())