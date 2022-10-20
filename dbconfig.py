import pymysql
# dbconfig.py
class MysqlController:
    def __init__(self, host, id, pw, db_name):
        self.conn = pymysql.connect(host=host, user= id, password=pw, db=db_name,charset='utf8')
        self.curs = self.conn.cursor()

    def insert_value(self,table_name, values):
        sql = 'INSERT INTO {0} VALUES ({1})'.format(table_name, ','.join(values))
        self.curs.execute(sql)
        self.conn.commit()


    def insert_value_with(self,table_name, col, values):
        sql = 'INSERT INTO {0}} ({1}) VALUES ({2})'.format(table_name, ','.join(col), ','.join(values))
        self.curs.execute(sql)
        self.conn.commit()