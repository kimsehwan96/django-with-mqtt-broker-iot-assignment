import MySQLdb
import traceback
from datetime import datetime

class DataDAO:
    def __init__(self):
        #기초 정보를 셋업함
        self.host = "3.34.87.77"
        self.username = "root"
        self.password = "j112189"
        self.database = "iot_db"
        self.temp = None
        self.timestamp = None
        self.humid = None
    
    
    def get_conn(self):
        db = MySQLdb.connect(user=self.username,
        host=self.host, passwd=self.password, db=self.database)

        return db

    def get_cursor(self, connection):
        return connection.cursor()

    def insert_data(self, temp, humid):
        self.temp = temp
        self.humid = humid
        con = self.get_conn()
        cursor = self.get_cursor(con)

        query = """
        INSERT INTO mqttApp_data(timestamp, temp, humid) VALUES(%s, %s, %s)
        """
        print(datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
        print(str(self.temp), str(self.humid))
        try:
            cursor.execute(query, (datetime.now().strftime("%Y-%m-%d %H:%I:%S"), self.temp, self.humid))
            con.commit()
        except Exception as e:
            print(traceback.format_exc())
            cursor.close()
        finally:
            cursor.close() #cursor를 커밋 이후 close한다.
            self.temp = None
            self.humid = None 
            self.timestamp = None


if __name__=="__main__":
    d = DataDAO()
    d.insert_data(10.5, 67.9)