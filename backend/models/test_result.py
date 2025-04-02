from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from . import db

class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    test_case_id = Column(Integer, ForeignKey('test_cases.id'), nullable=False)
    passed = Column(Boolean, default=False)
    output = Column(Text, nullable=True)
    execution_time = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submission = relationship('Submission', backref='test_results')
    test_case = relationship('TestCase', backref='test_results')
    
    def __init__(self, submission_id, test_case_id, passed, output, execution_time):
        self.submission_id = submission_id
        self.test_case_id = test_case_id
        self.passed = passed
        self.output = output
        self.execution_time = execution_time
    
    def get_weighted_score(self):
        if self.passed:
            return self.test_case.weight
        return 0.0
    
    def get_performance_metric(self):
        if not self.passed:
            return 0.0
        
        if self.execution_time < 0.1:
            return 1.0
        
        return min(1.0, max(0.0, 1.0 - (self.execution_time - 0.1)))
    
    def __repr__(self):
        status = "Passed" if self.passed else "Failed"
        return f"<TestResult {self.id}: {status} (Test {self.test_case_id}, Submission {self.submission_id})>"