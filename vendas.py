
# -*- coding: cp1252 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import conexao
import datetime


def novo():
    con = conexao.conexao()
    sql_txt = "select IFNULL(max(codigo)+1,1) as codigo from vendas"
    rs = con.consultar(sql_txt)

    if rs:
        txtcodigo.insert(0, rs[0])

    # Preenche a data atual
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
    txtdata.insert(0, data_atual)

    # Limpa os outros campos
    txtcliente.delete(0, "end")
    lblnomecliente.config(text="")
    txtproduto.delete(0, "end")
    lblnomeproduto.config(text="")
    txtquantidade.delete(0, "end")
    txtpreco.delete(0, "end")
    txtobservacao.delete("1.0", "end")
    
    # Limpa a tabela de itens
    for item in tree_itens.get_children():
        tree_itens.delete(item)
    
    # Zera o total
    lbltotal.config(text="R$ 0,00")

    con.fechar()


def limpar():
    txtcodigo.delete(0, "end")
    txtdata.delete(0, "end")
    txtcliente.delete(0, "end")
    lblnomecliente.config(text="")
    txtproduto.delete(0, "end")
    lblnomeproduto.config(text="")
    txtquantidade.delete(0, "end")
    txtpreco.delete(0, "end")
    txtobservacao.delete("1.0", "end")
    
    # Limpa a tabela de itens
    for item in tree_itens.get_children():
        tree_itens.delete(item)
    
    # Zera o total
    lbltotal.config(text="R$ 0,00")
    
    txt_pes_codigo.delete(0, "end")
    novo()


def buscar_cliente():
    var_cliente = txtcliente.get()
    
    if not var_cliente:
        messagebox.showwarning("Aviso", "Digite um código de cliente", parent=tela_vendas)
        return
    
    con = conexao.conexao()
    sql_txt = f"select codigo, nome from clientes where codigo = {var_cliente}"
    rs = con.consultar(sql_txt)

    if rs:
        lblnomecliente.config(text=rs[1])
    else:
        messagebox.showwarning("Aviso", "Cliente não encontrado", parent=tela_vendas)
        txtcliente.delete(0, "end")
        lblnomecliente.config(text="")
    
    con.fechar()


def buscar_produto():
    var_produto = txtproduto.get()
    
    if not var_produto:
        messagebox.showwarning("Aviso", "Digite um código de produto", parent=tela_vendas)
        return
    
    con = conexao.conexao()
    sql_txt = f"select codigo, nome, preco from produtos where codigo = {var_produto}"
    rs = con.consultar(sql_txt)

    if rs:
        lblnomeproduto.config(text=rs[1])
        txtpreco.delete(0, "end")
        txtpreco.insert(0, rs[2])
        txtquantidade.focus_set()
    else:
        messagebox.showwarning("Aviso", "Produto não encontrado", parent=tela_vendas)
        txtproduto.delete(0, "end")
        lblnomeproduto.config(text="")
        txtpreco.delete(0, "end")
    
    con.fechar()


def adicionar_item():
    var_produto = txtproduto.get()
    var_quantidade = txtquantidade.get()
    var_preco = txtpreco.get().replace(",", ".")
    
    if not var_produto or not var_quantidade or not var_preco:
        messagebox.showwarning("Aviso", "Preencha todos os campos do item", parent=tela_vendas)
        return
    
    try:
        quantidade = float(var_quantidade)
        preco = float(var_preco)
        subtotal = quantidade * preco
    except ValueError:
        messagebox.showwarning("Aviso", "Valores inválidos", parent=tela_vendas)
        return
    
    # Busca o nome do produto
    nome_produto = lblnomeproduto.cget("text")
    
    # Adiciona o item na tabela
    tree_itens.insert("", tk.END, values=(var_produto, nome_produto, var_quantidade, f"R$ {preco:.2f}", f"R$ {subtotal:.2f}"))
    
    # Atualiza o total
    atualizar_total()
    
    # Limpa os campos do item
    txtproduto.delete(0, "end")
    lblnomeproduto.config(text="")
    txtquantidade.delete(0, "end")
    txtpreco.delete(0, "end")
    txtproduto.focus_set()


def remover_item():
    selecionado = tree_itens.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um item para remover", parent=tela_vendas)
        return
    
    tree_itens.delete(selecionado)
    atualizar_total()


def atualizar_total():
    total = 0.0
    
    for item in tree_itens.get_children():
        valores = tree_itens.item(item, "values")
        subtotal_str = valores[4].replace("R$ ", "").replace(",", ".")
        total += float(subtotal_str)
    
    lbltotal.config(text=f"R$ {total:.2f}")


def buscar_venda():
    var_codigo = txt_pes_codigo.get()
    
    if not var_codigo:
        messagebox.showwarning("Aviso", "Digite um código de venda", parent=tela_vendas)
        return
    
    limpar()
    
    con = conexao.conexao()
    
    # Busca a venda
    sql_txt = f"select codigo, data, cliente, total, observacao from vendas where codigo = {var_codigo}"
    rs = con.consultar(sql_txt)
    
    if not rs:
        messagebox.showwarning("Aviso", "Venda não encontrada", parent=tela_vendas)
        novo()
        return
    
    # Preenche os campos da venda
    txtcodigo.insert(0, rs[0])
    txtdata.insert(0, rs[1])
    txtcliente.insert(0, rs[2])
    txtobservacao.insert("1.0", rs[4])
    
    # Busca o nome do cliente
    sql_txt = f"select nome from clientes where codigo = {rs[2]}"
    rs_cliente = con.consultar(sql_txt)
    if rs_cliente:
        lblnomecliente.config(text=rs_cliente[0])
    
    # Busca os itens da venda
    sql_txt = f"""
    SELECT v.produto, p.nome, v.quantidade, v.precoUnitario, v.subtotal 
    FROM venda_itens v 
    JOIN produtos p ON v.produto = p.codigo 
    WHERE v.venda = {var_codigo}
    """
    
    rs_itens = con.consultar_tree(sql_txt)
    
    # Preenche a tabela de itens
    for item in rs_itens:
        tree_itens.insert("", tk.END, values=(
            item[0],  # código do produto
            item[1],  # nome do produto
            item[2],  # quantidade
            f"R$ {float(item[3]):.2f}",  # preço unitário
            f"R$ {float(item[4]):.2f}"   # subtotal
        ))
    
    # Atualiza o total
    lbltotal.config(text=f"R$ {float(rs[3]):.2f}")
    
    con.fechar()


def visualizar_vendas():
    con = conexao.conexao()
    sql_txt = "select v.codigo, v.data, c.nome, v.total from vendas v join clientes c on v.cliente = c.codigo order by v.codigo desc"
    rs = con.consultar_tree(sql_txt)

    for linha in tree_vendas.get_children():
        tree_vendas.delete(linha)
    
    for linha in rs:
        tree_vendas.insert("", tk.END, values=(
            linha[0],  # código
            linha[1],  # data
            linha[2],  # nome do cliente
            f"R$ {float(linha[3]):.2f}"  # total
        ))

    con.fechar()


def duplo_click_venda(event):
    selecionado = tree_vendas.selection()
    if not selecionado:
        return
    
    valores = tree_vendas.item(selecionado, "values")
    txt_pes_codigo.delete(0, "end")
    txt_pes_codigo.insert(0, valores[0])
    buscar_venda()


def gravar():
    var_codigo = txtcodigo.get()
    var_data = txtdata.get()
    var_cliente = txtcliente.get()
    var_observacao = txtobservacao.get("1.0", "end").strip()
    
    # Verifica os campos obrigatórios
    if not var_cliente or lblnomecliente.cget("text") == "":
        messagebox.showwarning("Aviso", "Selecione um cliente válido", parent=tela_vendas)
        return
    
    # Verifica se há itens na venda
    if len(tree_itens.get_children()) == 0:
        messagebox.showwarning("Aviso", "Adicione pelo menos um item à venda", parent=tela_vendas)
        return
    
    # Calcula o total da venda
    total_str = lbltotal.cget("text").replace("R$ ", "").replace(",", ".")
    total = float(total_str)
    
    con = conexao.conexao()
    
    try:
        # Inicia a transação
        con.db.start_transaction()
        
        # Verifica se é uma atualização ou nova venda
        sql_txt = f"select codigo from vendas where codigo = {var_codigo}"
        rs = con.consultar(sql_txt)
        
        if rs:
            # É uma atualização, primeiramente exclui os itens antigos
            sql_txt = f"delete from venda_itens where venda = {var_codigo}"
            con.gravar(sql_txt)
            
            # Atualiza a venda
            sql_txt = f"""
            update vendas set 
                data='{var_data}', 
                cliente={var_cliente}, 
                total={total}, 
                observacao='{var_observacao}'
            where codigo = {var_codigo}
            """
            con.gravar(sql_txt)
        else:
            # É uma nova venda
            sql_txt = f"""
            insert into vendas(codigo, data, cliente, total, observacao)
            values ({var_codigo}, '{var_data}', {var_cliente}, {total}, '{var_observacao}')
            """
            con.gravar(sql_txt)
        
        # Insere os itens da venda
        for item in tree_itens.get_children():
            valores = tree_itens.item(item, "values")
            
            produto = valores[0]
            quantidade = valores[2].replace(",", ".")
            preco = valores[3].replace("R$ ", "").replace(",", ".")
            subtotal = valores[4].replace("R$ ", "").replace(",", ".")
            
            sql_txt = f"""
            insert into venda_itens(venda, produto, quantidade, precoUnitario, subtotal)
            values ({var_codigo}, {produto}, {quantidade}, {preco}, {subtotal})
            """
            con.gravar(sql_txt)
            
            # Atualiza o estoque
            sql_txt = f"update produtos set estoque = estoque - {quantidade} where codigo = {produto}"
            con.gravar(sql_txt)
        
        # Finaliza a transação
        con.db.commit()
        
        messagebox.showinfo("Aviso", "Venda gravada com sucesso", parent=tela_vendas)
        limpar()
        visualizar_vendas()
        novo()
        
    except Exception as e:
        # Em caso de erro, reverte a transação
        con.db.rollback()
        messagebox.showerror("Erro", f"Erro ao gravar venda: {str(e)}", parent=tela_vendas)
    
    finally:
        con.fechar()


def excluir():
    var_del = messagebox.askyesno("Exclusão", "Tem certeza que deseja excluir esta venda?", parent=tela_vendas)
    if not var_del:
        return
    
    var_codigo = txtcodigo.get()
    if not var_codigo:
        messagebox.showwarning("Aviso", "Nenhuma venda selecionada", parent=tela_vendas)
        return
    
    con = conexao.conexao()
    
    try:
        # Inicia a transação
        con.db.start_transaction()
        
        # Recupera os itens da venda para devolver ao estoque
        sql_txt = f"select produto, quantidade from venda_itens where venda = {var_codigo}"
        rs_itens = con.consultar_tree(sql_txt)
        
        # Devolve os itens ao estoque
        for item in rs_itens:
            produto = item[0]
            quantidade = item[1]
            sql_txt = f"update produtos set estoque = estoque + {quantidade} where codigo = {produto}"
            con.gravar(sql_txt)
        
        # Exclui os itens da venda
        sql_txt = f"delete from venda_itens where venda = {var_codigo}"
        con.gravar(sql_txt)
        
        # Exclui a venda
        sql_txt = f"delete from vendas where codigo = {var_codigo}"
        con.gravar(sql_txt)
        
        # Finaliza a transação
        con.db.commit()
        
        messagebox.showinfo("Aviso", "Venda excluída com sucesso", parent=tela_vendas)
        limpar()
        visualizar_vendas()
        novo()
        
    except Exception as e:
        # Em caso de erro, reverte a transação
        con.db.rollback()
        messagebox.showerror("Erro", f"Erro ao excluir venda: {str(e)}", parent=tela_vendas)
    
    finally:
        con.fechar()


def menu():
    tela_vendas.destroy()


if __name__ == '__main__': 
    tela_vendas = tk.Tk()
else:
    tela_vendas = tk.Toplevel()
    
tela_vendas.geometry('1000x700+100+50')
# Método alternativo para maximizar a janela no Linux
tela_vendas.attributes('-zoomed', True) if hasattr(tela_vendas, 'attributes') else tela_vendas.state('zoomed')
tela_vendas.title("Controle Comercial 1.0 - Lançamento de Vendas")
tela_vendas['bg'] = "gold"

# Carrega a imagem de fundo
tkimage_vendas = ImageTk.PhotoImage(Image.open(r"fundo_submodulos.jpg").resize((tela_vendas.winfo_screenwidth(), tela_vendas.winfo_screenheight())))
tk.Label(tela_vendas, image=tkimage_vendas).pack()

# Frame para os campos da venda
frame_venda = tk.Frame(tela_vendas, bd=2, relief=tk.RIDGE, bg="whitesmoke")
frame_venda.place(x=50, y=50, width=900, height=180)

# Campos da venda
lblcodigo = tk.Label(frame_venda, text="Código:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblcodigo.place(x=10, y=10, width=60, height=25)

txtcodigo = tk.Entry(frame_venda, width=35, font=('Calibri', 12))
txtcodigo.place(x=80, y=10, width=100, height=25)

lbldata = tk.Label(frame_venda, text="Data:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lbldata.place(x=210, y=10, width=50, height=25)

txtdata = tk.Entry(frame_venda, width=35, font=('Calibri', 12))
txtdata.place(x=270, y=10, width=120, height=25)

lblcliente = tk.Label(frame_venda, text="Cliente:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblcliente.place(x=10, y=50, width=60, height=25)

txtcliente = tk.Entry(frame_venda, width=35, font=('Calibri', 12))
txtcliente.place(x=80, y=50, width=100, height=25)

btn_busca_cliente = tk.Button(frame_venda, text="Buscar", bg='white', foreground='black', 
                              font=('Calibri', 10, 'bold'), command=buscar_cliente)
btn_busca_cliente.place(x=190, y=50, width=70, height=25)

lblnomecliente = tk.Label(frame_venda, text="", bg="white", fg="black", font=('Calibri', 12), anchor="w")
lblnomecliente.place(x=270, y=50, width=300, height=25)

lblobservacao = tk.Label(frame_venda, text="Obs:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblobservacao.place(x=10, y=90, width=60, height=25)

txtobservacao = tk.Text(frame_venda, font=('Calibri', 12))
txtobservacao.place(x=80, y=90, width=490, height=70)

# Frame para os itens da venda
frame_itens = tk.Frame(tela_vendas, bd=2, relief=tk.RIDGE, bg="whitesmoke")
frame_itens.place(x=50, y=240, width=900, height=200)

# Campos dos itens
lblproduto = tk.Label(frame_itens, text="Produto:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblproduto.place(x=10, y=10, width=70, height=25)

txtproduto = tk.Entry(frame_itens, width=35, font=('Calibri', 12))
txtproduto.place(x=90, y=10, width=100, height=25)

btn_busca_produto = tk.Button(frame_itens, text="Buscar", bg='white', foreground='black', 
                             font=('Calibri', 10, 'bold'), command=buscar_produto)
btn_busca_produto.place(x=200, y=10, width=70, height=25)

lblnomeproduto = tk.Label(frame_itens, text="", bg="white", fg="black", font=('Calibri', 12), anchor="w")
lblnomeproduto.place(x=280, y=10, width=300, height=25)

lblquantidade = tk.Label(frame_itens, text="Qtde:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblquantidade.place(x=10, y=50, width=70, height=25)

txtquantidade = tk.Entry(frame_itens, width=35, font=('Calibri', 12))
txtquantidade.place(x=90, y=50, width=100, height=25)

lblpreco = tk.Label(frame_itens, text="Preço:", bg="whitesmoke", fg="black", font=('Calibri', 12), anchor="w")
lblpreco.place(x=200, y=50, width=70, height=25)

txtpreco = tk.Entry(frame_itens, width=35, font=('Calibri', 12))
txtpreco.place(x=280, y=50, width=100, height=25)

btn_adicionar = tk.Button(frame_itens, text="Adicionar Item", bg='blue', foreground='white', 
                         font=('Calibri', 12, 'bold'), command=adicionar_item)
btn_adicionar.place(x=400, y=50, width=120, height=25)

btn_remover = tk.Button(frame_itens, text="Remover Item", bg='red', foreground='white', 
                       font=('Calibri', 12, 'bold'), command=remover_item)
btn_remover.place(x=530, y=50, width=120, height=25)

# Tabela de itens da venda atual
style = ttk.Style()
style.configure("mystyle.Treeview", font=("Calibri", 10))
style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

tree_itens = ttk.Treeview(frame_itens, column=("c1", "c2", "c3", "c4", "c5"), show='headings', style="mystyle.Treeview")

tree_itens.column("#1")
tree_itens.heading("#1", text="Código")
tree_itens.column("#1", width=60, anchor='c')

tree_itens.column("#2")
tree_itens.heading("#2", text="Produto")
tree_itens.column("#2", width=300, anchor='c')

tree_itens.column("#3")
tree_itens.heading("#3", text="Qtde")
tree_itens.column("#3", width=60, anchor='c')

tree_itens.column("#4")
tree_itens.heading("#4", text="Preço")
tree_itens.column("#4", width=100, anchor='c')

tree_itens.column("#5")
tree_itens.heading("#5", text="Subtotal")
tree_itens.column("#5", width=100, anchor='c')

tree_itens.place(x=10, y=90, width=860, height=100)

scrollbar_itens = ttk.Scrollbar(frame_itens, orient=tk.VERTICAL, command=tree_itens.yview)
tree_itens.configure(yscroll=scrollbar_itens.set)
scrollbar_itens.place(x=870, y=90, height=100)

# Label para mostrar o total
lbltexto_total = tk.Label(tela_vendas, text="TOTAL:", bg="black", fg="white", font=('Calibri', 16, 'bold'))
lbltexto_total.place(x=650, y=450, width=100, height=30)

lbltotal = tk.Label(tela_vendas, text="R$ 0,00", bg="white", fg="blue", font=('Calibri', 16, 'bold'))
lbltotal.place(x=750, y=450, width=200, height=30)

# Botões da venda
btngravar = tk.Button(tela_vendas, text="Gravar Venda", 
                     bg='black', foreground='white', font=('Calibri', 12, 'bold'), command=gravar)
btngravar.place(x=50, y=450, width=120, height=30)

btnexcluir = tk.Button(tela_vendas, text="Excluir Venda", 
                      bg='red', foreground='white', font=('Calibri', 12, 'bold'), command=excluir)
btnexcluir.place(x=180, y=450, width=120, height=30)

btnlimpar = tk.Button(tela_vendas, text="Nova Venda", 
                     bg='green', foreground='white', font=('Calibri', 12, 'bold'), command=limpar)
btnlimpar.place(x=310, y=450, width=120, height=30)

btnmenu = tk.Button(tela_vendas, text="Menu", 
                   bg='yellow', foreground='black', font=('Calibri', 12, 'bold'), command=menu)
btnmenu.place(x=440, y=450, width=120, height=30)

# Campo de pesquisa para vendas existentes
lbl_pes_codigo = tk.Label(tela_vendas, text="Buscar Venda Nº:", font=('Calibri', 12, 'bold'), anchor="w")
lbl_pes_codigo.place(x=50, y=500, width=150, height=25)

txt_pes_codigo = tk.Entry(tela_vendas, width=35, font=('Calibri', 12))
txt_pes_codigo.place(x=200, y=500, width=100, height=25)

btn_pes_codigo = tk.Button(tela_vendas, text="Buscar", 
                          bg='white', foreground='black', font=('Calibri', 12, 'bold'), command=buscar_venda)
btn_pes_codigo.place(x=310, y=500, width=90, height=25)

# Tabela de vendas existentes
tree_vendas = ttk.Treeview(tela_vendas, column=("c1", "c2", "c3", "c4"), show='headings', style="mystyle.Treeview")

tree_vendas.column("#1")
tree_vendas.heading("#1", text="Código")
tree_vendas.column("#1", width=80, anchor='c')

tree_vendas.column("#2")
tree_vendas.heading("#2", text="Data")
tree_vendas.column("#2", width=100, anchor='c')

tree_vendas.column("#3")
tree_vendas.heading("#3", text="Cliente")
tree_vendas.column("#3", width=300, anchor='c')

tree_vendas.column("#4")
tree_vendas.heading("#4", text="Total")
tree_vendas.column("#4", width=100, anchor='c')

tree_vendas.place(x=50, y=540, width=900, height=150)
tree_vendas.bind("<Double-1>", duplo_click_venda)

scrollbar_vendas = ttk.Scrollbar(tela_vendas, orient=tk.VERTICAL, command=tree_vendas.yview)
tree_vendas.configure(yscroll=scrollbar_vendas.set)
scrollbar_vendas.place(x=950, y=540, height=150)

# Inicializa a tela
novo()
visualizar_vendas()

if __name__ == '__main__':
    tela_vendas.mainloop()