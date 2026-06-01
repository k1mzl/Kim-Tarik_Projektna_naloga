import uuid
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key'

db = TinyDB('db.json')
users_table = db.table('users')
trenings_table = db.table('recipes')
User = Query()
Trening = Query()

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return users_table.get(User.id == user_id)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not get_current_user():
            flash('Za to dejanje se morate prijaviti.', 'error')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view

@app.context_processor
def inject_current_user():
    return {'current_user': get_current_user()}

@app.route('/')
def index():
    sport_filter = request.args.get('sport', '').strip()
    difficulty_filter = request.args.get('difficulty', '').strip()
    current_user = get_current_user()

    trenings = trenings_table.all()
    sports = sorted({trening.get('sport', '') for trening in trenings if trening.get('sport')})
    difficulties = sorted({trening.get('difficulty', '') for trening in trenings if trening.get('difficulty')})

    if sport_filter:
        trenings = [trening for trening in trenings if trening.get('sport') == sport_filter]
    if difficulty_filter:
        trenings = [trening for trening in trenings if trening.get('difficulty') == difficulty_filter]

    return render_template(
        'index.html',
        trenings=trenings,
        sports=sports,
        difficulties=difficulties,
        selected_sport=sport_filter,
        selected_difficulty=difficulty_filter,
        current_user=current_user,
        mine_view=False,
    )

@app.route('/my')
@login_required
def my_trenings():
    current_user = get_current_user()
    sport_filter = request.args.get('sport', '').strip()
    difficulty_filter = request.args.get('difficulty', '').strip()

    trenings = trenings_table.search(Trening.user_id == current_user['id'])
    sports = sorted({trening.get('sport', '') for trening in trenings if trening.get('sport')})
    difficulties = sorted({trening.get('difficulty', '') for trening in trenings if trening.get('difficulty')})

    if sport_filter:
        trenings = [trening for trening in trenings if trening.get('sport') == sport_filter]
    if difficulty_filter:
        trenings = [trening for trening in trenings if trening.get('difficulty') == difficulty_filter]

    return render_template(
        'index.html',
        trenings=trenings,
        sports=sports,
        difficulties=difficulties,
        selected_sport=sport_filter,
        selected_difficulty=difficulty_filter,
        mine_view=True,
    )

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

        new_user = {
            'id': uuid.uuid4().hex,
            'username': username,
            'password_hash': generate_password_hash(password),
        }
        users_table.insert(new_user)
        session['user_id'] = new_user['id']
        session['username'] = new_user['username']

        flash('Registracija uspešna. Dobrodošli!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', current_user=get_current_user())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = users_table.get(User.username == username)

        if not user or not check_password_hash(user['password_hash'], password):
            flash('Napačno uporabniško ime ali geslo.', 'error')
            return render_template('login.html', username=username)

        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('Prijava uspešna.', 'success')
        return redirect(url_for('my_trenings'))

    return render_template('login.html', current_user=get_current_user())

@app.route('/logout')
def logout():
    session.clear()
    flash('Odjava uspešna.', 'success')
    return redirect(url_for('index'))

@app.route('/trening/<trening_id>')
def trening_detail(trening_id):
    trening = trenings_table.get(Trening.id == trening_id)
    if not trening:
        flash('Trening ni bil najden.', 'error')
        return redirect(url_for('index'))

    return render_template('trening_detail.html', trening=trening, current_user=get_current_user())


@app.route('/trening/<trening_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trening(trening_id):
    trening = trenings_table.get(Trening.id == trening_id)
    if not trening:
        flash('Trening ni bil najden.', 'error')
        return redirect(url_for('index'))

    current_user = get_current_user()
    if trening.get('user_id') != current_user['id']:
        flash('Niste pooblaščeni za urejanje tega treninga.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        sport = request.form.get('sport', '').strip()
        difficulty = request.form.get('difficulty', '').strip()
        description = request.form.get('description', '').strip()
        duration = request.form.get('duration', '').strip()
        equipment = request.form.get('equipment', '').strip()

        if not all([name, sport, difficulty, description, duration, equipment]):
            flash('Vsa polja so obvezna.', 'error')
            return render_template('edit_trening.html', trening=trening)

        trenings_table.update({
            'name': name,
            'sport': sport,
            'difficulty': difficulty,
            'description': description,
            'duration': duration,
            'equipment': equipment,
        }, Trening.id == trening_id)

        flash('Trening je bil posodobljen.', 'success')
        return redirect(url_for('trening_detail', trening_id=trening_id))

    return render_template('edit_trening.html', trening=trening)


@app.route('/trening/<trening_id>/delete', methods=['POST'])
@login_required
def delete_trening(trening_id):
    trening = trenings_table.get(Trening.id == trening_id)
    if not trening:
        flash('Trening ni bil najden.', 'error')
        return redirect(url_for('index'))

    current_user = get_current_user()
    if trening.get('user_id') != current_user['id']:
        flash('Niste pooblaščeni za brisanje tega treninga.', 'error')
        return redirect(url_for('index'))

    trenings_table.remove(Trening.id == trening_id)
    flash('Trening je bil izbrisan.', 'success')
    return redirect(url_for('my_trenings'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_trening():
    current_user = get_current_user()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        sport = request.form.get('sport', '').strip()
        difficulty = request.form.get('difficulty', '').strip()
        description = request.form.get('description', '').strip()
        duration = request.form.get('duration', '').strip()
        equipment = request.form.get('equipment', '').strip()

        if not all([name, sport, difficulty, description, duration, equipment]):
            flash('Vsa polja so obvezna.', 'error')
            return render_template(
                'add_trening.html',
                name=name,
                sport=sport,
                difficulty=difficulty,
                description=description,
                duration=duration,
                equipment=equipment,
            )

        trenings_table.insert({
            'id': uuid.uuid4().hex,
            'user_id': current_user['id'],
            'name': name,
            'sport': sport,
            'difficulty': difficulty,
            'description': description,
            'duration': duration,
            'equipment': equipment,
        })

        flash('Trening je bil uspešno dodan.', 'success')
        return redirect(url_for('my_trenings'))

    return render_template('add_trening.html')

if __name__ == '__main__':
    app.run(debug=True)
