# AI Agent Logging Configuration

## Overview
The AI Agent project now uses structured logging to track operations, successes, and failures instead of printing to console.

## Log File Location
- **Default location**: `logs/ai_agent.log`
- The logs directory is created automatically if it doesn't exist

## Logging Levels
- **INFO**: Success confirmations, operation status, general information
- **ERROR**: Failures, exceptions, configuration issues
- **WARNING**: Important notices (shown on console too)

## Console Output
- The main.py script now only shows:
  - MCP server connection status
  - Available tools and resources (simplified view)
  - Basic error messages with reference to check log file
- Detailed information is logged to the file

## Log Format
```
[YYYY-MM-DD HH:MM:SS] LEVEL    logger_name - message
```

Example:
```
[2025-08-30 16:29:04] INFO     ai_agent - Connected successfully. Available tools: ['query', 'schema']
[2025-08-30 16:29:05] ERROR    ai_agent - Connection error: Server timeout
```

## Usage in Code
```python
from config.logging import setup_logging, get_logger

# Set up logging (usually done once in main)
logger = setup_logging()

# Or get a specific logger
logger = get_logger('module_name')

# Log messages
logger.info("Operation completed successfully")
logger.error("Operation failed with error: {error}")
```

## Configuration
- Log level can be adjusted in `config/logging.py`
- Custom log file path can be specified when calling `setup_logging(log_file="custom_path.log")`
- Console output level is set to WARNING by default (only warnings and errors shown)