# -*- coding: cp1252 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import conexao


def novo():
    con=conexao.conexao()
    sql_txt = f"select IFNULL(max(codigo)+1,1) as codigo from clientes"
    rs=con.consultar(sql_txt)

    if rs:
        txtcodigo.insert(0, rs[0])

    con.fechar()
    txtnome.focus_set()

def limpar():
    txtcodigo.delete(0,"end")
    txtnome.delete(0,"end")
    txttelefone.delete(0,"end")
    txtemail.delete(0,"end")
    txtobservacao.delete("1.0","end")
    txt_pes_nome.delete(0,"end")
    novo()

def buscar():
    var_codigo = txtcodigo.get()
    txtcodigo.delete(0,"end")
 
    con=conexao.conexao()
    sql_txt = f"select codigo,nome,telefone,email,observacao from clientes where codigo = {var_codigo}"
    rs=con.consultar(sql_txt)

    if rs:
    
        txtcodigo.insert(0, rs[0])
        txtnome.insert(0, rs[1])
        txttelefone.insert(0,rs[2])
        txtemail.insert(0,rs[3])
        txtobservacao.insert("1.0",(rs[4]))
    
    else:
        messagebox.showwarning("Aviso", "Código não Encontrado",parent = tela_cli)
        limpar()
        txtcodigo.focus_set()

    con.fechar()

def duplo_click(event):
    limpar()
    item = tree.item(tree.selection())
    txtcodigo.delete(0,"end")
    txtcodigo.insert(0, item['values'][0])
    buscar()

def visualizar():
    con=conexao.conexao()
    sql_txt = f"select * from clientes "
    rs=con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()

def pesquisar_nome(p):
    con=conexao.conexao()
    sql_txt = f"select * from clientes where nome like '%{p}%'"
    
    rs=con.consultar_tree(sql_txt)

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
    var_telefone = txttelefone.get()
    var_email = txtemail.get()
    var_observacao = txtobservacao.get("1.0","end")


    con=conexao.conexao()
    sql_txt = f"select codigo,nome,telefone,email,observacao from clientes where codigo = {var_codigo}"

    rs=con.consultar(sql_txt)

    if rs:
        sql_text = f"update clientes set nome='{var_nome}',telefone='{var_telefone}',email='{var_email}',observacao='{var_observacao}' where codigo = '{var_codigo}'"
    else:
        sql_text = f"insert into clientes(codigo,nome,telefone,email,observacao) values ({var_codigo},'{var_nome}','{var_telefone}','{var_email}','{var_observacao}')"

    print(sql_text)
    if con.gravar(sql_text):
        messagebox.showinfo("Aviso", "Item Gravado com Sucesso", parent = tela_cli)
        limpar()
    else:
        messagebox.showerror("Erro", "Houve um Erro na Gravação", parent = tela_cli)

    con.fechar()

    visualizar()

def excluir():
    var_del = messagebox.askyesno("Exclusão", "Tem certeza que deseja excluir?", parent = tela_cli)
    if var_del == True:
        var_codigo = txtcodigo.get()

        con=conexao.conexao()
        sql_text = f"delete from clientes where codigo = '{var_codigo}'"
        if con.gravar(sql_text):
              messagebox.showinfo("Aviso", "Item Excluído com Sucesso",parent = tela_cli)
              limpar()
        else:
            messagebox.showerror("Erro", "Houve um Erro na Exclusão",parent = tela_cli)

            
        con.fechar()

        visualizar()
        limpar()
    else:
        limpar()


def menu():
    tela_cli.destroy()

if __name__ == '__main__': 
    tela_cli = tk.Tk()
else:
    tela_cli = tk.Toplevel()

pes_nome = tela_cli.register(func=pesquisar_nome)
    
tela_cli.geometry('950x600+100+100')
# Método alternativo para maximizar a janela no Linux
tela_cli.attributes('-zoomed', True) if hasattr(tela_cli, 'attributes') else tela_cli.state('zoomed')
tela_cli.title("Controle Comercial 1.0 - Cadastro de Clientes")
tela_cli['bg'] = "gold"


tkimage_cli = ImageTk.PhotoImage(Image.open(r"fundo_submodulos.jpg").resize((tela_cli.winfo_screenwidth(), tela_cli.winfo_screenheight())))
tk.Label(tela_cli, image=tkimage_cli).pack()


lblcodigo = tk.Label(tela_cli, text ="Codigo:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor = "w")
lblcodigo.place(x = 50, y = 60, width=85, height = 25)

txtcodigo = tk.Entry(tela_cli, width = 35, font=('Calibri', 12))
txtcodigo.place(x = 150, y = 60, width = 100, height = 25)

buscabtn = tk.Button(tela_cli, text ="Pesquisar", 
                      bg ='white',foreground='black', font=('Calibri', 12, 'bold'), command = buscar)
buscabtn.place(x = 280, y = 60, width = 90, height = 25)

lblnome = tk.Label(tela_cli, text ="Nome:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor = "w")
lblnome.place(x = 50, y = 100, width=85, height = 25)

txtnome = tk.Entry(tela_cli, width = 35, font=('Calibri', 12))
txtnome.place(x = 150, y = 100, width = 360, height = 25)

lbltelefone = tk.Label(tela_cli, text ="Telefone:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor = "w")
lbltelefone.place(x = 50, y = 140, width=85, height = 25)

txttelefone = tk.Entry(tela_cli, width = 35, font=('Calibri', 12))
txttelefone.place(x = 150, y = 140, width = 360, height = 25)

lblemail = tk.Label(tela_cli, text ="E-mail:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor = "w")
lblemail.place(x = 50, y = 180, width=85, height = 25)

txtemail = tk.Entry(tela_cli, width = 35, font=('Calibri', 12))
txtemail.place(x = 150, y = 180, width = 360, height = 25)

lblobservacao = tk.Label(tela_cli, text ="Observacao:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor = "w")
lblobservacao.place(x = 50, y = 220, width=85, height = 25)

txtobservacao= tk.Text(tela_cli, font=('Calibri', 12))
txtobservacao.place(x=150, y=220, width=360, height=80)

lbl_pes_nome = tk.Label(tela_cli, text ="Pesquisar por Nome :", font=('Calibri', 12, 'bold'), anchor = "w")
lbl_pes_nome.place(x = 50, y = 390, width=200, height = 25)
txt_pes_nome = tk.Entry(tela_cli, width = 35, font=('Calibri', 12),validate='key', validatecommand=(pes_nome,'%P'))
txt_pes_nome.place(x = 210, y = 390, width = 360, height = 25)

btngravar = tk.Button(tela_cli, text ="Gravar", 
                       bg ='black',foreground='white', font=('Calibri', 12, 'bold'), command = gravar)
btngravar.place(x = 150, y = 320, width = 65)

btnexcluir = tk.Button(tela_cli, text ="Excluir", 
                       bg ='red',foreground='white', font=('Calibri', 12, 'bold'), command = excluir)
btnexcluir.place(x = 250, y = 320, width = 65)

btnlimpar = tk.Button(tela_cli, text ="Limpar", 
                       bg ='green',foreground='white', font=('Calibri', 12, 'bold'), command = limpar)
btnlimpar.place(x = 350, y = 320, width = 65)

btnmenu = tk.Button(tela_cli, text ="Menu", 
                       bg ='yellow',foreground='black', font=('Calibri', 12, 'bold'), command=menu)
btnmenu.place(x = 450, y = 320, width = 65)

style = ttk.Style()
style.configure("mystyle.Treeview", font=("Calibri", 10))
style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

tree = ttk.Treeview(tela_cli, column=("c1", "c2", "c3", "c4", "c5"), show='headings', style="mystyle.Treeview")

tree.column("#1")
tree.heading("#1", text="Código")
tree.column("#1", width = 100, anchor ='c')

tree.column("#2")
tree.heading("#2", text="Nome")
tree.column("#2", width = 200, anchor ='c')

tree.column("#3")
tree.heading("#3", text="Telefone")
tree.column("#3", width = 100, anchor ='w')

tree.column("#4")
tree.heading("#4", text="E-mail")
tree.column("#4", width = 150, anchor ='c')

tree.column("#5")
tree.heading("#5", text="Observação")
tree.column("#5", width = 300, anchor ='c')

tree.place(x=50,y=420,height=120)

scrollbar = ttk.Scrollbar(tela_cli, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.place(x = 901, y = 420,height=120)

visualizar()
novo()

tela_cli.mainloop()