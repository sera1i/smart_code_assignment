# Smart Code Assignment Evaluator

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/Flask-2.0%2B-blue)](https://flask.palletsprojects.com/)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Instructor Workflow](#instructor-workflow)
  - [Student Workflow](#student-workflow)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Smart Code Assignment Evaluator is an intelligent system designed to streamline the evaluation of programming assignments. It automates code assessment, detects plagiarism, and provides detailed feedback to students. The platform supports multiple programming languages and offers comprehensive analytics for instructors to track student performance.

## Features
- **Automated Code Evaluation**: Run submissions against predefined test cases to ensure correctness.
- **Plagiarism Detection**: Advanced algorithms to detect code similarities and maintain academic integrity.
- **Performance Analytics**: Detailed metrics on code quality, efficiency, and execution time.
- **Role-Based Access**: Separate dashboards and functionalities for instructors and students.
- **Early Submission Rewards**: Bonus scoring for submissions made before the deadline.
- **Late Submission Penalties**: Automated penalties for late submissions.
- **Code Quality Assessment**: Evaluate code readability, complexity, and documentation.
- **User-Friendly Interface**: Intuitive dashboards for both instructors and students.

## Technology Stack
- **Backend**: Python with Flask
- **Database**: SQLAlchemy (SQLite for development, PostgreSQL for production)
- **Frontend**: HTML, CSS, Bootstrap 5
- **JavaScript**: Chart.js for data visualization
- **Authentication**: Flask-Login for user management
- **Configuration Management**: Environment variables for sensitive data

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for frontend dependencies)
- Git
- Virtual environment manager (e.g., `venv`)

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/smart-code-assignment-evaluator.git
   cd smart-code-assignment-evaluator
