from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import get_user_by_username, check_user_password
from app.models.livro import Livro  # Importa a classe Modelo POO

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username)
        
        if user and check_user_password(user, password):
            session['user_id'] = user['id'] if hasattr(user, '__getitem__') else user.id
            return redirect(url_for('auth.welcome'))
        
        flash('Usuário ou senha inválidos!', 'danger')
    
    # Aponta diretamente para login.html na pasta app/templates/
    return render_template('login.html')

@auth_bp.route('/welcome')
def welcome():
    # Busca todos os livros do SQLite através do método de classe POO
    livros_cadastrados = Livro.get_all()
    
    # Aponta diretamente para welcome.html na pasta app/templates/
    return render_template('welcome.html', livros=livros_cadastrados)

@auth_bp.route('/livros/novo', methods=['GET', 'POST'])
def cadastrar_livro():
    if request.method == 'POST':
        # 1. Recebe os dados do formulário HTML
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        ano = request.form.get('ano')

        if titulo and autor and ano:
            # 2. Instancia o objeto da classe modelo POO
            novo_livro = Livro(titulo=titulo, autor=autor, ano=int(ano))
            
            # 3. Guarda no ficheiro .db via sqlite3
            novo_livro.salvar()
            
            # 4. Redireciona para a listagem
            return redirect(url_for('auth.welcome'))

    # Aponta diretamente para cadastrar_livro.html na pasta app/templates/
    return render_template('cadastrar_livro.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))