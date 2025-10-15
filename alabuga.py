# vulnerable_app.py
import requests
import pickle
import subprocess
import os
import sys
from flask import Flask, request, render_template_string
import sqlite3
import json

app = Flask(__name__)

# 🔴 КРИТИЧЕСКИЕ УЯЗВИМОСТИ:

# 1. Hardcoded secrets
DATABASE_PASSWORD = "super_secret_123"
API_KEY = "sk_live_1234567890abcdef"
JWT_SECRET = "my_ultra_secret_jwt_key"

# 2. SQL Injection vulnerability
def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 🔴 SQL Injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

# 3. Command Injection
def run_system_command(cmd):
    # 🔴 Command Injection
    return subprocess.check_output(cmd, shell=True)

# 4. Insecure Deserialization
def load_user_data(data):
    # 🔴 Insecure deserialization
    return pickle.loads(data)

# 5. XSS Vulnerability
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # 🔴 XSS vulnerability
    return render_template_string(f"<h1>Search results for: {query}</h1>")

# 6. Insecure requests
def call_external_api(url, data):
    # 🔴 Disabled SSL verification
    response = requests.post(url, json=data, verify=False)
    
    # 🔴 Hardcoded credentials in request
    auth_response = requests.get(
        'https://api.example.com/data',
        auth=('admin', 'password123')
    )
    
    return response.text

# 7. Insecure file operations
def read_sensitive_file(filename):
    # 🔴 Path traversal potential
    with open(filename, 'r') as f:
        return f.read()

# 8. Weak cryptography
import hashlib
def hash_password(password):
    # 🔴 Weak hashing (MD5)
    return hashlib.md5(password.encode()).hexdigest()

# 9. Insecure random
import random
def generate_token():
    # 🔴 Insecure random for security purposes
    return random.randint(1000, 9999)

# 10. Debug mode in production
@app.route('/')
def home():
    user_input = request.args.get('input', '')
    
    # 🔴 Various vulnerabilities in one function
    if user_input:
        # Command injection
        result = run_system_command(f"echo {user_input}")
        
        # SQL injection  
        user_data = get_user_data(user_input)
        
        # Insecure deserialization
        try:
            loaded = load_user_data(user_input.encode())
        except:
            loaded = None
    
    return "Welcome to vulnerable app!"

# 11. Insecure CORS
@app.after_request
def after_request(response):
    # 🔴 Overly permissive CORS
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

# 12. Information exposure
@app.route('/debug')
def debug_info():
    # 🔴 Information exposure
    return {
        'database_password': DATABASE_PASSWORD,
        'api_key': API_KEY,
        'system_path': os.environ.get('PATH'),
        'secret_key': app.secret_key
    }

# 13. Insecure configuration
app.config['SECRET_KEY'] = 'hardcoded_secret_key'
app.config['DEBUG'] = True  # 🔴 Debug mode in production

# 14. Insecure direct object reference
@app.route('/files/<filename>')
def get_file(filename):
    # 🔴 Insecure direct object reference
    return read_sensitive_file(filename)

# 15. SSRF vulnerability
@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    # 🔴 Potential SSRF
    response = requests.get(url, timeout=5)
    return response.text

# 16. Code injection
@app.route('/execute')
def execute_code():
    code = request.args.get('code')
    # 🔴 Code injection
    exec(code)
    return "Code executed"

# 17. Insecure session management
from flask import session
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # 🔴 Weak password hashing
    hashed_pw = hash_password(password)
    
    # 🔴 Session fixation vulnerability
    session['user'] = username
    session['admin'] = True  # 🔴 Hardcoded admin access
    
    return "Logged in"

# 18. Insecure headers
@app.route('/admin')
def admin_panel():
    # 🔴 Missing security headers
    return "Admin panel"

# 19. Buffer overflow potential
def process_large_input(data):
    # 🔴 Potential buffer issues
    large_string = "A" * 1000000 + data
    return large_string[:100]

# 20. Insecure dependencies (simulated)
def use_deprecated_library():
    # 🔴 Using deprecated/insecure methods
    import md5  # Deprecated
    return md5.new("data").hexdigest()

# 21. Race condition
import threading
counter = 0

def increment_counter():
    global counter
    # 🔴 Race condition
    counter += 1

# 22. Insecure logging
import logging
def log_sensitive_data(user_data):
    # 🔴 Logging sensitive information
    logging.info(f"User login: {user_data}")
    print(f"Password attempt: {user_data.get('password')}")

# 23. Weak input validation
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    # 🔴 Weak email validation
    if '@' in email:
        return "Valid email"
    return "Invalid email"

# 24. Insecure crypto
import base64
def encrypt_data(data):
    # 🔴 Weak encryption (base64 is not encryption!)
    return base64.b64encode(data.encode())

# 25. Hardcoded IPs and endpoints
INTERNAL_SERVICE = "http://192.168.1.100:8080/internal-api"

def call_internal_service():
    # 🔴 Hardcoded internal endpoints
    return requests.get(INTERNAL_SERVICE).json()

if __name__ == '__main__':
    # 🔴 Running with debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
