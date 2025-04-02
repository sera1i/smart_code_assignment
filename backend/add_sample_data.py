import os
from datetime import timedelta

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///smart_code_evaluator.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'c', 'cpp', 'h', 'hpp', 'py', 'java', 'js'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Code evaluation configuration
    EXECUTION_TIMEOUT = 5  # Maximum code execution time in seconds
    MAX_MEMORY_MB = 100  # Maximum memory usage in MB
    SANDBOX_ENABLED = True  # Enable sandboxed execution
    
    # Plagiarism detection configuration
    PLAGIARISM_THRESHOLD = 0.75  # Similarity threshold (0-1) to flag as potential plagiarism
    MIN_TOKEN_LENGTH = 3  # Minimum token length for plagiarism detection
    
    # Scoring configuration
    EARLY_SUBMISSION_BONUS = 0.1  # 10% bonus for submissions before deadline
    EARLY_DAYS_THRESHOLD = 2  # Days before deadline to qualify for early submission bonus
    LATE_SUBMISSION_PENALTY = 0.2  # 20% penalty per day for late submissions
    MAX_LATE_DAYS = 5  # Maximum days late after which submissions are not accepted
    
    # Code quality metrics weights
    CODE_QUALITY_WEIGHT = {
        'readability': 0.3,
        'complexity': 0.3,
        'documentation': 0.2,
        'efficiency': 0.2
    }
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')
    
    # Email configuration for notifications
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@smartcodeevaluator.com'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SANDBOX_ENABLED = False  # Disable sandbox in development for easier debugging

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SANDBOX_ENABLED = False  # Disable sandbox in testing

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # In production, ensure these are set in environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Enable more secure settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

# Choose configuration based on environment
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}