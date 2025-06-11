import json
from models import listar_alunos, listar_disciplinas, listar_notas
from tkinter import messagebox

def exportar_dados_para_json(caminho='dados_exportados.json'):
    dados = {
        'alunos': [],
        'disciplinas': [],
        'notas': []
    }

    try:
        for a in listar_alunos():
            dados['alunos'].append({
                'id': a[0],
                'nome': a[1],
                'matricula': a[2]
            })

        for d in listar_disciplinas():
            dados['disciplinas'].append({
                'id': d[0],
                'nome': d[1],
                'codigo': d[2]
            })

        for n in listar_notas():
            dados['notas'].append({
                'id': n[0],
                'aluno': n[1],
                'disciplina': n[2],
                'valor': n[3]
            })

        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return True
    except IOError as e:
        messagebox.showerror("Erro de Exportação", f"Não foi possível escrever o arquivo JSON: {e}")
        return False
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado durante a exportação: {e}")
        return False