import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def conectar():
    return sqlite3.connect('teste.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
       CREATE TABLE IF NOT EXISTS usuarios(
       telefone TEXT PRIMARY KEY,
       nome TEXT NOT NULL,
       email TEXT NOT NULL,
       endereco TEXT NOT NULL                          
       ) 
    ''')
    conn.commit()
    conn.close()

def inserir_usuario():
    nome = entry_nome.get()
    email = entry_email.get()    
    endereco = entry_endereco.get()
    telefone = entry_telefone.get()

    if nome and email and telefone:
        try:
            conn = conectar()
            c = conn.cursor()
            c.execute('INSERT INTO usuarios(telefone, nome, email, endereco) VALUES (?, ?, ?, ?)', 
                      (telefone, nome, email, endereco))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso.')
            mostrar_usuario()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'Telefone já cadastrado.')
    else:
        messagebox.showerror('Erro', 'Preencha todos os campos.')

def mostrar_usuario():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    for cliente in usuarios:
        tree.insert("", "end", values=cliente)
    conn.close()

def delete_usuario():
    dados_del = tree.selection()
    if dados_del:
        telefone = tree.item(dados_del)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM usuarios WHERE telefone = ?', (telefone,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Registro deletado.')
        mostrar_usuario()
    else:
        messagebox.showerror('Erro', 'Selecione um registro para deletar.')

def editar():
    selecao = tree.selection()
    if selecao:
        telefone_original = tree.item(selecao)['values'][0]

        novo_nome = entry_nome.get()
        novo_email = entry_email.get()
        novo_endereco = entry_endereco.get()
        novo_telefone = entry_telefone.get()

        if novo_nome and novo_email and novo_telefone:
            conn = conectar()
            c = conn.cursor()
            c.execute('''
                UPDATE usuarios 
                SET nome = ?, email = ?, endereco = ?, telefone = ?
                WHERE telefone = ?
            ''', (novo_nome, novo_email, novo_endereco, novo_telefone, telefone_original))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Registro atualizado.')
            mostrar_usuario()
        else:
            messagebox.showerror('Erro', 'Preencha todos os campos.')
    else:
        messagebox.showwarning('Aviso', 'Selecione um registro para editar.')

# Interface gráfica
janela = tk.Tk()
janela.configure(bg="#664242")
janela.title('CRUD')
janela.geometry('1080x720')

TITULO = tk.Label(janela, text='CADASTRO de CLIENTES', fg='black', font=('roboto', 20, 'bold'), bg="#664242")
TITULO.grid(row=0, column=1, padx=10, pady=10)

label_nome = tk.Label(janela, text='NOME: ', font=('arial', 15), bg="#664242", fg="white")
label_nome.grid(row=1, column=0, padx=10, pady=10)

entry_nome = tk.Entry(janela, font=('arial', 15))
entry_nome.grid(row=1, column=1, padx=10, pady=10)
#---------------------------------------------------------------------------------------------------------
label_endereco = tk.Label(janela, text='ENDEREÇO: ', font=('arial', 15), bg="#664242", fg="white")
label_endereco.grid(row=2, column=0, padx=10, pady=10)

entry_endereco = tk.Entry(janela, font=('arial', 15))
entry_endereco.grid(row=2, column=1, padx=10, pady=10)
#---------------------------------------------------------------------------------------------------------
label_email = tk.Label(janela, text='E-MAIL: ', font=('arial', 15), bg="#664242", fg="white")
label_email.grid(row=3, column=0, padx=10, pady=10)

entry_email = tk.Entry(janela, font=('arial', 15))
entry_email.grid(row=3, column=1, padx=10, pady=10)
#-----------------------------------------------------------------------------------------------------------
label_telefone = tk.Label(janela, text='TELEFONE: ', font=('arial', 15), bg="#664242", fg="white")
label_telefone.grid(row=4, column=0, padx=10, pady=10)

entry_telefone = tk.Entry(janela, font=('arial', 15))
entry_telefone.grid(row=4, column=1, padx=10, pady=10)
#------------------------------------------------------------------------------------------------------------

btn_salvar = tk.Button(janela, text='Salvar', font=('arial', 15), command=inserir_usuario)
btn_salvar.grid(row=5, column=0, padx=5, pady=10)

btn_editar = tk.Button(janela, text='Editar', font=('arial', 15), command=editar)
btn_editar.grid(row=5, column=1, padx=5, pady=10)

btn_Deletar = tk.Button(janela, text='Deletar', font=('arial', 15), command=delete_usuario)
btn_Deletar.grid(row=5, column=2, padx=5, pady=10)

columns = ('TELEFONE', 'NOME', 'E-MAIL', 'ENDEREÇO')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_usuario()
janela.mainloop()