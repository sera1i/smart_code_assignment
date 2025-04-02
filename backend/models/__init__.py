from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .assignment import Assignment
from .submission import Submission
from .test_case import TestCase
from .test_result import TestResult

__all__ = [
    'db',
    'User',
    'Assignment',
    'Submission',
    'TestCase',
    'TestResult'
]