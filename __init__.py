from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/', methods=['GET'])
def return_home():
    if 'authentifie' in session and session['authentifie']:
        return render_template('home.html')
    else:
        return redirect(url_for('authentification'))




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
