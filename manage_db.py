'''
Blog Engine
Copyright (C) 2019  Franco Minucci

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import sqlite3

DB_STRING = './database/blog.db'

def setup():
    conn = sqlite3.connect(DB_STRING)
    with open('./database/schema.sql') as sch:
        ct = sch.read().split(';')
        for stmt in ct:
            conn.execute(stmt)
    
    conn.execute("INSERT INTO admins VALUES ('username', 'password','email@whatever.xxx')")
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

def query_by_year(table,year):
    conn = sqlite3.connect(DB_STRING)
    c = conn.cursor()
    c.execute("SELECT * FROM "+table)
    res = c.fetchall()
    conn.close()
    return (post for post in res if year in post[3])

if __name__=='__main__':

    setup()
    # p0 = '0,"My first post","This is the content of my first post","30-10-2018"'
    # p1 = '1,"My second post","This is the content of my second post","30-10-2018"'
    # insert('blog_post',[p0,p1])
    #print(query('admins'))
    # print(query('blog_post'))