import pandas as pd
import sqlite3
import config

class DataBase:
    
    def __init__(self):
        self.conn = sqlite3.connect(config.table)
        self.cursor = self.conn.cursor()

    async def readExcelToDb(self, df):
        '''Получаем значение по ASIN с бд и обновляем запись!'''

        # Проверяем наличие столбца ASIN в DataFrame
        if 'ASIN' in df.columns:
            asin_column = df['ASIN']

            # Проверяем, есть ли пустые значения в столбце ASIN
            if asin_column.isnull().any():
                return  # Прерываем выполнение функции, так как есть пустые значения ASIN

            # Проверяем наличие ASIN в базе данных
            for asin in asin_column.unique():
                result = self.cursor.execute("SELECT * FROM `Table` WHERE `ASIN` = ?", (asin,))
                data = result.fetchall()

                if bool(len(data)):
                    # Удаляем существующую запись с заданным ASIN
                    self.cursor.execute("DELETE FROM `Table` WHERE `ASIN` = ?", (asin,))
                    self.conn.commit()

            # Добавляем новые данные из DataFrame
            df.to_sql("Table", self.conn, if_exists='append', index=False)
            self.conn.commit()
    
    async def userExists(self, user_id):
        '''Проверяем есть ли пользователь в базе'''
        result = self.cursor.execute("SELECT * FROM `Users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))
    
    async def isEmployeeActive(self, user_id):
        '''Проверяем работает ли у нас пользователь!'''
        result = self.cursor.execute("SELECT * FROM `Users` WHERE `user_id` = ? AND (`role` = 'WORKER' OR `role` = 'CREATOR')", (user_id,))
        return bool(len(result.fetchall()))
    
    async def isCreator(self, user_id):
        '''Проверяем является ли пользователь создателем!'''
        result = self.cursor.execute("SELECT * FROM `Users` WHERE `user_id` = ? AND `role` = 'CREATOR'", (user_id,))
        return bool(len(result.fetchall()))
    
    async def foundAsin(self, asin):
        '''Получаем значение по ASIN с бд!'''
        result_data = []

        for el in asin:
            result = self.cursor.execute("SELECT * FROM `Table` WHERE `ASIN` = ?", (el,))
            data = result.fetchall()
        
            if bool(len(data)):
                result_data.extend(data)

        if bool(len(result_data)):
            # Конвертируем данные в DataFrame pandas
            df = pd.DataFrame(result_data, columns=['Researcher', 'Category', 'ASIN', 'SKU', 'Link', 'Price_Amazon', 'Provider', 'Price', 'Shipping_price', 'Stock', 'Days', 'Supplier', 'Tax', 'Margin', 'Roy', 'Formula', 'Handling', 'Merchant', 'Variation', 'Title_1', 'Title_2', 'Bullet_1', 'Bullet_2', 'Bullet_3', 'Bullet_4', 'IMG_1', 'IMG_2', 'IMG_3', 'IMG_4', 'UPC', 'Exception'])
        
            # Записываем данные в файл Excel (XLSX)
            df.to_excel('result.xlsx', index=False, engine='openpyxl')

        return result_data
    
    async def getExcel(self, name):
        '''Получаем excel файл с товарами определенного магазина'''
        result = self.cursor.execute(f"SELECT * FROM `Table` WHERE SKU LIKE '{name}%'")
        data = result.fetchall()
        
        if bool(len(data)):
            # Конвертируем данные в DataFrame pandas
            df = pd.DataFrame(data, columns=['Researcher', 'Category', 'ASIN', 'SKU', 'Link', 'Price_Amazon', 'Provider', 'Price', 'Shipping_price', 'Stock', 'Days', 'Supplier', 'Tax', 'Margin', 'Roy', 'Formula', 'Handling', 'Merchant', 'Variation', 'Title_1', 'Title_2', 'Bullet_1', 'Bullet_2', 'Bullet_3', 'Bullet_4', 'IMG_1', 'IMG_2', 'IMG_3', 'IMG_4', 'UPC'])
        
            # Записываем данные в файл Excel (XLSX)
            df.to_excel('tables.xlsx', index=False, engine='openpyxl')
        
        return data
    
    async def checkStore(self, name):
        '''Проверяем существует ли магазин'''
        result = self.cursor.execute(f"SELECT * FROM `Table` WHERE SKU LIKE '{name}%'")
        data = result.fetchall()

        return data

    async def addUser(self, user_id):
        '''Добавляем пользователя в базу'''
        self.cursor.execute("INSERT INTO `Users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()
    
    async def changeRole(self, user_id, role):
        '''Изменяем роль пользователя'''
        self.cursor.execute('UPDATE `Users` SET `role` = ? WHERE `user_id` = ?', (role, user_id))
        return self.conn.commit()
    
    async def getPrep(self, name):
        '''Получаем преп'''
        result = self.cursor.execute(f"SELECT DISTINCT Supplier FROM `Table` WHERE SKU LIKE '{name}%'")
        data = result.fetchall()

        return data
    
    async def dltEl(self, asin):
        for el in asin:
            self.cursor.execute("DELETE FROM `Table` WHERE `ASIN` = ?", (el,))
        return True


    def close(self):
        self.conn.close()