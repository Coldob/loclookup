from cmd import Cmd
import sqlite3
from sqlite3 import Error
import os
import random
from decimal import Decimal
con = sqlite3.connect('loc.db')
con.row_factory = lambda cursor, row: row[0]
cur = con.cursor()
sqlite3.connect('loc.db')
try:
    con.execute("create virtual table location using fts3(n, name, x1 ,y1 ,x2 ,y2)")
except Error as e:
    print()
class loclookup(Cmd):
    prompt = 'loclookup> '
    intro = "Welcome, to location lookup! Ƹ̵̡Ӝ̵̨̄,Ʒ\nhelp for commands"
    def help_gen(self):
        print("generate a new random location based on location info")
    def help_newtable(self):
        print("resets all saved locations for location data")
    def help_newloc(self):
        print("This is how you save a new square area")
    def do_newtable(self, arg):
        try:
            con.execute("DROP TABLE location;")
            con.execute("create virtual table location using fts3(n, name, x1 ,y1 ,x2 ,y2)")
            con.executescript("""
                insert into location (n, name, x1, y1, x2, y2) values (0, 'test', 1, 2, 3, 4)
                """)
        except Error as e:
            print(e)
        finally:
            print("Your location data has been reset!")
    def do_newloc(self,inp):
        print("Enter name for coordinate")
        title = input("Enter name here:")
        cur.execute('SELECT n FROM location')
        num = cur.fetchall()
        nuo = int(max(num))
        nu = nuo+1
        print("Enter corner of location (ex 123, 123)\nIt is usually easiest to copy and paste coordinate directly from google maps")
        x1, y1 = input("paste coordinates for first corner here: ").split(", ")
        x2, y2 = input("paste coordinates for second corner here: ").split(", ")
        print("Location has been saved")
        con.executescript(f'insert into location (n, name, x1, x2, y1, y2) values ({nu}, "{title}", {x1}, {x2}, {y1}, {y2})')
    def do_gen(self, inp):
        cur.execute('SELECT n FROM location')
        num = cur.fetchall()
        end = int(max(num))
        sel = random.randint(1,end)
        cur.execute(f'SELECT x1 FROM location WHERE n={sel};')
        h1 = str(cur.fetchall()).replace('[',"").replace(']',"")
        cur.execute(f'SELECT x2 FROM location WHERE n={sel};')
        h2 = str(cur.fetchall()).replace('[',"").replace(']',"")
        cur.execute(f'SELECT y1 FROM location WHERE n={sel};')
        j1 = str(cur.fetchall()).replace('[',"").replace(']',"")
        cur.execute(f'SELECT y2 FROM location WHERE n={sel};')
        j2 = str(cur.fetchall()).replace('[',"").replace(']',"")
        x1 = float(h1)
        x2 = float(h2)
        y1 = float(j1)
        y2 = float(j2)
        if x1>x2 :
            xr = random.uniform(x2, x1)
        else:
            xr = random.uniform(x1, x2)
        if y1>y2 :
            yr = random.uniform(y2, y1)
        else:
            yr = random.uniform(y1, y2)
        print(f'{xr}, {yr}')
    def do_exit(self, inp):
        print("No place like home.")
        return True

    def help_exit(self, line):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == '__main__':
    loclookup().cmdloop()
