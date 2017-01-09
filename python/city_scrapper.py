import urllib2
from bs4 import BeautifulSoup
import sqlite3

def next_chr(char):
    if ord(char) in range(ord('a'),ord('z')):
        return chr(ord(char)+1)
    elif char == 'z':
        return ' '
    elif char == ' ':
        return "'"
    elif char == "'":
        return "error"

def pop_cities(search_str,str_len):
    print search_str
    url = "http://h1bdata.info/cities.php?term=" + search_str.replace(' ','%20').replace("'",'%27')
    city_list = urllib2.urlopen(url).read()
    command = "city = " + city_list.strip()
    exec(command)
    if (len(city)==50):
        print "go lower level and search"
        return pop_cities(search_str + 'a',str_len)
    else:
        if (len(city)>0):
            insert_query = "insert into city (city_name) values" + city_list.strip().replace('","','"),("').replace('[','(').replace(']',')')+";"
            c.execute(insert_query)
            conn.commit()
            print "inserted cities"
        if search_str[-1:] == "'" and len(search_str) <= str_len + 1:
            print "end of search"
            return
        elif search_str[-1:] == "'":
            return pop_cities(search_str[:-2]+next_chr(search_str[-2:][0]),str_len)
        else:
            print "go upper level and search"
            return pop_cities(search_str[:-1]+next_chr(search_str[-1:]),str_len)
