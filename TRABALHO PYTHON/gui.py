import tkinter as tk
from tkinter import ttk, messagebox
from models import (
    incluir_aluno, listar_alunos, alterar_aluno, excluir_aluno, buscar_alunos,
    incluir_disciplina, listar_disciplinas, alterar_disciplina, excluir_disciplina, buscar_disciplinas,
    incluir_nota, listar_notas, alterar_nota, excluir_nota, buscar_notas
)
from exporter import exportar_dados_para_json

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Escolar")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#e0e0e0')
        style.configure('TLabel', background='#e0e0e0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        style.configure('TEntry', font=('Arial', 10))
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        style.map('TButton', background=[('active', '#c0c0c0')])

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill='both', expand=True, padx=10, pady=10)

        self.criar_aba_alunos()
        self.criar_aba_disciplinas()
        self.criar_aba_notas()
        self.criar_aba_exportar()

    # --- Funções de Placeholder ---
    def setup_placeholder(self, entry_widget, placeholder_text):
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(foreground='grey')

        entry_widget.bind("<FocusIn>", lambda event: self.on_focus_in(event, entry_widget, placeholder_text))
        entry_widget.bind("<FocusOut>", lambda event: self.on_focus_out(event, entry_widget, placeholder_text))

    def on_focus_in(self, event, entry_widget, placeholder_text):
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, tk.END)
            entry_widget.config(foreground='black')

    def on_focus_out(self, event, entry_widget, placeholder_text):
        if not entry_widget.get():
            entry_widget.insert(0, placeholder_text)
            entry_widget.config(foreground='grey')

    # ------------------- Aba Alunos -------------------

    def criar_aba_alunos(self):
        aba = ttk.Frame(self.tabs, padding="10 10 10 10")
        self.tabs.add(aba, text='Alunos')

        frame_controles = ttk.LabelFrame(aba, text="Gerenciar Alunos", padding="10 10 10 10")
        frame_controles.pack(pady=10, fill='x')

        tk.Label(frame_controles, text="Nome:").grid(row=0, column=0, sticky='w', pady=5)
        self.nome_aluno_entry = ttk.Entry(frame_controles, width=40)
        self.nome_aluno_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame_controles, text="Matrícula:").grid(row=1, column=0, sticky='w', pady=5)
        self.matricula_aluno_entry = ttk.Entry(frame_controles, width=40)
        self.matricula_aluno_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame_controles, text="Filtrar:").grid(row=2, column=0, sticky='w', pady=5)
        self.termo_busca_aluno_entry = ttk.Entry(frame_controles, width=30)
        self.termo_busca_aluno_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.setup_placeholder(self.termo_busca_aluno_entry, "Nome ou Matrícula")

        ttk.Button(frame_controles, text="Filtrar", command=self.buscar_alunos).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(frame_controles, text="Limpar Filtro", command=self.limpar_busca_alunos).grid(row=2, column=3, padx=5, pady=5)


        frame_botoes = ttk.Frame(frame_controles)
        frame_botoes.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(frame_botoes, text="Incluir", command=self.adicionar_aluno).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Alterar", command=self.editar_aluno).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.deletar_aluno).pack(side='left', padx=5)

        self.lista_alunos = tk.Listbox(aba, height=15, selectmode=tk.SINGLE, font=('Arial', 10))
        self.lista_alunos.pack(fill='both', expand=True, pady=10)
        self.lista_alunos.bind('<<ListboxSelect>>', self.carregar_aluno_selecionado)

        self.atualizar_lista_alunos()

    def atualizar_lista_alunos(self, dados=None):
        self.lista_alunos.delete(0, tk.END)
        alunos_para_exibir = dados if dados is not None else listar_alunos()
        for aluno in alunos_para_exibir:
            self.lista_alunos.insert(tk.END, f"ID: {aluno[0]} - {aluno[1]} ({aluno[2]})")

    def buscar_alunos(self):
        termo = self.termo_busca_aluno_entry.get().strip()
        if termo == "Nome ou Matrícula":
            termo = ""

        if termo:
            resultados = buscar_alunos(termo)
            self.atualizar_lista_alunos(resultados)
        else:
            self.atualizar_lista_alunos()

    def limpar_busca_alunos(self):
        self.termo_busca_aluno_entry.delete(0, tk.END)
        self.setup_placeholder(self.termo_busca_aluno_entry, "Nome ou Matrícula")
        self.atualizar_lista_alunos()

    def carregar_aluno_selecionado(self, event):
        selecao = self.lista_alunos.curselection()
        if selecao:
            idx = selecao[0]
            item_selecionado = self.lista_alunos.get(idx)
            try:
                id_aluno_str = item_selecionado.split(' - ')[0].replace('ID: ', '')
                id_aluno = int(id_aluno_str)

                aluno_selecionado = next((a for a in listar_alunos() if a[0] == id_aluno), None)

                if aluno_selecionado:
                    self.nome_aluno_entry.delete(0, tk.END)
                    self.nome_aluno_entry.insert(0, aluno_selecionado[1])
                    self.matricula_aluno_entry.delete(0, tk.END)
                    self.matricula_aluno_entry.insert(0, aluno_selecionado[2])
            except (ValueError, IndexError):
                messagebox.showwarning("Erro", "Não foi possível carregar os dados do aluno selecionado.")

    def adicionar_aluno(self):
        nome = self.nome_aluno_entry.get().strip()
        matricula = self.matricula_aluno_entry.get().strip()
        if not nome or not matricula:
            messagebox.showwarning("Entrada Inválida", "Nome e Matrícula não podem ser vazios.")
            return

        if incluir_aluno(nome, matricula):
            messagebox.showinfo("Sucesso", "Aluno incluído com sucesso!")
            self.nome_aluno_entry.delete(0, tk.END)
            self.matricula_aluno_entry.delete(0, tk.END)
            self.atualizar_lista_alunos()

    def editar_aluno(self):
        selecao = self.lista_alunos.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um aluno para alterar.")
            return

        item_selecionado = self.lista_alunos.get(selecao[0])
        try:
            matricula_antiga = item_selecionado.split('(')[-1].replace(')', '')
        except IndexError:
            messagebox.showerror("Erro", "Formato de item selecionado inválido. Tente novamente.")
            return

        novo_nome = self.nome_aluno_entry.get().strip()
        nova_matricula = self.matricula_aluno_entry.get().strip()

        if not novo_nome or not nova_matricula:
            messagebox.showwarning("Entrada Inválida", "Nome e Matrícula não podem ser vazios.")
            return

        if alterar_aluno(matricula_antiga, novo_nome, nova_matricula):
            messagebox.showinfo("Sucesso", "Aluno alterado com sucesso!")
            self.nome_aluno_entry.delete(0, tk.END)
            self.matricula_aluno_entry.delete(0, tk.END)
            self.atualizar_lista_alunos()

    def deletar_aluno(self):
        selecao = self.lista_alunos.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um aluno para excluir.")
            return

        item_selecionado = self.lista_alunos.get(selecao[0])
        try:
            matricula = item_selecionado.split('(')[-1].replace(')', '')
        except IndexError:
            messagebox.showerror("Erro", "Formato de item selecionado inválido. Tente novamente.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o aluno com matrícula {matricula}?"):
            if excluir_aluno(matricula):
                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                self.nome_aluno_entry.delete(0, tk.END)
                self.matricula_aluno_entry.delete(0, tk.END)
                self.atualizar_lista_alunos()
                self.atualizar_lista_notas()

    # ------------------- Aba Disciplinas -------------------

    def criar_aba_disciplinas(self):
        aba = ttk.Frame(self.tabs, padding="10 10 10 10")
        self.tabs.add(aba, text='Disciplinas')

        frame_controles = ttk.LabelFrame(aba, text="Gerenciar Disciplinas", padding="10 10 10 10")
        frame_controles.pack(pady=10, fill='x')

        tk.Label(frame_controles, text="Nome:").grid(row=0, column=0, sticky='w', pady=5)
        self.nome_disciplina_entry = ttk.Entry(frame_controles, width=40)
        self.nome_disciplina_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame_controles, text="Código:").grid(row=1, column=0, sticky='w', pady=5)
        self.codigo_disciplina_entry = ttk.Entry(frame_controles, width=40)
        self.codigo_disciplina_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame_controles, text="Filtrar:").grid(row=2, column=0, sticky='w', pady=5)
        self.termo_busca_disciplina_entry = ttk.Entry(frame_controles, width=30)
        self.termo_busca_disciplina_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.setup_placeholder(self.termo_busca_disciplina_entry, "Nome ou Código")

        ttk.Button(frame_controles, text="Filtrar", command=self.buscar_disciplinas).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(frame_controles, text="Limpar Filtro", command=self.limpar_busca_disciplinas).grid(row=2, column=3, padx=5, pady=5)


        frame_botoes = ttk.Frame(frame_controles)
        frame_botoes.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(frame_botoes, text="Incluir", command=self.adicionar_disciplina).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Alterar", command=self.editar_disciplina).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.deletar_disciplina).pack(side='left', padx=5)

        self.lista_disciplinas = tk.Listbox(aba, height=15, selectmode=tk.SINGLE, font=('Arial', 10))
        self.lista_disciplinas.pack(fill='both', expand=True, pady=10)
        self.lista_disciplinas.bind('<<ListboxSelect>>', self.carregar_disciplina_selecionada)

        self.atualizar_lista_disciplinas()

    def atualizar_lista_disciplinas(self, dados=None):
        self.lista_disciplinas.delete(0, tk.END)
        disciplinas_para_exibir = dados if dados is not None else listar_disciplinas()
        for d in disciplinas_para_exibir:
            self.lista_disciplinas.insert(tk.END, f"ID: {d[0]} - {d[1]} ({d[2]})")

    def buscar_disciplinas(self):
        termo = self.termo_busca_disciplina_entry.get().strip()
        if termo == "Nome ou Código":
            termo = ""

        if termo:
            resultados = buscar_disciplinas(termo)
            self.atualizar_lista_disciplinas(resultados)
        else:
            self.atualizar_lista_disciplinas()

    def limpar_busca_disciplinas(self):
        self.termo_busca_disciplina_entry.delete(0, tk.END)
        self.setup_placeholder(self.termo_busca_disciplina_entry, "Nome ou Código")
        self.atualizar_lista_disciplinas()

    def carregar_disciplina_selecionada(self, event):
        selecao = self.lista_disciplinas.curselection()
        if selecao:
            idx = selecao[0]
            item_selecionado = self.lista_disciplinas.get(idx)
            try:
                id_disciplina_str = item_selecionado.split(' - ')[0].replace('ID: ', '')
                id_disciplina = int(id_disciplina_str)
                disciplina_selecionada = next((d for d in listar_disciplinas() if d[0] == id_disciplina), None)
                if disciplina_selecionada:
                    self.nome_disciplina_entry.delete(0, tk.END)
                    self.nome_disciplina_entry.insert(0, disciplina_selecionada[1])
                    self.codigo_disciplina_entry.delete(0, tk.END)
                    self.codigo_disciplina_entry.insert(0, disciplina_selecionada[2])
            except (ValueError, IndexError):
                messagebox.showwarning("Erro", "Não foi possível carregar os dados da disciplina selecionada.")

    def adicionar_disciplina(self):
        nome = self.nome_disciplina_entry.get().strip()
        codigo = self.codigo_disciplina_entry.get().strip()
        if not nome or not codigo:
            messagebox.showwarning("Entrada Inválida", "Nome e Código não podem ser vazios.")
            return

        if incluir_disciplina(nome, codigo):
            messagebox.showinfo("Sucesso", "Disciplina incluída com sucesso!")
            self.nome_disciplina_entry.delete(0, tk.END)
            self.codigo_disciplina_entry.delete(0, tk.END)
            self.atualizar_lista_disciplinas()

    def editar_disciplina(self):
        selecao = self.lista_disciplinas.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma disciplina para alterar.")
            return

        idx = selecao[0]
        item_selecionado = self.lista_disciplinas.get(idx)
        try:
            id_disciplina_str = item_selecionado.split(' - ')[0].replace('ID: ', '')
            id_disc = int(id_disciplina_str)
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Não foi possível obter o ID da disciplina selecionada.")
            return

        novo_nome = self.nome_disciplina_entry.get().strip()
        novo_codigo = self.codigo_disciplina_entry.get().strip()

        if not novo_nome or not novo_codigo:
            messagebox.showwarning("Entrada Inválida", "Nome e Código não podem ser vazios.")
            return

        if alterar_disciplina(id_disc, novo_nome, novo_codigo):
            messagebox.showinfo("Sucesso", "Disciplina alterada com sucesso!")
            self.nome_disciplina_entry.delete(0, tk.END)
            self.codigo_disciplina_entry.delete(0, tk.END)
            self.atualizar_lista_disciplinas()

    def deletar_disciplina(self):
        selecao = self.lista_disciplinas.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma disciplina para excluir.")
            return

        idx = selecao[0]
        item_selecionado = self.lista_disciplinas.get(idx)
        try:
            id_disciplina_str = item_selecionado.split(' - ')[0].replace('ID: ', '')
            id_disc = int(id_disciplina_str)
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Não foi possível obter o ID da disciplina selecionada.")
            return

        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta disciplina? Isso também excluirá as notas associadas."):
            if excluir_disciplina(id_disc):
                messagebox.showinfo("Sucesso", "Disciplina excluída com sucesso!")
                self.nome_disciplina_entry.delete(0, tk.END)
                self.codigo_disciplina_entry.delete(0, tk.END)
                self.atualizar_lista_disciplinas()
                self.atualizar_lista_notas()

    # ------------------- Aba Notas -------------------

    def criar_aba_notas(self):
        aba = ttk.Frame(self.tabs, padding="10 10 10 10")
        self.tabs.add(aba, text='Notas')

        frame_controles = ttk.LabelFrame(aba, text="Gerenciar Notas", padding="10 10 10 10")
        frame_controles.pack(pady=10, fill='x')

        ttk.Label(frame_controles, text="Para incluir/alterar, use o ID do aluno e da disciplina. Para filtrar, use o nome do aluno ou da disciplina.",
                  font=('Arial', 9, 'italic'), foreground='blue').grid(row=0, column=0, columnspan=4, sticky='w', pady=5) 

        tk.Label(frame_controles, text="ID Aluno:").grid(row=1, column=0, sticky='w', pady=5)
        self.aluno_id_entry = ttk.Entry(frame_controles, width=15)
        self.aluno_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame_controles, text="ID Disciplina:").grid(row=1, column=2, sticky='w', pady=5)
        self.disciplina_id_entry = ttk.Entry(frame_controles, width=15)
        self.disciplina_id_entry.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

        tk.Label(frame_controles, text="Valor da Nota (0-10):").grid(row=2, column=0, sticky='w', pady=5)
        self.nota_entry = ttk.Entry(frame_controles, width=15)
        self.nota_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame_controles, text="Filtrar Nota:").grid(row=3, column=0, sticky='w', pady=5)
        self.termo_busca_nota_entry = ttk.Entry(frame_controles, width=30)
        self.termo_busca_nota_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.setup_placeholder(self.termo_busca_nota_entry, "Nome do Aluno ou Disciplina")

        ttk.Button(frame_controles, text="Filtrar", command=self.buscar_notas).grid(row=3, column=2, padx=5, pady=5) 
        ttk.Button(frame_controles, text="Limpar Filtro", command=self.limpar_busca_notas).grid(row=3, column=3, padx=5, pady=5) 
        frame_botoes = ttk.Frame(frame_controles)
        frame_botoes.grid(row=4, column=0, columnspan=4, pady=10)

        ttk.Button(frame_botoes, text="Incluir", command=self.adicionar_nota).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Alterar", command=self.editar_nota).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.deletar_nota).pack(side='left', padx=5)

        self.lista_notas = tk.Listbox(aba, height=15, selectmode=tk.SINGLE, font=('Arial', 10))
        self.lista_notas.pack(fill='both', expand=True, pady=10)
        self.lista_notas.bind('<<ListboxSelect>>', self.carregar_nota_selecionada)

        self.atualizar_lista_notas()

    def atualizar_lista_notas(self, dados=None):
        self.lista_notas.delete(0, tk.END)
        notas_para_exibir = dados if dados is not None else listar_notas()
        for n in notas_para_exibir:
            self.lista_notas.insert(tk.END, f"ID: {n[0]} - Aluno: {n[1]} | Disciplina: {n[2]} | Nota: {n[3]:.2f}")

    def buscar_notas(self): 
        termo = self.termo_busca_nota_entry.get().strip()
        if termo == "Nome do Aluno ou Disciplina":
            termo = ""

        if termo:
            resultados = buscar_notas(termo)
            self.atualizar_lista_notas(resultados)
        else:
            self.atualizar_lista_notas()

    def limpar_busca_notas(self): 
        self.termo_busca_nota_entry.delete(0, tk.END)
        self.setup_placeholder(self.termo_busca_nota_entry, "Nome do Aluno ou Disciplina")
        self.atualizar_lista_notas()

    def carregar_nota_selecionada(self, event):
        selecao = self.lista_notas.curselection()
        if selecao:
            idx = selecao[0]
            item_selecionado = self.lista_notas.get(idx)
            try:
                id_nota_str = item_selecionado.split(' - ')[0].replace('ID: ', '')
                id_nota = int(id_nota_str)
                
                todas_notas = listar_notas()
                nota_obj = next((n for n in todas_notas if n[0] == id_nota), None)

                if nota_obj:
                    self.aluno_id_entry.delete(0, tk.END)
                    self.disciplina_id_entry.delete(0, tk.END)
                    self.nota_entry.delete(0, tk.END)
                    self.nota_entry.insert(0, str(nota_obj[3]))
            except (ValueError, IndexError):
                messagebox.showwarning("Erro", "Não foi possível carregar os dados da nota selecionada.")

    def adicionar_nota(self):
        aluno_id_str = self.aluno_id_entry.get().strip()
        disciplina_id_str = self.disciplina_id_entry.get().strip()
        valor_str = self.nota_entry.get().strip()

        if not aluno_id_str or not disciplina_id_str or not valor_str:
            messagebox.showwarning("Entrada Inválida", "Todos os campos para nota são obrigatórios.")
            return

        try:
            aluno_id = int(aluno_id_str)
            disciplina_id = int(disciplina_id_str)
            valor = float(valor_str)
            if not (0 <= valor <= 10):
                messagebox.showwarning("Entrada Inválida", "O valor da nota deve estar entre 0 e 10.")
                return
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "ID de Aluno, ID de Disciplina devem ser números inteiros. O valor da nota deve ser um número válido.")
            return

        if incluir_nota(aluno_id, disciplina_id, valor):
            messagebox.showinfo("Sucesso", "Nota incluída com sucesso!")
            self.aluno_id_entry.delete(0, tk.END)
            self.disciplina_id_entry.delete(0, tk.END)
            self.nota_entry.delete(0, tk.END)
            self.atualizar_lista_notas()

    def editar_nota(self):
        selecao = self.lista_notas.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma nota para alterar.")
            return

        idx = selecao[0]
        item_selecionado = self.lista_notas.get(idx)
        try:
            id_nota_str = item_selecionado.split(' - ')[0].replace('ID: ', '')
            id_nota = int(id_nota_str)
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Não foi possível obter o ID da nota selecionada.")
            return

        novo_valor_str = self.nota_entry.get().strip()

        if not novo_valor_str:
            messagebox.showwarning("Entrada Inválida", "O valor da nota não pode ser vazio.")
            return

        try:
            novo_valor = float(novo_valor_str)
            if not (0 <= novo_valor <= 10):
                messagebox.showwarning("Entrada Inválida", "O valor da nota deve estar entre 0 e 10.")
                return
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "O valor da nota deve ser um número válido.")
            return

        if alterar_nota(id_nota, novo_valor):
            messagebox.showinfo("Sucesso", "Nota alterada com sucesso!")
            self.aluno_id_entry.delete(0, tk.END)
            self.disciplina_id_entry.delete(0, tk.END)
            self.nota_entry.delete(0, tk.END)
            self.atualizar_lista_notas()


    def deletar_nota(self):
        selecao = self.lista_notas.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma nota para excluir.")
            return

        idx = selecao[0]
        item_selecionado = self.lista_notas.get(idx)
        try:
            id_nota_str = item_selecionado.split(' - ')[0].replace('ID: ', '')
            id_nota = int(id_nota_str)
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Não foi possível obter o ID da nota selecionada.")
            return

        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta nota?"):
            if excluir_nota(id_nota):
                messagebox.showinfo("Sucesso", "Nota excluída com sucesso!")
                self.aluno_id_entry.delete(0, tk.END)
                self.disciplina_id_entry.delete(0, tk.END)
                self.nota_entry.delete(0, tk.END)
                self.atualizar_lista_notas()

    # ------------------- Aba Exportar -------------------

    def criar_aba_exportar(self):
        aba = ttk.Frame(self.tabs, padding="20 20 20 20")
        self.tabs.add(aba, text='Exportar Dados')

        ttk.Label(aba, text="Opções de Exportação", font=('Arial', 12, 'bold')).pack(pady=20)
        ttk.Button(aba, text="Exportar para JSON", command=self.exportar_dados).pack(pady=10)
        ttk.Label(aba, text="Os dados serão salvos em 'dados_exportados.json' na mesma pasta do programa.").pack(pady=5)


    def exportar_dados(self):
        if exportar_dados_para_json():
            messagebox.showinfo("Exportado", "Dados exportados com sucesso para dados_exportados.json")