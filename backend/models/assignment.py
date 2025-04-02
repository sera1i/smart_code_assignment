from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from . import db

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    language = Column(String(20), nullable=False)
    max_score = Column(Float, default=100.0)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationship to User (Backref already defined in User model, so no need to redefine here)
    test_cases = relationship('TestCase', backref='assignment', cascade='all, delete-orphan')
    submissions = relationship('Submission', backref='assignment', cascade='all, delete-orphan')
    
    def __init__(self, title, description, due_date, language, max_score, created_by):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.language = language
        self.max_score = max_score
        self.created_by = created_by
    
    def get_test_cases(self):
        return self.test_cases
    
    def get_submissions(self, user_id=None):
        if user_id:
            return [s for s in self.submissions if s.user_id == user_id]
        return self.submissions
    
    def get_submission_stats(self):
        submissions = self.submissions
        total = len(submissions)
        
        if total == 0:
            return {
                'total': 0,
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'on_time_submissions': 0,
                'late_submissions': 0
            }
        
        scores = [s.score for s in submissions]
        on_time = [s for s in submissions if s.submission_time <= self.due_date]
        
        return {
            'total': total,
            'average_score': sum(scores) / total if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'lowest_score': min(scores) if scores else 0,
            'on_time_submissions': len(on_time),
            'late_submissions': total - len(on_time)
        }
    
    def is_past_due(self):
        return datetime.utcnow() > self.due_date
    
    def __repr__(self):
        return f"<Assignment {self.id}: {self.title}>"
