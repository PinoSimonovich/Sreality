
import psycopg2

class SrealityPipeline:
    
    def __init__(self):
        
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'weaksauce'
        database = 'sreality'
        
        ## Create/Connect to PSQL
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Check if database exists
        self.cur.execute("select exists(select * from pg_catalog.pg_database where datname=%s)", (database,))
        if not self.cur.fetchone()[0]:
            self.cur.execute("rollback")
            self.cur.execute(f'CREATE DATABASE {database}')
        
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.connection.set_client_encoding('UTF8')
        # self.connection.autocommit = True
        self.cur = self.connection.cursor()
        
        ## Create schema and table if none exists
        self.cur.execute("CREATE SCHEMA IF NOT EXISTS scrape")
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS scrape.flats(
                id serial PRIMARY KEY,
                title text,
                links text
            )
        """)
        
        ## Clean table
        self.cur.execute("TRUNCATE TABLE scrape.flats")
    
    def process_item(self, item, spider):
        
        ## Define insert statement
        self.cur.execute(
            "insert into scrape.flats (title, links) values (%s,%s)",
            (item["title"],str(item["links"]))
        )
        
        ## Execute insert of data into database
        self.connection.commit()
        
        # return item
    
    def close_spider(self, spider):
        
        ## Construct html page and save it before exiting
        self.cur.execute("SELECT * FROM scrape.flats")
        data = self.cur.fetchall()
        
        head = "<html><meta charset=\"UTF-8\"><body>"
        divs = " ".join([
            "<div>" +\
            "<h3>" +\
            d[1].replace("\u016f","").encode("utf-8", errors='ignore').decode('utf-8') +\
            "</h3>" +\
            " ".join([
                "<img src='" + e + "' style='width:128px;height:128px;'>"
                for e in eval(d[2])[:6] # limit to 6 images, just in case
            ]) +\
            "</div>"
            for d in data
        ])
        tail = "</body></html>"
        
        html = open("index.html", 'w')
        html.write(head + divs + tail)
        html.close()
        
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
