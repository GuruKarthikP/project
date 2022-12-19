import sqlite3
import os

class Image(object):
    def __init__(self):
        self.image_name = []

    def load_directory(self, path):
        """
        :param path: Provide Path of File Directory
        :return: List of image Names
        """
        for x in os.listdir(path):
            self.image_name.append(x)
        return self.image_name

    def database_connect(self, database, tablename, image_data):
        """
        :database name tablename

       """
        try:
            conn = sqlite3.connect(f"{database}.db")
            cursor = conn.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tablename} 
               (image BLOB)""")
            cursor.execute(f"""
             INSERT INTO {tablename}(image) VALUES(?)
             """, (image_data,))
            conn.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            if conn:
                conn.close()
                print("sqlite connection is closed")

def main():
    obj = Image()
    os.chdir("C:/Users/kalya/OneDrive - UNCG/Desktop/output")
    paths_list = obj.load_directory(path='C:/Users/kalya/OneDrive - UNCG/Desktop/output')
    for x in paths_list:
        print(f'Objects in the directory:{x}')
        print(x)
        with open(x, "rb") as f:
            data = f.read()
            obj.database_connect(database='test1', tablename='image_tes', image_data=data)
            print(f"{x} Added to database ")
        


def fetch_data(database, table_name):
    counter = 1
    os.chdir("C:/Users/kalya/OneDrive - UNCG/Desktop/output")
    try:
        conn = sqlite3.connect("test1.db")
        print('connected')
        cursor = conn.cursor()
        data = cursor.execute("""SELECT * FROM image_tes """)
        print('data recieved')
        for x in data.fetchall():
            path = f"C:/Users/kalya/OneDrive - UNCG/Desktop/output1/img_{counter}.jpg"
            print(path)
            with open(path, "wb") as f:
                f.write(x[0])
                counter = counter + 1
                conn.commit()
    except sqlite3.Error as error:

        print("Error while fetching a sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("sqlite connection is closed")


if __name__ == "__main__":
    # Program starts from here
    main()
    print('fetching the records from the table')
    fetch_data(database='test1.db', table_name='image_tes')