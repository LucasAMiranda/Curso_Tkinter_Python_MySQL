import mysql.connector

class conexao(object):
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="root", password="", db="controle")


    def gravar(self, sql):
        try:
            cur = self.db.cursor()
            cur.execute(sql)
            cur.close()
            self.db.commit()
        except:
            return False
        return True

    def consultar(self, sql):
        rs=None
        try:
            cur=self.db.cursor()
            cur.execute(sql)
            rs=cur.fetchone()
        except:
            return None
        return rs

    def consultar_tree(self, sql_text):
        rs=None
        try:
            cur=self.db.cursor()
            cur.execute(sql_text)
            rs=cur.fetchall()
        except:
            return None
        return rs

    def fechar(self):
        self.db.close()

