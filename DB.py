import sqlite3
import datetime as dt

#%%
class Video_DB:
    
    def __init__(self, name): 
        self.name = name
 
        
    def connect(self):
        self.conn = sqlite3.connect(str(self.name) + ".db")
        self.cursor = self.conn.cursor()  
        
        
    def close(self):
        self.conn.commit()
        self.conn.close()
            
        
    def create_table(self, name):  
        
        self.table_name = name
        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} 
                        (video_id text PRIMARY KEY, channel_name text, video_name text, language text,
                        comment_count text, like_count text, dislike_count text, relation text, views_count text, 
                        tags_count text, video_duration text, video_discription text, analysis text, date text)""")
        self.close()
     
    def create_table_for_comments(self):
        
        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS Comments 
                        (_id text, comment text,
                        FOREIGN KEY (_id) REFERENCES {self.table_name}(video_id) ON DELETE CASCADE)""")
        self.close()
        
    
    def insert_into_comments_table(self, _id, comment):
        
        self.connect()
        self.cursor.execute(f"""INSERT INTO Comments VALUES ('{_id}', '{comment}')""")
        self.close()
        
    
    def print_comments(self, id_video):
        
        self.connect()
        try:
            self.cursor.execute(f"SELECT * from Comments where _id = '{id_video}'")
            comments = self.cursor.fetchall()
        except:
            comments = False
            
        return comments
        self.close()
        
        
    def check_actuality_by_id(self, id_video):
        
        self.connect()
        self.cursor.execute(f"""SELECT * FROM {self.table_name} WHERE video_id = '{id_video}'""")
        
        data_mass = self.cursor.fetchall()
        
        if data_mass == []:
            return False       
        else:
            video_data = data_mass[0][-1].split('-')
            rq_date = dt.date(int(video_data[0]),int(video_data[1]),int(video_data[2]))
            rq_delta = dt.date.today() - rq_date
            
            if rq_delta.days > 14:
                self.delete(data_mass[0][0])
                return False
            else:
                return True
        self.close()
        
    
    def insert(self, art):        
        
        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(f"""INSERT INTO {self.table_name} VALUES ('{art.video_id}',
                            '{art.channel_name}', '{art.video_name}','{art.language}', '{art.comment_count}', 
                            '{art.like_count}', '{art.dislike_count}', '{art.relation}', '{art.views_count}',
                            '{art.tags_count}', '{art.video_duration}', '{art.video_discription}', 
                            '{art.analysis}','{date_of_entry}')""")
        self.close()


    def extract_obj_by_id(self, id_video):
        
        self.connect()
        self.cursor.execute(f"""SELECT * FROM {self.table_name} WHERE video_id = '{id_video}'""")
        obj = self.cursor.fetchall()
        return obj
        self.close()
    
    
    def delete(self, delete_data):       
        
        self.connect()
        self.cursor.execute(f"""DELETE FROM {self.table_name} WHERE youtube_link = '{delete_data}'""")
        self.close()
        
     
    def create_favourites_table(self):
        
        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS Favourites
                        (person_id text PRIMARY KEY, youtube_link text)""")
        self.close()
    
    
    def number_of_links(self, user_id):
        
        self.connect()
        self.cursor.execute(f"""SELECT COUNT(*) FROM Favourites WHERE person_id = '{user_id}'""")
        number = self.cursor.fetchall()
        return number
        self.close()
        
        
    def insert_into_favourites_table(self, person_id, youtube_link):
        
        self.connect()
        quantity_of_links = self.number_of_links(person_id)
        
        if quantity_of_links == 10:
            print('''You exceeded the limit for storing links in Favorites
                  Please delete one of the entries and repeat the operation''')
        else:            
            self.cursor.execute(f"""INSERT INTO Favourites VALUES ('{person_id}','{youtube_link}')""")
        self.close()
     
        
        
    def delete_from_favourites_table(self, user_id, link):
        
        self.connect()
        self.cursor.execute(f"""DELETE FROM Favourites WHERE youtube_link = '{link}' and person_id = '{user_id}'""")
        self.close()
        
        
    def print_favorites_table(self, user_id):
        
        self.connect()
        count = 1
        text = ''
        self.cursor.execute(f"""SELECT * FROM Favourites WHERE person_id = '{user_id}'""")
        massive = self.cursor.fetchall()
        
        for item in massive:
            text += f'{count}. {item[0]}-{item[1]}' + '\n'           
            count += 1
            
        return text
        self.close()
    

    def create_user_table(self):
        
        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS User 
                        (user_name text PRIMARY KEY, status text, date text)""")
        self.close() 
        
     
    def insert_into_user_table(self, user_name, user_status):
        
        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(f"""INSERT INTO User VALUES ('{user_name}', '{user_status}', '{date_of_entry}')""")
        self.close()
        
    
    def print_user_table(self):
        
        self.connect()
        self.cursor.execute(f"SELECT * from User")
        result = self.cursor.fetchall()            
        return result
        self.close()
        
        
    def update_state_in_user_table(self, user_name, number_state):
        
        self.connect()
        self.cursor.execute(f"UPDATE User set status = '{number_state}' where user_name = '{user_name}'")
        self.close()


    def get_user_state(self, user_name):

        self.connect()
        self.cursor.execute(f"select * from User where user_name = '{user_name}'")
        result = self.cursor.fetchall()
        return result
        self.close()


    def create_statistic_table(self):

        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS Statistic 
                        (u_name text, action text, date text,
                        FOREIGN KEY (u_name) REFERENCES User (user_name) ON DELETE CASCADE)""")
        self.close()


    def insert_into_statistic_table(self, name, action):

        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(f"""INSERT INTO User VALUES ('{name}', '{action}', '{date_of_entry}')""")
        self.close()


    def print_statistic_table(self):

        self.connect()
        self.cursor.execute(f"SELECT * from Statistic")
        result = self.cursor.fetchall()
        return result
        self.close()

    def check_new_users(self, date):

        self.connect()
        self.cursor.execute(f"Select * from User where date = '{date}'")
        result = self.cursor.fetchall()
        return result
        self.close


    def check_week_new_users(self):

        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(f"select count(*) from User where date <= (select date('now')) and date >= (select date('now', '-7 days'))")
        result = self.cursor.fetchall()
        return result
        self.close()

#%%
class Interaction:
    
    def __init__(self, database):        
        self.database = database
    
    
    def create_table(self, name):       
        self.database.create_table(name)
        
        
    def input_data(self, data):
        self.database.insert(data)
        
    
    def extract_obj_by_id(self, _id):
        obj = self.database.extract_obj_by_id(_id)
        return obj
    
    
    def check_actuality_by_id(self, _id):
        res = self.database.check_actuality_by_id(_id)
        return res
    
    
    def create_table_for_comments(self):
        self.database.create_table_for_comments()
        
        
    def insert_into_comments_table(self, video_id, comment):
        self.database.insert_into_comments_table(video_id, comment)
    
    
    def print_comments(self, _id):
        text = self.database.print_comments(_id)
        return text
    
    
    def create_favourites_table(self):
        self.database.create_favourites_table()
        
        
    def insert_into_favourites_table(self, person_id, youtube_link):
        self.database.insert_into_favourites_table(person_id, youtube_link)
        
        
    def delete_from_favourites_table(self, user_id, link):
        self.database.delete_from_favourites_table(user_id, link)


    def print_favorites_table(self, user_id):
        string = self.database.print_favorites_table(user_id)
        return string
    
    
    def create_user_table(self):
        self.database.create_user_table()
        
        
    def insert_into_user_table(self, user_name, user_status):  
        self.database.insert_into_user_table(user_name, user_status)

    def print_user_table(self):
        result = self.database.print_user_table()
        return result

    def check_new_users(self, date):
       result = self.database.check_new_users(date)
       return result
        
        
    def update_state_in_user_table(self, user_name, number_state):
        self.database.update_state_in_user_table(user_name, number_state)

    def get_user_state(self, user_name):
        result = self.database.get_user_state(user_name)
        return result


    def create_statistic_table(self):
        self.database.create_statistic_table()


    def insert_into_statistic_table(self, name, action):
        self.database.insert_into_statistic_table(name, action)


    def print_statistic_table(self):
        result = self.database.print_statistic_table()
        print(result)


    def check_week_new_users(self):
        result = self.database.check_week_new_users()
        return result
        
