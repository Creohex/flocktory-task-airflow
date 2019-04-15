from common import *
import os
import psycopg2

### tests: ###
# common:
#  |- helper funcs
#   \ sql queries (select/insert)
# ...

# conn = psycopg2.connect(user = "docker",
#                         password = "P@ssw0rd",
#                         host = "127.0.0.1",
#                         port = "5432",
#                         database = "main")

# print(conn)

# cur = conn.cursor()
# cur.execute("select * from level")
# print(cur)
# cur.fetchone()
# for x in cur:
#     print(x)

# cur.execute("DELETE FROM level WHERE level='TRACE'")
# conn.commit()
# cur.fetchone()
# conn.close()


# os.environ['PGUSER'] = 'docker'
# os.environ['PGPORT'] = "5432"
# os.environ['PGPASSWORD'] = 'P@ssw0rd'
# os.environ['PGDATABASE'] = 'main'
# os.environ['E'] = "20"
# os.environ['PGHOST'] = 'db'

# from datetime import datetime
# from dateutil import parser
# x = parser.parse('2019-04-14T04:00:00+00:00')
# print(x)