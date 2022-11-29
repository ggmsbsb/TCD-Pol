from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import pymysql

# Conexão com o BD
mypass = "root"
mydatabase="db"

con = pymysql.connect(host="localhost",user="root",password=mypass,database=mydatabase)
cur = con.cursor()

# Table utilizada 
issueTable = "books_issued" 
bookTable = "books" 
    
#Lista com todos os IDs de livros
allBid = [] 

#Lista de livros alugados
def issue():
    
    global issueBtn,labelFrame,lb1,inf1,inf2,quitBtn,root,Canvas1,status
    
    bid = inf1.get()
    issueto = inf2.get()

    issueBtn.destroy()
    labelFrame.destroy()
    lb1.destroy()
    inf1.destroy()
    inf2.destroy()
    
    #Coleta todos os livros cujos IDs constam como emprestados
    extractBid = "select bid from "+bookTable
    try:
        cur.execute(extractBid)
        con.commit()
        for i in cur:
            allBid.append(i[0])
        
        if bid in allBid:
            checkAvail = "select status from "+bookTable+" where bid = '"+bid+"'"
            cur.execute(checkAvail)
            con.commit()
            for i in cur:
                check = i[0]
                
            if check == 'avail':
                status = True
            else:
                status = False
        #Livro não disponivel
        else:
            messagebox.showinfo("Erro","Livro não disponível")
    except:
        messagebox.showinfo("Erro","ID não encontrado")
    
    #Registrar um empréstimo de um livro
    issueSql = "insert into "+issueTable+" values ('"+bid+"','"+issueto+"')"
    show = "select * from "+issueTable
    
    #Atualizando o status de um livro, definindo-o como emprestado
    updateStatus = "update "+bookTable+" set status = 'issued' where bid = '"+bid+"'"
    try:
        if bid in allBid and status == True:
            cur.execute(issueSql)
            con.commit()
            cur.execute(updateStatus)
            con.commit()
            messagebox.showinfo('Successs',"Livro emprestado!")
            root.destroy()
        else:
            allBid.clear()
            messagebox.showinfo('Menssagem',"Livro já emprestado.")
            root.destroy()
            return
    except:
        messagebox.showinfo("Erro.","O valor inserido não existe, tente novamente.")
    
    print(bid)
    print(issueto)
    
    allBid.clear()
    
def issueBook(): 
    
    global issueBtn,labelFrame,lb1,inf1,inf2,quitBtn,root,Canvas1,status
    
    root = Tk()
    root.title("Library")
    root.minsize(width=400,height=400)
    root.geometry("600x500")
    
    Canvas1 = Canvas(root)
    Canvas1.config(bg="#D6ED17")
    Canvas1.pack(expand=True,fill=BOTH)

    headingFrame1 = Frame(root,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        
    headingLabel = Label(headingFrame1, text="Empréstimo", bg='black', fg='white', font=('Courier',15))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)  
        
    # ID
    lb1 = Label(labelFrame,text="ID : ", bg='black', fg='white')
    lb1.place(relx=0.05,rely=0.2)
        
    inf1 = Entry(labelFrame)
    inf1.place(relx=0.3,rely=0.2, relwidth=0.62)
    
    # Emprestar ao aluno X
    lb2 = Label(labelFrame,text="Emprestar á: ", bg='black', fg='white')
    lb2.place(relx=0.05,rely=0.4)
        
    inf2 = Entry(labelFrame)
    inf2.place(relx=0.3,rely=0.4, relwidth=0.62)
    
    
    #Botão de emprestimo
    issueBtn = Button(root,text="Emprestar",bg='#d1ccc0', fg='black',command=issue)
    issueBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(root,text="Sair",bg='#aaa69d', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    root.mainloop()