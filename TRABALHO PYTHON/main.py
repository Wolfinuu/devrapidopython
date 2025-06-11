import tkinter as tk
from database import criar_tabelas
from gui import App

if __name__ == "__main__":
    criar_tabelas()  # Garante que as tabelas sejam criadas
    root = tk.Tk()
    app = App(root)
    root.mainloop()