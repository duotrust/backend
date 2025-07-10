from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'replace-this-with-a-strong-key'

login_manager = LoginManager()
login_manager.init_app(app)

# Simple in‑memory user store
users = {'admin': {'password': 'BBQs@uce@2025!@#$', 'role': 'admin'}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in users and users[u]['password'] == p:
            login_user(User(u))
            return redirect(url_for('dashboard'))
        return "Invalid credentials", 401
    return '''
      <form action="" method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Login</button>
      </form>
    '''

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.id}! You are logged in."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
