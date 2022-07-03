import sqlite3

class Product:
    #инициализация
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    # Добавление всех объектов из БД
    def add_item(self, name, descr, picid, price, category):
        try:
            # Вставка записи в таблицу
            self.__cur.execute("INSERT INTO items VALUES(NULL, ?, ?, ?, ?, ?)", (name, descr, picid, price, category))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления предмета в БД " + str(e))
            return False

        return True

    # Удаление из таблицы по id предмета
    def delete_item(self, delId):
        try:
            # Удаление записи из таблицы
            self.__cur.execute(f"DELETE FROM items WHERE query_id='{delId}'")
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка удаления из БД " + str(e))
            return False

        return True

    def get_items_names(self):
        #return bool(self.__cur.execute("SELECT * FROM items WHERE user_id=?", (user_id,)).fetchone())
        #return self.__cur.execute("SELECT item_name FROM items")

        #self.__cur.execute("SELECT item_id, item_name, item_category FROM items")
        self.__cur.execute("SELECT * FROM items")

        res = []
        for i in self.__cur:
            res.append(i)
            #print(i)

        #print(res)
        return res


    def get_categorys(self):
        self.__cur.execute("SELECT item_category FROM items")

        res = set()
        for i in self.__cur:
            res.add(i[0])
            #print(i)

        #print(res)
        return res


    #def searchItems(self):
    #    try:
    #        # Вытаскиваем названия
    #        self.__cur.execute("SELECT item_id FROM items")
    #        self.__db.commit()
    #        for entry in self.__cur: