from flask import Flask, render_template_string, render_template, jsonify

app = Flask(__name__)

@app.route('/test')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
