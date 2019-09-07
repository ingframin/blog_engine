import sqlite3

DB_STRING = './database/blog.db'

def setup():
    conn = sqlite3.connect(DB_STRING)
    with open('./database/schema.sql') as sch:
        ct = sch.read().split(';')
        for stmt in ct:
            conn.execute(stmt)
    
    conn.execute("INSERT INTO admins VALUES ('username', 'password','email@whatever.it')")
    conn.commit()
    conn.close()

def insert(table, values):
    conn = sqlite3.connect(DB_STRING)
    for v in values:
        conn.execute("INSERT INTO "+table+" VALUES ("+ v +")")
    conn.commit()
    conn.close()

def query(table,id = -1):
    conn = sqlite3.connect(DB_STRING)
    c = conn.cursor()
    if int(id) >= 0:
        c.execute("SELECT * FROM "+table+" WHERE PID="+str(id))
    else:
        c.execute('SELECT * FROM '+table)
    res = c.fetchall()
    conn.close()
    return res

def contacts(username):
    conn = sqlite3.connect(DB_STRING)
    c = conn.cursor()
    c.execute("SELECT content FROM contacts WHERE username="+username)
    res = c.fetchall()
    return res[0][0]

def query_by_year(table,year):
    conn = sqlite3.connect(DB_STRING)
    c = conn.cursor()
    c.execute("SELECT * FROM "+table)
    res = c.fetchall()
    conn.close()
    return (post for post in res if year in post[3])

if __name__=='__main__':

    setup()
    #p0 = '0,"My first post","This is the content of my first post","30-10-2018"'
    #p1 = '1,"My second post","This is the content of my second post","30-10-2018"'
    #cnt = '"username","E-mail: <a href=""mailto:something@else.it"">something@else.it</a><br><a href=""https://www.linkedin.com"">LnkedIn</a> "'
    #insert('blog_post',[p0,p1])
    #insert('contacts',[cnt])