import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import conexao


def novo():
    con = conexao.conexao()
    sql_txt = "select IFNULL(max(codigo)+1,1) as codigo from produtos"
    rs = con.consultar(sql_txt)

    if rs:
        txtcodigo.insert(0, rs[0])

    con.fechar()
    txtnome.focus_set()


def limpar():
    txtcodigo.delete(0, "end")
    txtnome.delete(0, "end")
    txtpreco.delete(0, "end")
    txtcategoria.delete(0, "end")
    txtdescricao.delete("1.0", "end")
    txtestoque.delete(0, "end")
    txt_pes_nome.delete(0, "end")
    novo()


def buscar():
    var_codigo = txtcodigo.get()
    txtcodigo.delete(0, "end")
 
    con = conexao.conexao()
    sql_txt = f"select codigo, nome, preco, categoria, descricao, estoque from produtos where codigo = {var_codigo}"
    rs = con.consultar(sql_txt)

    if rs:
        txtcodigo.insert(0, rs[0])
        txtnome.insert(0, rs[1])
        txtpreco.insert(0, rs[2])
        txtcategoria.insert(0, rs[3])
        txtdescricao.insert("1.0", rs[4])
        txtestoque.insert(0, rs[5])
    
    else:
        messagebox.showwarning("Aviso", "Código não Encontrado", parent=tela_prod)
        limpar()
        txtcodigo.focus_set()

    con.fechar()


def duplo_click(event):
    limpar()
    item = tree.selection()[0]
    valores = tree.item(item, "values")
    txtcodigo.delete(0, "end")
    txtcodigo.insert(0, valores[0])
    buscar()


def visualizar():
    con = conexao.conexao()
    sql_txt = "select codigo, nome, preco, categoria, estoque from produtos"
    rs = con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()


def pesquisar_nome(p):
    con = conexao.conexao()
    sql_txt = f"select codigo, nome, preco, categoria, estoque from produtos where nome like '%{p}%'"
    
    rs = con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()   

    return True


def gravar():
    var_codigo = txtcodigo.get()
    var_nome = txtnome.get()
    var_preco = txtpreco.get().replace(",", ".")
    var_categoria = txtcategoria.get()
    var_descricao = txtdescricao.get("1.0", "end").strip()
    var_estoque = txtestoque.get()

    con = conexao.conexao()
    sql_txt = f"select codigo from produtos where codigo = {var_codigo}"

    rs = con.consultar(sql_txt)

    if rs:
        sql_text = f"update produtos set nome='{var_nome}', preco={var_preco}, categoria='{var_categoria}', descricao='{var_descricao}', estoque={var_estoque} where codigo = {var_codigo}"
    else:
        sql_text = f"insert into produtos(codigo, nome, preco, categoria, descricao, estoque) values ({var_codigo}, '{var_nome}', {var_preco}, '{var_categoria}', '{var_descricao}', {var_estoque})"

    if con.gravar(sql_text):
        messagebox.showinfo("Aviso", "Item Gravado com Sucesso", parent=tela_prod)
        limpar()
    else:
        messagebox.showerror("Erro", "Houve um Erro na Gravação", parent=tela_prod)

    con.fechar()
    visualizar()


def excluir():
    var_del = messagebox.askyesno("Exclusão", "Tem certeza que deseja excluir?", parent=tela_prod)
    if var_del:
        var_codigo = txtcodigo.get()

        con = conexao.conexao()
        sql_text = f"delete from produtos where codigo = {var_codigo}"
        if con.gravar(sql_text):
            messagebox.showinfo("Aviso", "Item Excluído com Sucesso", parent=tela_prod)
            limpar()
        else:
            messagebox.showerror("Erro", "Houve um Erro na Exclusão", parent=tela_prod)
            
        con.fechar()
        visualizar()
    else:
        limpar()


def menu():
    tela_prod.destroy()


if __name__ == '__main__': 
    tela_prod = tk.Tk()
else:
    tela_prod = tk.Toplevel()

pes_nome = tela_prod.register(func=pesquisar_nome)
    
tela_prod.geometry('950x600+100+100')
# Método alternativo para maximizar a janela no Linux
tela_prod.attributes('-zoomed', True) if hasattr(tela_prod, 'attributes') else tela_prod.state('zoomed')
tela_prod.title("Controle Comercial 1.0 - Cadastro de Produtos/Serviços")
tela_prod['bg'] = "gold"

# Carrega a imagem de fundo
tkimage_prod = ImageTk.PhotoImage(Image.open(r"fundo_submodulos.jpg").resize((tela_prod.winfo_screenwidth(), tela_prod.winfo_screenheight())))
tk.Label(tela_prod, image=tkimage_prod).pack()

# Campo código
lblcodigo = tk.Label(tela_prod, text="Código:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblcodigo.place(x=50, y=60, width=85, height=25)

txtcodigo = tk.Entry(tela_prod, width=35, font=('Calibri', 12))
txtcodigo.place(x=150, y=60, width=100, height=25)

buscabtn = tk.Button(tela_prod, text="Pesquisar", 
                    bg='white', foreground='black', font=('Calibri', 12, 'bold'), command=buscar)
buscabtn.place(x=280, y=60, width=90, height=25)

# Campo nome
lblnome = tk.Label(tela_prod, text="Nome:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblnome.place(x=50, y=100, width=85, height=25)

txtnome = tk.Entry(tela_prod, width=35, font=('Calibri', 12))
txtnome.place(x=150, y=100, width=350, height=25)

# Campo preço
lblpreco = tk.Label(tela_prod, text="Preço:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblpreco.place(x=50, y=140, width=85, height=25)

txtpreco = tk.Entry(tela_prod, width=35, font=('Calibri', 12))
txtpreco.place(x=150, y=140, width=150, height=25)

# Campo categoria
lblcategoria = tk.Label(tela_prod, text="Categoria:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblcategoria.place(x=310, y=140, width=85, height=25)

txtcategoria = tk.Entry(tela_prod, width=35, font=('Calibri', 12))
txtcategoria.place(x=400, y=140, width=150, height=25)

# Campo descrição
lbldescricao = tk.Label(tela_prod, text="Descrição:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lbldescricao.place(x=50, y=180, width=85, height=25)

txtdescricao = tk.Text(tela_prod, font=('Calibri', 12))
txtdescricao.place(x=150, y=180, width=350, height=60)

# Campo estoque
lblestoque = tk.Label(tela_prod, text="Estoque:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblestoque.place(x=50, y=250, width=85, height=25)

txtestoque = tk.Entry(tela_prod, width=35, font=('Calibri', 12))
txtestoque.place(x=150, y=250, width=100, height=25)

# Campo de pesquisa
lbl_pes_nome = tk.Label(tela_prod, text="Pesquisar por Nome:", font=('Calibri', 12, 'bold'), anchor="w")
lbl_pes_nome.place(x=50, y=390, width=150, height=25)

txt_pes_nome = tk.Entry(tela_prod, width=35, font=('Calibri', 12), validate='key', validatecommand=(pes_nome, '%P'))
txt_pes_nome.place(x=210, y=390, width=300, height=25)

# Botões
btngravar = tk.Button(tela_prod, text="Gravar", 
                     bg='black', foreground='white', font=('Calibri', 12, 'bold'), command=gravar)
btngravar.place(x=150, y=320, width=65)

btnexcluir = tk.Button(tela_prod, text="Excluir", 
                      bg='red', foreground='white', font=('Calibri', 12, 'bold'), command=excluir)
btnexcluir.place(x=250, y=320, width=65)

btnlimpar = tk.Button(tela_prod, text="Limpar", 
                     bg='green', foreground='white', font=('Calibri', 12, 'bold'), command=limpar)
btnlimpar.place(x=350, y=320, width=65)

btnmenu = tk.Button(tela_prod, text="Menu", 
                   bg='yellow', foreground='black', font=('Calibri', 12, 'bold'), command=menu)
btnmenu.place(x=450, y=320, width=65)

# Configuração da TreeView
style = ttk.Style()
style.configure("mystyle.Treeview", font=("Calibri", 10))
style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

tree = ttk.Treeview(tela_prod, column=("c1", "c2", "c3", "c4", "c5"), show='headings', style="mystyle.Treeview")

tree.column("#1")
tree.heading("#1", text="Código")
tree.column("#1", width=80, anchor='c')

tree.column("#2")
tree.heading("#2", text="Nome")
tree.column("#2", width=250, anchor='c')

tree.column("#3")
tree.heading("#3", text="Preço")
tree.column("#3", width=100, anchor='c')

tree.column("#4")
tree.heading("#4", text="Categoria")
tree.column("#4", width=150, anchor='c')

tree.column("#5")
tree.heading("#5", text="Estoque")
tree.column("#5", width=100, anchor='c')

tree.place(x=50, y=420, height=120, width=700)

scrollbar = ttk.Scrollbar(tela_prod, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.place(x=750, y=420, height=120)

# Inicializa a tela
visualizar()
novo()

if __name__ == '__main__':
    tela_prod.mainloop()