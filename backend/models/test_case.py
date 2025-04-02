from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from . import db

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    input_data = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False)
    weight = Column(Float, default=1.0)
    description = Column(String(200), nullable=True)
    execution_timeout = Column(Integer, default=5)
    
    test_results = relationship('TestResult', backref='test_case', cascade='all, delete-orphan')
    
    def __init__(self, assignment_id, input_data, expected_output, weight=1.0, is_hidden=False, description=None, execution_timeout=5):
        self.assignment_id = assignment_id
        self.input_data = input_data
        self.expected_output = expected_output
        self.weight = weight
        self.is_hidden = is_hidden
        self.description = description
        self.execution_timeout = execution_timeout
    
    def get_results_for_submission(self, submission_id):
        for result in self.test_results:
            if result.submission_id == submission_id:
                return result
        return None
    
    def get_passing_rate(self):
        if not self.test_results:
            return 0.0
        
        passed = sum(1 for result in self.test_results if result.passed)
        return (passed / len(self.test_results)) * 100
    
    def get_average_execution_time(self):
        if not self.test_results:
            return 0.0
        
        times = [result.execution_time for result in self.test_results]
        return sum(times) / len(times)
    
    def to_dict(self, include_hidden=False):
        data = {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'weight': self.weight,
            'description': self.description
        }
        
        if include_hidden or not self.is_hidden:
            data.update({
                'input_data': self.input_data,
                'expected_output': self.expected_output
            })
        
        return data
    
    def __repr__(self):
        return f"<TestCase {self.id} for Assignment {self.assignment_id}>"