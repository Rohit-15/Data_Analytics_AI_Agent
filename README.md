# Data_Analytics_AI_Agent

An AI-powered data analytics agent built with LangGraph framework that interfaces with MySQL databases to provide intelligent data analysis and insights. The agent specializes in querying electricity and gas consumption data, client information, and pricing analytics through natural language interactions.

## 🏗️ Architecture Overview
![Application Architecture](https://github.com/Rohit-15/Data_Analytics_AI_Agent/blob/main/ai_agent_architecture.png)


### Communication Flow

![Communication Flow](https://github.com/Rohit-15/Data_Analytics_AI_Agent/blob/main/communication_flow.png)


## 🚀 Features

- **Natural Language to SQL**: Convert user questions into optimized SQL queries
- **Dual Response Format**: Provides both plain English explanations and structured pandas DataFrames
- **Memory Management**: Maintains conversation context using LangGraph's MemorySaver
- **Error Handling**: Robust error handling with detailed logging
- **Database Schema Awareness**: Deep understanding of client_data and price_data tables
- **MCP Integration**: Uses Model Context Protocol for secure database connections
- **Asynchronous Processing**: Built for high-performance concurrent operations

## 🔧 Key Components

### Agent (agent.py)
- **AgentState**: Pydantic model for state management
- **initiate_llm()**: LLM initialization with tool binding
- **build_agent()**: StateGraph construction and compilation
- **Router Logic**: Conditional edge routing between nodes

### Main Handler (main.py)
- **Async Processing**: `invoke_graph_response()` for graph execution
- **MCP Integration**: MySQL server connection and tool retrieval
- **Error Handling**: Comprehensive exception management

### System Prompt (system_prompt.py)
- **Role Definition**: "Crstl" AI data analyst persona
- **Schema Documentation**: Detailed table and column descriptions
- **Response Format**: Guidelines for dual-format responses
- **Best Practices**: SQL query optimization and data handling

### Configuration
- **Database Config**: Environment-based MySQL connection settings
- **Logging Config**: Structured logging with file and console handlers
- **Memory Management**: Thread-based conversation persistence

## 📊 Response Format

Every query receives two types of responses:

1. **Plain English Explanation**
   - Business insights and interpretations
   - Trend analysis and patterns
   - Actionable recommendations

2. **Structured DataFrame**
   - Clean, organized tabular data
   - Proper column names and data types
   - Summary statistics when relevant
  
## 🧪 To Do

1) **Write comprehensive test scripts**


2) **Build an MCP server with data visualization tools**

3) **Explore multi-agent framework integration**
