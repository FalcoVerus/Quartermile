from flask import Flask, request, render_template
import mysql.connector as mysql

#Connecting to the DB
qmdb = mysql.connect(
  host="localhost",
  user="falco",
  password="Falco@1",
  database="qm"
)
qmcursor = qmdb.cursor()

app = Flask(__name__)

# Defining the home page of our site
@app.route('/', methods=['GET', 'POST'])  # this sets the route to this page
def index():
    if request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')
        qmcursor.execute('SELECT * FROM car_data WHERE brand=%s AND model=%s ORDER BY et', (brand, model))
        result = qmcursor.fetchall()
        return render_template('result.html', data=result)
    return render_template('index.html')

# Main driver
if __name__ == '__main__':
    app.run()
