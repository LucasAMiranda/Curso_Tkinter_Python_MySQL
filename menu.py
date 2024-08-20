# -*- coding: cp1252 -*-
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

tela = tk.Tk()
tela.geometry('1960x800+0+0')
# Substitua 'zoomed' por atributos específicos para maximizar a janela no Ubuntu
tela.attributes('-zoomed', True)  # Para maximizar a janela no Linux
tela.title("Controle Comercial 1.0 - Menu")
tela['bg'] = "gold"

# Certifique-se de que o caminho da imagem está correto
tkimage = ImageTk.PhotoImage(Image.open(r"./fundo_menu.jpg").resize((tela.winfo_screenwidth(), tela.winfo_screenheight())))

tk.Label(tela, image=tkimage).pack()

def clientes():
    exec(open(r"./clientes.py").read(), locals())
    
def sobre():
    messagebox.showinfo("Sobre", "Sistema Comercial 1.0")

def sair():
    var_sair = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
    if var_sair:
        tela.destroy()
    else:
        messagebox.showinfo("Ótimo", "Que bom que você escolheu continuar")

barramenu = tk.Menu(tela)
menu_func = tk.Menu(barramenu)
menu_ajuda = tk.Menu(barramenu)

barramenu.add_cascade(label="Funcionalidades", menu=menu_func)
menu_func.add_command(label="Clientes", command=clientes)
menu_func.add_command(label="Produtos/Serviços")
menu_func.add_command(label="Vendas")
menu_func.add_command(label="Gestão de Acessos")
menu_func.add_separator()
menu_func.add_command(label="Sair", command=sair)

barramenu.add_cascade(label="Ajuda", menu=menu_ajuda)
menu_ajuda.add_command(label="Sobre", command=sobre)
tela.config(menu=barramenu)

tela.mainloop()
