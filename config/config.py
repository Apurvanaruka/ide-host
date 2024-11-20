class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add your database connection string here
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # For SQLite, change for PostgreSQL or others
    # Other configuration values like API keys, debug settings, etc.

class DevelopmentConfig(Config):
    DEBUG = True
    # Development specific settings

class ProductionConfig(Config):
    DEBUG = False
    # Production specific settings

class TestingConfig(Config):
    TESTING = True
    # Test-specific settings
