from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    assignments_created = db.relationship('Assignment', backref='creator', lazy='dynamic')
    submissions = db.relationship('Submission', backref='user', lazy='dynamic')
    
    def __init__(self, email, password_hash=None, first_name=None, last_name=None, role='student'):
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    @property
    def is_instructor(self):
        return self.role == 'instructor'
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_student_statistics(self):
        if not self.is_student:
            return None
            
        total_submissions = self.submissions.count()
        on_time_submissions = self.submissions.filter(
            Submission.submission_time <= Assignment.due_date
        ).join(Assignment).count()
        
        avg_score = 0
        if total_submissions > 0:
            scores_sum = sum(sub.score for sub in self.submissions)
            avg_score = scores_sum / total_submissions
            
        return {
            'total_submissions': total_submissions,
            'on_time_submissions': on_time_submissions,
            'late_submissions': total_submissions - on_time_submissions,
            'avg_score': avg_score
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'