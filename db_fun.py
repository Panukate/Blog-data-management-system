import mysql.connector
obj=mysql.connector.connect(host='localhost',
                            username='root',
                            password='Pranita@321',
                            database='blog_data')
if obj:
    print('successfully connected')
else:
    print('plz try again')

cur=obj.cursor()
def create_table():
    cur.execute('create table if not exists blogtable(title Text,author text, article text,postdate DATE,image BLOB)')
def add_post(blog_title,blog_auther,blog_article,blog_date,img_file):
    cur.execute("insert into blogtable(title,author,article,postdate,image) values(%s,%s,%s,%s,%s)",(blog_title, blog_auther,blog_article,blog_date,img_file))
    obj.commit()
def view_all_records():
    cur.execute("select * from blogtable")
    data=cur.fetchall()
    return data
def view_all_titles():
    cur.execute("Select distinct title from blogtable ")
    data=cur.fetchall()
    return data
def get_blog_title(title):
    cur.execute("select * from blogtable where title='{}'".format(title))
    data=cur.fetchall()
    return data
def get_blog_author(author):
    cur.execute("select * from blogtable where title='{}'".format(author))
    data = cur.fetchall()
    return data
def delete_blog(author):
    cur.execute("Delete from blogtable where author='{}'".format(author))
    obj.commit()