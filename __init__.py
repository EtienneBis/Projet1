import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = r'b_45[y2L"B4Q8z\n\zf#/'  # Clé secrète

# Configurer la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurer le dossier pour les images téléchargées
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

# Créer le dossier si nécessaire
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modèle utilisateur
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    photos = db.relationship('Photo', backref='owner', lazy=True)

# Modèle photo
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Créer les tables dans la base de données
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route du menu
@app.route('/')
def home():
    return render_template('home.html')

# Route d'inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        flash('Invalid credentials')
    return render_template('login.html')

# Route de déconnexion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Route pour le profil
@app.route('/profile')
@login_required
def profile():
    user_photos = Photo.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', photos=user_photos)

# Route pour upload une photo
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('profile'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('profile'))
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_photo = Photo(filename=filename, owner=current_user)
        db.session.add(new_photo)
        db.session.commit()
        return redirect(url_for('profile'))


# Route pour télécharger une photo
@app.route('/download/<filename>')
@login_required
def download_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)






if __name__ == '__main__':
    app.run(debug=True)
