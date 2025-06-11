import sqlite3
from tkinter import messagebox # Importar messagebox para exibir erros (tratamento de exceção)

def conectar():
    try:
        conn = sqlite3.connect('sistema_escolar.db')
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados: {e}")
        return None

def criar_tabelas():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS aluno (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    matricula TEXT NOT NULL UNIQUE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS disciplina (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    codigo TEXT NOT NULL UNIQUE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nota (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER,
                    disciplina_id INTEGER,
                    valor REAL,
                    FOREIGN KEY(aluno_id) REFERENCES aluno(id) ON DELETE CASCADE,
                    FOREIGN KEY(disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Criação de Tabela", f"Erro ao criar tabelas: {e}")
        finally:
            conn.close()