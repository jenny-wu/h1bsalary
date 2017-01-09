## loop over city names to scrape all salary data
import urllib2
import urllib
from bs4 import BeautifulSoup
import sqlite3
from random import randint
from time import sleep

conn = sqlite3.connect('h1b_salary.db')
c = conn.cursor()
c.execute("DROP TABLE salary")
c.execute('''CREATE TABLE salary
             (company_name text, job_title text, salary integer, city_name text, submit_date text, start_date text, status text, scrape_url text)''')

# retrieve city list
city_list = []
for row in c.execute("SELECT * FROM city;"):
    city_list.append(row[0])

# loop over city list
for city in city_list:
    print city
    rand_gap = randint(1,5)
    print "sleep for "+str(rand_gap)+" seconds."
    sleep(rand_gap)
    param = {'city':city.decode('unicode_escape').encode('utf8')}
    url = "http://h1bdata.info/index.php?em=&job=&"+urllib.urlencode(param,'utf8')+"&year=All+Years"
    print url
    soup = BeautifulSoup(urllib2.urlopen(url).read(),'html.parser')
    table = soup.find('table', attrs={'id': 'myTable'})

    rows = table.findAll('tr')

    ncol = 0
    for tr in rows:
        ncol = ncol + 1
        cols = tr.findAll('td')
        text = ""
        for td in cols:
            # null values
            if td.find(text=True) is None:
                text = text + "NULL" + ';'
            # salary, remove comma
            elif ncol == 3:
                text = text + td.find(text=True).replace(",","") + ';'
            else:
                text = text + td.find(text=True).replace(";","") + ';'
            # insert complete row into db
            if text.count(";") == 7:
                text = text + url + ';'
                row_to_insert = "'" + text.replace("'","''").replace(";","','")[:-2]
                #print row_to_insert
                c.execute("INSERT INTO salary VALUES (" + row_to_insert + ")")
    conn.commit()

conn.close()
