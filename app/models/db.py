import psycopg2
import config
from models.pool import db_pool

def init_db(pwd_hash):
    if not db_pool.create_pool():
        raise Exception("Не удалось создать пул соединений")

    conn = db_pool.getconn()

    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL
    );
    ''')

    cur.execute('''
    INSERT INTO users (username, password, role)
    VALUES (%s, %s, 'admin')
    ON CONFLICT DO NOTHING;
    ''', ('admin', pwd_hash))

    cur.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id serial PRIMARY KEY,
        author VARCHAR(255) NOT NULL,
        text TEXT NOT NULL,
        likes INT
    );
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id serial PRIMARY KEY,
        author VARCHAR(255) NOT NULL,
        text TEXT NOT NULL
    );
    ''')

    conn.commit()

    cur.close()
    db_pool.putconn(conn)

    print('найс')

def get_hashed_pass(username):
    
    conn = db_pool.getconn()

    cur = conn.cursor()

    cur.execute('SELECT password FROM users WHERE username = %s', (username,))
    data = cur.fetchone()
    
    cur.close()
    db_pool.putconn(conn)

    if data:
        return data[0]

    return None

def set_hashed_pass(username, password):

    conn = db_pool.getconn()

    cur = conn.cursor()

    cur.execute('''
    INSERT INTO users (username, password, role)
    VALUES (%s, %s, 'user')
    ON CONFLICT (username) DO NOTHING;
    ''', (username, password))

    created = cur.rowcount > 0
    conn.commit()
    cur.close()
    db_pool.putconn(conn)

    return created