import sqlite3
from database import conectar
from tkinter import messagebox

# ----------------------- Aluno ------------------------

def incluir_aluno(nome, matricula):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO aluno (nome, matricula) VALUES (?, ?)", (nome, matricula))
            conn.commit()
            return True # Retorna True em caso de sucesso
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Matrícula já existe!")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao incluir aluno: {e}")
            return False
        finally:
            conn.close()
    return False

def listar_alunos():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM aluno ORDER BY nome ASC") # Ordena por nome
            dados = cursor.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao listar alunos: {e}")
            return []
        finally:
            conn.close()
    return []

def buscar_alunos(termo_busca):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            # Busca por nome ou matrícula, case-insensitive
            cursor.execute("SELECT * FROM aluno WHERE nome LIKE ? OR matricula LIKE ? ORDER BY nome ASC",
                           (f"%{termo_busca}%", f"%{termo_busca}%"))
            dados = cursor.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Busca", f"Erro ao buscar alunos: {e}")
            return []
        finally:
            conn.close()
    return []


def alterar_aluno(matricula_antiga, novo_nome, nova_matricula):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            # Primeiro, encontra o aluno pelo ID para obter o ID real
            cursor.execute("SELECT id FROM aluno WHERE matricula = ?", (matricula_antiga,))
            aluno_data = cursor.fetchone()
            if not aluno_data:
                messagebox.showwarning("Aviso", "Aluno não encontrado com a matrícula especificada.")
                return False
            id_aluno = aluno_data[0]

            cursor.execute("UPDATE aluno SET nome = ?, matricula = ? WHERE id = ?", (novo_nome, nova_matricula, id_aluno))
            conn.commit()
            if cursor.rowcount == 0:
                # Este caso é pouco provável com a busca por ID, mas mantemos
                messagebox.showwarning("Aviso", "Nenhum aluno encontrado com a matrícula especificada para alteração.")
                return False
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nova matrícula já existe para outro aluno!")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao alterar aluno: {e}")
            return False
        finally:
            conn.close()
    return False

def excluir_aluno(matricula):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM aluno WHERE matricula = ?", (matricula,))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "Nenhum aluno encontrado com a matrícula especificada.")
                return False
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao excluir aluno: {e}")
            return False
        finally:
            conn.close()
    return False

# ----------------------- Disciplina ------------------------

def incluir_disciplina(nome, codigo):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO disciplina (nome, codigo) VALUES (?, ?)", (nome, codigo))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Código de disciplina já existe!")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao incluir disciplina: {e}")
            return False
        finally:
            conn.close()
    return False

def listar_disciplinas():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM disciplina ORDER BY nome ASC")
            dados = cursor.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao listar disciplinas: {e}")
            return []
        finally:
            conn.close()
    return []

# Não é necessário buscar disciplina por nome, pois o código já é único e pode ser usado para busca.
# No entanto, podemos adicionar uma função de busca se for útil para filtrar a lista.
def buscar_disciplinas(termo_busca):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM disciplina WHERE nome LIKE ? OR codigo LIKE ? ORDER BY nome ASC",
                           (f"%{termo_busca}%", f"%{termo_busca}%"))
            dados = cursor.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Busca", f"Erro ao buscar disciplinas: {e}")
            return []
        finally:
            conn.close()
    return []


def alterar_disciplina(id_disc, novo_nome, novo_codigo):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE disciplina SET nome = ?, codigo = ? WHERE id = ?", (novo_nome, novo_codigo, id_disc))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "Nenhuma disciplina encontrada com o ID especificado.")
                return False
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Novo código de disciplina já existe para outra disciplina!")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao alterar disciplina: {e}")
            return False
        finally:
            conn.close()
    return False

def excluir_disciplina(id_disc):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM disciplina WHERE id = ?", (id_disc,))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "Nenhuma disciplina encontrada com o ID especificado.")
                return False
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao excluir disciplina: {e}")
            return False
        finally:
            conn.close()
    return False

# ----------------------- Nota ------------------------

def incluir_nota(aluno_id, disciplina_id, valor):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            # Verifica se o aluno e a disciplina existem antes de inserir a nota
            cursor.execute("SELECT id FROM aluno WHERE id = ?", (aluno_id,))
            if cursor.fetchone() is None:
                messagebox.showerror("Erro", "ID do aluno não encontrado.")
                return False

            cursor.execute("SELECT id FROM disciplina WHERE id = ?", (disciplina_id,))
            if cursor.fetchone() is None:
                messagebox.showerror("Erro", "ID da disciplina não encontrado.")
                return False

            cursor.execute("INSERT INTO nota (aluno_id, disciplina_id, valor) VALUES (?, ?, ?)", (aluno_id, disciplina_id, valor))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "ID de aluno ou disciplina inválido. Verifique se o aluno e a disciplina existem.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao incluir nota: {e}")
            return False
        finally:
            conn.close()
    return False

def listar_notas():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT nota.id, aluno.nome, disciplina.nome, nota.valor
                FROM nota
                JOIN aluno ON nota.aluno_id = aluno.id
                JOIN disciplina ON nota.disciplina_id = disciplina.id
                ORDER BY aluno.nome, disciplina.nome
            """)
            dados = cursor.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao listar notas: {e}")
            return []
        finally:
            conn.close()
    return []

def buscar_notas(termo_busca):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            # Busca notas por nome do aluno ou nome da disciplina
            cursor.execute("""
                SELECT nota.id, aluno.nome, disciplina.nome, nota.valor
                FROM nota
                JOIN aluno ON nota.aluno_id = aluno.id
                JOIN disciplina ON nota.disciplina_id = disciplina.id
                WHERE aluno.nome LIKE ? OR disciplina.nome LIKE ?
                ORDER BY aluno.nome, disciplina.nome
            """, (f"%{termo_busca}%", f"%{termo_busca}%"))
            dados = cursor.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Busca", f"Erro ao buscar notas: {e}")
            return []
        finally:
            conn.close()
    return []

def alterar_nota(id_nota, novo_valor):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE nota SET valor = ? WHERE id = ?", (novo_valor, id_nota))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "Nenhuma nota encontrada com o ID especificado.")
                return False
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao alterar nota: {e}")
            return False
        finally:
            conn.close()
    return False

def excluir_nota(id_nota):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM nota WHERE id = ?", (id_nota,))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "Nenhuma nota encontrada com o ID especificado.")
                return False
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao excluir nota: {e}")
            return False
        finally:
            conn.close()
    return False