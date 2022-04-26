from cmd import Cmd
import sqlite3
from sqlite3 import Error
import os
import random
from decimal import Decimal
con = sqlite3.connect('loc.db')
con.enable_load_extension(True)
con.enable_load_extension(False)
con.row_factory = lambda cursor, row: row[0]
cur = con.cursor()
sqlite3.connect('loc.db')
class loclookup(Cmd):
    prompt = 'loclookup> '
    intro = "Welcome, to location lookup! Ƹ̵̡Ӝ̵̨̄,Ʒ\n if the database is having issues delete it and Enter ts then newtable\nEnter help for commands"
    def help_sgen(self):
        print("this is for generating a random point in a single location format: sgen {name}")

    def help_gen(self):
        print("generate a new random location based on location info")

    def help_newtable(self):
        print("resets all saved locations for location data")

    def help_list(self):
        print("lists current saved locations in database")

    def help_newloc(self):
        print("records a square area into the database which is used to generate a random coordinate in")

    def help_view(self):
        print("usage view {name} lists coordinates associated with a database entry")

    def help_compass(self):
        print("gives a random compass value")

    def help_del(self):
        print("deletes a table value")

    def do_compass(self, arg):
        comp = random.randint(0,364)
        print("Compass Direction:", comp)

#this is the code for resetting the entire sql table can be optimized
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
#this is how you set a new location to be saved to database
    def do_newloc(self,inp):
        try:
            print("Enter name for coordinate")
            title = input("Enter name here:")
            cur.execute('SELECT n FROM location')
            num = cur.fetchall()
            print(num)
            nuo = int(max(num))
            nu = nuo+1
            print(nu)
            print("Enter corner of location (ex 123, 123)\nIt is usually easiest to copy and paste coordinate directly from google maps")
            x1, y1 = input("paste coordinates for first corner here: ").split(", ")
            x2, y2 = input("paste coordinates for second corner here: ").split(", ")
            print("Location Saved!")
            con.executescript(f'insert into location (n, name, x1, x2, y1, y2) values ({nu}, "{title}", {x1}, {x2}, {y1}, {y2})')
        except:
            print("coordinates must be numerals in the format #, #")
            return
#this gens a random coordinate from the locations saved
    def do_gen(self, inp):
        cur.execute('SELECT n FROM location')
        num = cur.fetchall()
        end = int(max(num))
        sel = random.randint(1,end)
        print("Here are your coordinates! :)")
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
# this gens a random coordinate within the location you have selected
    def do_sgen(self, inp):
            cur.execute(f"SELECT n FROM location WHERE name MATCH '%{inp}%';")
            number = str(cur.fetchall()).replace('[',"").replace(']',"")
            if number.isnumeric():
                print("Here are your coordinates! :)")
                cur.execute(f"SELECT x1 FROM location WHERE name MATCH '%{inp}%';")
                h1 = str(cur.fetchall()).replace('[',"").replace(']',"")
                cur.execute(f"SELECT x2 FROM location WHERE name MATCH '%{inp}%';")
                h2 = str(cur.fetchall()).replace('[',"").replace(']',"")
                cur.execute(f"SELECT y1 FROM location WHERE name MATCH '%{inp}%';")
                j1 = str(cur.fetchall()).replace('[',"").replace(']',"")
                cur.execute(f"SELECT y2 FROM location WHERE name MATCH '%{inp}%';")
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
                return
            print("This location does not exist\nOr no location was stated please use format sgen {name}")
#this lists the locations that have been saved by name
    def do_list(self, inp):
        cur.execute('SELECT name FROM location')
        print(cur.fetchall())
#this shows you the coordinates saved for one location
    def do_view(self, sel):
        cur.execute(f"SELECT n FROM location WHERE name MATCH '%{sel}%';")
        number = str(cur.fetchall()).replace('[',"").replace(']',"")
        if number.isnumeric():
            cur.execute(f"SELECT x1 FROM location WHERE name MATCH '%{sel}%';")
            h1 = str(cur.fetchall()).replace('[',"").replace(']',"")
            cur.execute(f"SELECT x2 FROM location WHERE name MATCH '%{sel}%';")
            h2 = str(cur.fetchall()).replace('[',"").replace(']',"")
            cur.execute(f"SELECT y1 FROM location WHERE name MATCH '%{sel}%';")
            j1 = str(cur.fetchall()).replace('[',"").replace(']',"")
            cur.execute(f"SELECT y2 FROM location WHERE name MATCH '%{sel}%';")
            j2 = str(cur.fetchall()).replace('[',"").replace(']',"")
            print(f'{sel}:[x1:{h1},y1:{j1},x2:{h2},y2:{j2}]')
            return
        print("this coordinate does not exist\nOr no location was stated please use format view {name}")
#this is how you delete a single location that has been saved in the database
    def do_del(self, inp):
        cur.execute(f"SELECT n FROM location WHERE name MATCH '%{inp}%';")
        number = str(cur.fetchall()).replace('[',"").replace(']',"")
        if number.isnumeric():
            cur.execute(f"DELETE FROM location WHERE name MATCH '%{inp}%';")
            print("Coordinates deleted!")
            return
        print("This is not a saved datapoint\n Or no datapoint was entered")
#exit command
    def do_exit(self, inp):
        print("No place like home.")
        return True

    def help_exit(self, line):
        print('exit the application. Shorthand: x q or Ctrl-d.')
#ts for trouble shoot this is how you start the program after table is made it sets the table newloc should be entered after this command
#there is a better way to do this but sadly I have to focus on other coursework
    def do_ts(self, inp):
        try:
            con.execute("create virtual table location using fts3(n, name, x1, y1, x2, y2)")
        except:
            print("Table already exists")
            return
    def help_ts(self):
        print("creates a new virtual table this command was made for first time setup")

    def default(self, inp):
        if inp == 'x' or inp == 'z':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == '__main__':
    loclookup().cmdloop()
