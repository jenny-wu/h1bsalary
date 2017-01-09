import urllib2
from bs4 import BeautifulSoup
import sqlite3

# import environment
import pandas

top_companies = pandas.read_table("../data/top_companies.txt", sep='    ')
print top_companies.shape

top_companies.head()
del top_companies['Latest Filings']

conn = sqlite3.connect('h1b_salary.db')
c = conn.cursor()
c.execute("DROP TABLE salary_top50_companies")
c.execute('''CREATE TABLE salary_top50_companies
             (company_name text, job_title text, salary integer, city_name text, submit_date text, start_date text, status text, scrape_url text)''')

# loop over top 50 companies list
top50_companies = top_companies[0:50]
for index, row in top50_companies.iterrows():
    employer = row["Company Name"].replace(" ","+").replace("&","%26").replace("(","%28").replace(")","%29")
    print employer
    for year in range(2010,2017):
        print year
        url = "http://h1bdata.info/index.php?em="+employer+"&job=&city=&year="+str(year)
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
                    c.execute("INSERT INTO salary_top50_companies VALUES (" + row_to_insert + ")")
    conn.commit()

conn.close()
