import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Database configuration class that handles MySQL connection parameters."""
    
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.port = int(os.getenv('MYSQL_PORT', '3306'))
        self.user = self._get_required_env('MYSQL_USER')
        self.password = self._get_required_env('MYSQL_PASSWORD')
        self.database = self._get_required_env('MYSQL_DATABASE')
        self.charset = os.getenv('MYSQL_CHARSET', 'utf8mb4')
        self.collation = os.getenv('MYSQL_COLLATION', 'utf8mb4_unicode_ci')
        self.sql_mode = os.getenv('MYSQL_SQL_MODE', 'TRADITIONAL')
        
        # Additional MySQL settings
        self.connect_timeout = int(os.getenv('MYSQL_CONNECT_TIMEOUT', '30'))
        self.autocommit = os.getenv('MYSQL_AUTOCOMMIT', 'True').lower() == 'true'
        self.use_ssl = os.getenv('MYSQL_USE_SSL', 'False').lower() == 'true'
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or raise ValueError if not set."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set. "
                           f"Please check your .env file or environment variables.")
        return value
    
    def to_env_dict(self) -> dict:
        """Convert configuration to environment variables dictionary for MCP client."""
        return {
            'MYSQL_HOST': self.host,
            'MYSQL_PORT': str(self.port),
            'MYSQL_USER': self.user,
            'MYSQL_PASSWORD': self.password,
            'MYSQL_DATABASE': self.database,
            'MYSQL_CHARSET': self.charset,
            'MYSQL_COLLATION': self.collation,
            'MYSQL_SQL_MODE': self.sql_mode,
            'MYSQL_CONNECT_TIMEOUT': str(self.connect_timeout),
            'MYSQL_AUTOCOMMIT': str(self.autocommit),
            'MYSQL_USE_SSL': str(self.use_ssl),
        }
    
    def get_connection_url(self) -> str:
        """Generate MySQL connection URL."""
        return f"mysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def validate(self) -> bool:
        """Validate configuration parameters."""
        try:
            assert 1 <= self.port <= 65535, f"Invalid port number: {self.port}"
            assert self.host, "Host cannot be empty"
            assert self.user, "User cannot be empty"
            assert self.database, "Database name cannot be empty"
            assert self.connect_timeout > 0, f"Invalid connect timeout: {self.connect_timeout}"
            return True
        except AssertionError as e:
            raise ValueError(f"Database configuration validation failed: {e}")

# Create global database configuration instance
db_config = DatabaseConfig()