import sqlite3
from Product import Product
import io

class dbase:
    def __init__(self, dbase):
        self.__db = dbase
        self.__cur = dbase.cursor()
        #self.__cur = db.cursor()

    # Соединение с БД
    #def connect_db(self):
    #    conn = sqlite3.connect('main.db')
    #    conn.row_factory = sqlite3.Row

    #    return conn

    # Создание БД
    def create_db(self, dbase):
        #global dbase

        conn = sqlite3.connect('main.db')
        conn.row_factory = sqlite3.Row

        #db = connect_db(self, dbase)
        #with open('sq_db.sql', mode="r") as file:
        with io.open('sq_db.sql', encoding='utf-8') as file:
           self.__db.cursor().executescript(file.read())
        self.__db.commit()

        dbase = Product(db)

# Ввод данных в БД
def input_data():
    # Формат ввода: Название книги, Описание, Цена
    with io.open('input.txt', encoding='utf-8') as file:
        for line in file:
            splitLine = line.split(';')
            dbase.add_item(splitLine[0], splitLine[1], splitLine[2], int(splitLine[3]))

