import logging
import logging.config
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Set up logging configuration for the AI Agent application.
    
    Args:
        log_level: Logging level (default: INFO)
        log_file: Log file path (default: logs/ai_agent.log)
    """
    if log_file is None:
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'ai_agent.log')
    
    # Logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '[%(asctime)s] %(levelname)-8s %(name)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'level': log_level,
                'formatter': 'detailed',
                'filename': log_file,
                'mode': 'a',
                'encoding': 'utf-8'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': logging.WARNING,  # Only show warnings and errors on console
                'formatter': 'simple'
            }
        },
        'loggers': {
            'ai_agent': {
                'handlers': ['file', 'console'],
                'level': log_level,
                'propagate': False
            }
        },
        'root': {
            'handlers': ['file'],
            'level': log_level
        }
    }
    
    logging.config.dictConfig(logging_config)
    return logging.getLogger('ai_agent')

def get_logger(name=None):
    """Get a logger instance for the AI Agent application."""
    if name:
        return logging.getLogger(f'ai_agent.{name}')
    return logging.getLogger('ai_agent')