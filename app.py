import sqlite3
import flask
import datetime

print(datetime.datetime.now())

app = flask.Flask(__name__)

def connect():
    conn = sqlite3.connect('t_list.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS holidays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,        -- holiday name
        start_date TEXT,  -- holiday start
        end_date TEXT,    -- holiday end
        duration INTEGER  -- length in days
    );
    """)
    c.close()
    conn.close()
    
connect()

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/add')
def add_holiday():
    name = flask.request.form['name']
    start_str = flask.request.form['start']
    end_str = flask.request.form['end']

    # Convert string → datetime
    start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()

    # Calculate duration in days
    duration = (end_date - start_date).days + 1  # +1 to count the last day

    # Insert into DB
    conn = sqlite3.connect('t_list.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO holidays (name, start_date, end_date, duration)
        VALUES (?, ?, ?, ?)
    """, (name, start_str, end_str, duration))
    conn.commit()
    conn.close()

    return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
    app.run(port=8367, debug=True)