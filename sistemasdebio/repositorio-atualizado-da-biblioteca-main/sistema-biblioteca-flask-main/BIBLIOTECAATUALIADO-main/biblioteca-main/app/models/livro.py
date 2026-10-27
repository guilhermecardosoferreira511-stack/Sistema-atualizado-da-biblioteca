from app.database import DatabaseConnection

class Livro:
    """
    Classe de Modelo (POO) para a entidade Livro.
    Isola os comandos SQL nativos do restante da aplicação.
    """
    def __init__(self, titulo=None, autor=None, ano=None, livro_id=None):
        self.id = livro_id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano

    @classmethod
    def init_db(cls):
        """Cria a tabela 'livros' caso não exista no arquivo biblioteca.db."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano INTEGER NOT NULL
                )
            ''')

    def salvar(self):
        """Insere o livro atual diretamente na base de dados SQLite."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)"
            cursor.execute(sql, (self.titulo, self.autor, self.ano))
            self.id = cursor.lastrowid
        return self

    @classmethod
    def get_all(cls):
        """Realiza um SELECT e retorna todos os registros do banco de dados."""
        cls.init_db()
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, autor, ano FROM livros")
            return cursor.fetchall()