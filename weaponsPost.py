import psycopg2
import os
import pandas

class weaponsData(object):
    def parseFile(self):
        self.readFile('weapons.csv')

    def readFile(self, filename):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        df = pandas.read_csv(filename, sep="|")
        df.to_sql("weapon", conn, if_exists='append', index=False)

c = weaponsData().parseFile()