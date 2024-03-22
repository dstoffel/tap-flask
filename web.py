from flask import Flask
from markupsafe import escape
app = Flask(__name__)
import pymysql as MySQLdb

@app.route('/')
def hello_world():
    return 'Hello, World2!'

@app.route('/sql'):
def sql():
    server = open('/bindings/mysql/host').read()
    user = open('/bindings/mysql/username').read()
    passwd = open('/bindings/mysql/password').read()
    dbname =  open('/bindings/mysql/database').read()
    print(f'using {server} / {user} / {passwd} / {dbname}')
    try:
        db = MySQLdb.connect(server, user, passwd, dbname)
        cursor = db.cursor()        
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
    # Check if anything at all is 
        return 'OK'              
    except MySQLdb.Error:
        return "ERROR IN CONNECTION"


@app.route('/hello/<username>')
def hello_user(username):
    # say hello to that user
    return 'Hello %s' % escape(username)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
