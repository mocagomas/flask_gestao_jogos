from flask import Flask, flash, render_template, redirect, url_for, request, flash
from models import db, Jogo, Utilizador
from forms import JogoForm, LoginForm, RegistoForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.secret_key = 'segredomuitobemguardado'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Utilizador.query.get(int(user_id))

# Criar a Base de dados
@app.before_request
def criar_bd():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('listar'))

@app.route('/jogos')
@login_required
def listar():
    jogos = Jogo.query.all()
    return render_template('lista.html', jogos=jogos)

@app.route('/livros/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    form = JogoForm()
    if form.validate_on_submit():
        jogo = Jogo(titulo=form.titulo.data, genero=form.genero.data, plataforma=form.plataforma.data)
        db.session.add(jogo)
        db.session.commit()
        return redirect(url_for('listar'))
    return render_template('adicionar.html', form=form)

@app.route('/jogos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    jogo = Jogo.query.get_or_404(id)
    form = JogoForm(obj=jogo)
    if form.validate_on_submit():
        form.populate_obj(jogo)
        db.session.commit()
        return redirect(url_for('listar'))
    return render_template('editar.html', form=form)

@app.route('/jogos/apagar/<int:id>')
@login_required
def apagar(id):
    jogo = Jogo.query.get_or_404(id)
    db.session.delete(jogo)
    db.session.commit()
    return redirect(url_for('listar'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilizador.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        return "Login inválido. Tente novamente!"
    return render_template('login.html', form=form)

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    form = RegistoForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        if not username or not password:
            flash("Preencha todos os campos corretamente.", "erro")
            return render_template('registo.html', form=form)

        if Utilizador.query.filter_by(username=username).first():
            flash("O utilizador já existe, escolha outro nome.", "erro")
            return render_template('registo.html', form=form)

        novo_utilizador = Utilizador(username=username)
        novo_utilizador.set_password(password)
        db.session.add(novo_utilizador)
        db.session.commit()
        flash("Registo efetuado com sucesso!", "sucesso")
        return redirect(url_for('login'))

    return render_template('registo.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)