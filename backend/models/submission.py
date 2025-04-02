from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from . import db

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    code = Column(Text, nullable=False)
    submission_time = Column(DateTime, default=datetime.utcnow)
    score = Column(Float, default=0.0)
    feedback = Column(Text, nullable=True)
    is_graded = Column(Boolean, default=False)
    
    test_results = relationship('TestResult', backref='submission', cascade='all, delete-orphan')
    
    def __init__(self, user_id, assignment_id, code, submission_time=None, score=0.0, feedback=None):
        self.user_id = user_id
        self.assignment_id = assignment_id
        self.code = code
        self.submission_time = submission_time or datetime.utcnow()
        self.score = score
        self.feedback = feedback
        self.is_graded = False
    
    def is_on_time(self):
        from .assignment import Assignment
        assignment = Assignment.query.get(self.assignment_id)
        return self.submission_time <= assignment.due_date
    
    def days_late(self):
        from .assignment import Assignment
        assignment = Assignment.query.get(self.assignment_id)
        
        if self.submission_time <= assignment.due_date:
            return 0
        
        delta = self.submission_time - assignment.due_date
        return delta.total_seconds() / (24 * 60 * 60)
    
    def get_passed_test_cases(self):
        return [result for result in self.test_results if result.passed]
    
    def get_failed_test_cases(self):
        return [result for result in self.test_results if not result.passed]
    
    def get_test_case_pass_rate(self):
        total_tests = len(self.test_results)
        if total_tests == 0:
            return 0
        
        passed_tests = len(self.get_passed_test_cases())
        return (passed_tests / total_tests) * 100
    
    def get_plagiarism_score(self, threshold=0.75):
        return {
            'max_similarity': 0.0,
            'similar_submissions': [],
            'is_plagiarized': False,
        }
    
    def update_score(self, new_score, feedback=None):
        self.score = new_score
        if feedback:
            self.feedback = feedback
        self.is_graded = True
        db.session.commit()
    
    def __repr__(self):
        return f"<Submission {self.id}: User {self.user_id}, Assignment {self.assignment_id}>"