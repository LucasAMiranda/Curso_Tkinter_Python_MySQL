import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import conexao


def novo():
    con = conexao.conexao()
    sql_txt = "select IFNULL(max(id)+1,1) as id from usuarios"
    rs = con.consultar(sql_txt)

    if rs:
        txtid.insert(0, rs[0])

    con.fechar()
    txtusername.focus_set()


def limpar():
    txtid.delete(0, "end")
    txtusername.delete(0, "end")
    txtnome.delete(0, "end")
    combo_funcao.current(0)
    txtsenha.delete(0, "end")
    txtconfirmarsenha.delete(0, "end")
    txt_pes_usuario.delete(0, "end")
    novo()


def buscar():
    var_id = txtid.get()
    txtid.delete(0, "end")
 
    con = conexao.conexao()
    sql_txt = f"select id, username, nome, funcao, senha from usuarios where id = {var_id}"
    rs = con.consultar(sql_txt)

    if rs:
        txtid.insert(0, rs[0])
        txtusername.insert(0, rs[1])
        txtnome.insert(0, rs[2])
        
        # Define a função no combobox baseado no valor do banco
        if rs[3] == "admin":
            combo_funcao.current(0)
        elif rs[3] == "gerente":
            combo_funcao.current(1)
        elif rs[3] == "vendedor":
            combo_funcao.current(2)
        else:
            combo_funcao.current(3)
            
        # Não exibe a senha por segurança, apenas preenche um placeholder
        txtsenha.insert(0, "********")
        txtconfirmarsenha.insert(0, "********")
    
    else:
        messagebox.showwarning("Aviso", "Usuário não Encontrado", parent=tela_acesso)
        limpar()
        txtid.focus_set()

    con.fechar()


def duplo_click(event):
    limpar()
    item = tree.selection()[0]
    valores = tree.item(item, "values")
    txtid.delete(0, "end")
    txtid.insert(0, valores[0])
    buscar()


def toggle_status(event=None):
    if not tree.selection():
        return
        
    item = tree.selection()[0]
    valores = tree.item(item, "values")
    usuario_id = valores[0]
    status_atual = valores[4]  # Assume que a coluna de status é a quinta
    
    novo_status = "inativo" if status_atual == "ativo" else "ativo"
    
    con = conexao.conexao()
    sql_txt = f"UPDATE usuarios SET ativo = '{novo_status}' WHERE id = {usuario_id}"
    
    if con.gravar(sql_txt):
        messagebox.showinfo("Aviso", "Status atualizado com sucesso", parent=tela_acesso)
        visualizar()
    else:
        messagebox.showerror("Erro", "Falha ao atualizar status", parent=tela_acesso)
    
    con.fechar()


def visualizar():
    con = conexao.conexao()
    sql_txt = "select id, username, nome, funcao, ativo from usuarios"
    rs = con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()


def pesquisar_usuario(p):
    con = conexao.conexao()
    sql_txt = f"select id, username, nome, funcao, ativo from usuarios where username like '%{p}%' or nome like '%{p}%'"
    
    rs = con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()   

    return True


def gravar():
    var_id = txtid.get()
    var_username = txtusername.get()
    var_nome = txtnome.get()
    var_funcao = combo_funcao.get()  # Obtém o texto selecionado
    var_senha = txtsenha.get()
    var_confirmarsenha = txtconfirmarsenha.get()

    # Mapeia o texto da função para o valor armazenado no banco
    if var_funcao == "Administrador":
        var_funcao_db = "admin"
    elif var_funcao == "Gerente":
        var_funcao_db = "gerente"
    elif var_funcao == "Vendedor":
        var_funcao_db = "vendedor"
    else:
        var_funcao_db = "usuario"

    # Verifica se as senhas coincidem
    if var_senha != var_confirmarsenha:
        messagebox.showerror("Erro", "As senhas não coincidem", parent=tela_acesso)
        return

    # Verifica se é necessário atualizar a senha
    con = conexao.conexao()
    sql_txt = f"select id, username, senha from usuarios where id = {var_id}"
    rs = con.consultar(sql_txt)

    if rs:
        # Atualização de usuário existente
        if var_senha == "********" or not var_senha:
            # Mantém a senha atual
            sql_text = f"update usuarios set username='{var_username}', nome='{var_nome}', funcao='{var_funcao_db}' where id = {var_id}"
        else:
            # Atualiza com a nova senha
            sql_text = f"update usuarios set username='{var_username}', nome='{var_nome}', funcao='{var_funcao_db}', senha='{var_senha}' where id = {var_id}"
    else:
        # Criação de novo usuário
        if not var_senha:
            messagebox.showerror("Erro", "A senha é obrigatória para novos usuários", parent=tela_acesso)
            return
        sql_text = f"insert into usuarios(id, username, nome, funcao, senha, ativo) values ({var_id}, '{var_username}', '{var_nome}', '{var_funcao_db}', '{var_senha}', 'ativo')"

    if con.gravar(sql_text):
        messagebox.showinfo("Aviso", "Usuário salvo com sucesso", parent=tela_acesso)
        limpar()
    else:
        messagebox.showerror("Erro", "Houve um erro na gravação", parent=tela_acesso)

    con.fechar()
    visualizar()


def excluir():
    var_del = messagebox.askyesno("Exclusão", "Tem certeza que deseja excluir?", parent=tela_acesso)
    if var_del:
        var_id = txtid.get()

        con = conexao.conexao()
        sql_text = f"delete from usuarios where id = {var_id}"
        if con.gravar(sql_text):
            messagebox.showinfo("Aviso", "Usuário excluído com sucesso", parent=tela_acesso)
            limpar()
        else:
            messagebox.showerror("Erro", "Houve um erro na exclusão", parent=tela_acesso)
            
        con.fechar()
        visualizar()
        limpar()
    else:
        limpar()


def menu():
    tela_acesso.destroy()


if __name__ == '__main__': 
    tela_acesso = tk.Tk()
else:
    tela_acesso = tk.Toplevel()

pes_usuario = tela_acesso.register(func=pesquisar_usuario)
    
tela_acesso.geometry('950x600+100+100')
# Método alternativo para maximizar a janela no Linux
tela_acesso.attributes('-zoomed', True) if hasattr(tela_acesso, 'attributes') else tela_acesso.state('zoomed')
tela_acesso.title("Controle Comercial 1.0 - Gestão de Acessos")
tela_acesso['bg'] = "gold"

# Carrega a imagem de fundo
tkimage_acesso = ImageTk.PhotoImage(Image.open(r"fundo_submodulos.jpg").resize((tela_acesso.winfo_screenwidth(), tela_acesso.winfo_screenheight())))
tk.Label(tela_acesso, image=tkimage_acesso).pack()

# Campo ID
lblid = tk.Label(tela_acesso, text="ID:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblid.place(x=50, y=60, width=120, height=25)

txtid = tk.Entry(tela_acesso, width=35, font=('Calibri', 12))
txtid.place(x=180, y=60, width=100, height=25)

buscabtn = tk.Button(tela_acesso, text="Pesquisar", 
                     bg='white', foreground='black', font=('Calibri', 12, 'bold'), command=buscar)
buscabtn.place(x=290, y=60, width=90, height=25)

# Campo Nome de Usuário
lblusername = tk.Label(tela_acesso, text="Nome de Usuário:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblusername.place(x=50, y=100, width=120, height=25)

txtusername = tk.Entry(tela_acesso, width=35, font=('Calibri', 12))
txtusername.place(x=180, y=100, width=200, height=25)

# Campo Nome Completo
lblnome = tk.Label(tela_acesso, text="Nome Completo:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblnome.place(x=50, y=140, width=120, height=25)

txtnome = tk.Entry(tela_acesso, width=35, font=('Calibri', 12))
txtnome.place(x=180, y=140, width=300, height=25)

# Campo Função
lblfuncao = tk.Label(tela_acesso, text="Função:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblfuncao.place(x=50, y=180, width=120, height=25)

combo_funcao = ttk.Combobox(tela_acesso, values=["Administrador", "Gerente", "Vendedor", "Usuário"], font=('Calibri', 12))
combo_funcao.place(x=180, y=180, width=200, height=25)
combo_funcao.current(0)  # Define o valor padrão

# Campo Senha
lblsenha = tk.Label(tela_acesso, text="Senha:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblsenha.place(x=50, y=220, width=120, height=25)

txtsenha = tk.Entry(tela_acesso, width=35, font=('Calibri', 12), show="*")
txtsenha.place(x=180, y=220, width=200, height=25)

# Campo Confirmar Senha
lblconfirmarsenha = tk.Label(tela_acesso, text="Confirmar Senha:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblconfirmarsenha.place(x=50, y=260, width=120, height=25)

txtconfirmarsenha = tk.Entry(tela_acesso, width=35, font=('Calibri', 12), show="*")
txtconfirmarsenha.place(x=180, y=260, width=200, height=25)

# Campo de Pesquisa
lbl_pes_usuario = tk.Label(tela_acesso, text="Pesquisar:", font=('Calibri', 12, 'bold'), anchor="w")
lbl_pes_usuario.place(x=50, y=390, width=100, height=25)

txt_pes_usuario = tk.Entry(tela_acesso, width=35, font=('Calibri', 12), validate='key', validatecommand=(pes_usuario, '%P'))
txt_pes_usuario.place(x=160, y=390, width=300, height=25)

# Botões
btngravar = tk.Button(tela_acesso, text="Salvar", 
                     bg='black', foreground='white', font=('Calibri', 12, 'bold'), command=gravar)
btngravar.place(x=180, y=310, width=65)

btnexcluir = tk.Button(tela_acesso, text="Excluir", 
                     bg='red', foreground='white', font=('Calibri', 12, 'bold'), command=excluir)
btnexcluir.place(x=260, y=310, width=65)

btnlimpar = tk.Button(tela_acesso, text="Limpar", 
                     bg='green', foreground='white', font=('Calibri', 12, 'bold'), command=limpar)
btnlimpar.place(x=340, y=310, width=65)

btnmenu = tk.Button(tela_acesso, text="Menu", 
                   bg='yellow', foreground='black', font=('Calibri', 12, 'bold'), command=menu)
btnmenu.place(x=420, y=310, width=65)

# Configuração da TreeView
style = ttk.Style()
style.configure("mystyle.Treeview", font=("Calibri", 10))
style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

tree = ttk.Treeview(tela_acesso, column=("c1", "c2", "c3", "c4", "c5"), show='headings', style="mystyle.Treeview")

tree.column("#1")
tree.heading("#1", text="ID")
tree.column("#1", width=50, anchor='c')

tree.column("#2")
tree.heading("#2", text="Nome de Usuário")
tree.column("#2", width=150, anchor='c')

tree.column("#3")
tree.heading("#3", text="Nome Completo")
tree.column("#3", width=200, anchor='c')

tree.column("#4")
tree.heading("#4", text="Função")
tree.column("#4", width=100, anchor='c')

tree.column("#5")
tree.heading("#5", text="Status")
tree.column("#5", width=80, anchor='c')

tree.place(x=50, y=420, height=120, width=850)

# Botão de alternar status
btn_status = tk.Button(tela_acesso, text="Alternar Status", 
                     bg='blue', foreground='white', font=('Calibri', 10, 'bold'), command=toggle_status)
btn_status.place(x=470, y=390, width=120, height=25)

scrollbar = ttk.Scrollbar(tela_acesso, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.place(x=900, y=420, height=120)

# Inicializa a tela
visualizar()
novo()

if __name__ == '__main__':
    tela_acesso.mainloop()