import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key'

db = TinyDB('db.json')
users_table = db.table('users')
User = Query()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username:
            flash('Uporabniško ime je obvezno.', 'error')
            return render_template('register.html', username=username)

        if len(password) < 6:
            flash('Geslo mora vsebovati vsaj 6 znakov.', 'error')
            return render_template('register.html', username=username)

        existing_user = users_table.get(User.username == username)
        if existing_user:
            flash('Uporabniško ime že obstaja.', 'error')
            return render_template('register.html', username=username)

        users_table.insert({
            'id': uuid.uuid4().hex,
            'username': username,
            'password_hash': generate_password_hash(password),
        })

        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
