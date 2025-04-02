from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import json

from models import db, User, Assignment, Submission, TestCase, TestResult
from utils.code_evaluator import evaluate_code
from utils.plagiarism_detector import check_plagiarism
from utils.scoring_algorithm import calculate_score
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ensure UPLOAD_FOLDER exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) if user_id else None

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    assignments = Assignment.query.all()
    stats = {}
    
    if current_user.is_student:
        submissions = Submission.query.filter_by(user_id=current_user.id).all()
    else:
        submissions = Submission.query.all()
        students = User.query.filter_by(role='student').all()
        stats = {
            'total_students': len(students),
            'total_assignments': len(assignments),
            'total_submissions': len(submissions),
            'assignment_stats': []
        }
        
        for assignment in assignments:
            assignment_submissions = Submission.query.filter_by(assignment_id=assignment.id).all()
            avg_score = sum(sub.score for sub in assignment_submissions) / len(assignment_submissions) if assignment_submissions else 0
            stats['assignment_stats'].append({
                'id': assignment.id,
                'title': assignment.title,
                'submissions': len(assignment_submissions),
                'avg_score': avg_score
            })
    
    return render_template('dashboard.html', assignments=assignments, stats=stats, user=current_user)

@app.route('/submit/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
    if not current_user.is_student:
        flash('Only students can submit assignments', 'danger')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    if request.method == 'POST':
        code = request.form.get('code')
        
        if 'code_file' in request.files:
            file = request.files['code_file']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                with open(file_path, 'r') as f:
                    code = f.read()
        
        submission = Submission(
            user_id=current_user.id,
            assignment_id=assignment_id,
            code=code,
            submission_time=datetime.now()
        )
        db.session.add(submission)
        db.session.commit()
        
        test_cases = TestCase.query.filter_by(assignment_id=assignment_id).all()
        test_results = []
        
        for test_case in test_cases:
            result = evaluate_code(code, test_case.input_data, test_case.expected_output, assignment.language)
            test_result = TestResult(
                test_case_id=test_case.id,
                submission_id=submission.id,
                passed=result['passed'],
                output=result['output'],
                execution_time=result['execution_time']
            )
            test_results.append(test_result)
        
        other_submissions = Submission.query.filter(
            Submission.assignment_id == assignment_id,
            Submission.user_id != current_user.id
        ).all()
        
        plagiarism_results = []
        for other_sub in other_submissions:
            if other_sub.code:
                similarity = check_plagiarism(code, other_sub.code)
                if similarity > app.config['PLAGIARISM_THRESHOLD']:
                    plagiarism_results.append({'submission_id': other_sub.id, 'user_id': other_sub.user_id, 'similarity': similarity})
        
        submission.score = calculate_score(
            test_results=test_results,
            test_cases=test_cases,
            plagiarism_results=plagiarism_results,
            submission_time=submission.submission_time,
            due_date=assignment.due_date,
            max_score=assignment.max_score
        )
        
        db.session.add_all(test_results)
        db.session.commit()
        flash('Assignment submitted successfully', 'success')
        return redirect(url_for('submission_result', submission_id=submission.id))
    
    return render_template('submit.html', assignment=assignment)

if __name__ == '__main__':
    app.run(debug=True)