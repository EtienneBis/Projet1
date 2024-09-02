from flask import Flask, render_template_string, render_template, jsonify

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('hello.html')

# @app.route('/signin')
# def signin():
#     return render_template('signin.html')

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')

@app.route('/', methods=['GET'])
def return_home():
    if 'authentifie' in session and session['authentifie']:
        return render_template('home.html')
    else:
        return redirect(url_for('authentification'))

if __name__ == '__main__':
    app.run(debug=True)
