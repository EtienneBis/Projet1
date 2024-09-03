# from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('test.html')

# @app.route('/signin')
# def signin():
#     return render_template('signin.html')

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')




from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'b_45[y2L"B4Q8z\nzzf#/'  # Clé secrète

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Page de redirection si non connecté

# Utilisateurs fictifs (à remplacer par une gestion réelle des utilisateurs)
users = {
    'user1': {'password': generate_password_hash('password')},
    'user2': {'password': generate_password_hash('anotherpassword')}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            login_user(User(username))
            return redirect(url_for('profile'))
        return 'Invalid credentials', 401  # Ajout d'un statut HTTP en cas d'échec de connexion
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return f'Hello, {current_user.id}!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))








# @app.route('/', methods=['GET'])
# def return_home():
#     if 'authentifie' in session and session['authentifie']:
#         return render_template('home.html')
#     else:
#         return redirect(url_for('authentification'))









# @app.route('/sign_up', methods=['GET'])
# def formulaire_client():
#     return render_template('signup.html')

# @app.route('/sign_up', methods=['POST'])
# def enregistrer_client():
#     login = request.form['login']
#     password = request.form['password']

#     conn = sqlite3.connect('database/database.db')
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO user (login, password) VALUES (?, ?)', (login, password))
#     conn.commit()
#     conn.close()
#     user = verify_credentials(login, password)
#     if user:
#         session['authentifie'] = True
#         session['user_id'] = user[0] 
#         return redirect(url_for('ReadBDD'))
    
#     return redirect('/')

# @app.route('/sign_in', methods=['GET', 'POST'])
# def authentification():
#     if request.method == 'POST':
#         login = request.form['login']
#         password = request.form['password']
#         user = verify_credentials(login, password)
#         if user:
#             session['authentifie'] = True
#             session['user_id'] = user[0] 
#             return redirect('/')
#         else:
#             return render_template('signin.html', error=True)
#     return render_template('signin.html', error=False)

# @app.route('/sign_out', methods=['GET'])
# def deconnexion_utilisateur():
#     session['authentifie'] = False
#     session['user_id'] = "" 
#     return redirect('/')










if __name__ == '__main__':
    app.run(debug=True)
