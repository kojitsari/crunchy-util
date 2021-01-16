import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, anime_name):
    """ create a table from the create_table statement
    :param conn: Connection object
    :param anime_name: a CREATE TABLE statement
    :return:
    """
    sql = f""" CREATE TABLE IF NOT EXISTS {anime_name} (
                                        episode_num integer NOT NULL,
                                        episode_name text NOT NULL,
                                        episode_url text NOT NULL,
                                        unique_id integer NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def insert_data(conn, anime_name, episode_nums, episode_names, episode_urls, unique_id):
    """
    Create a new project into the projects table
    :param conn:
    :param anime_name:
    :return: episode_url
    """
    sql = f''' INSERT INTO {anime_name} (episode_num, episode_name, episode_url, unique_id)
               VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (episode_nums, episode_names, episode_urls, unique_id))
    conn.commit()
    return cur.lastrowid

def update_data(conn, anime_name, episode_nums, episode_names, episode_urls, unique_id):
    """
    update episode_num, episode_name, episode_url
    :param conn:
    :param anime_name:
    :return: episode_num
    """
    sql = f''' UPDATE {anime_name}
              SET episode_name ? ,
                  episode_url ?,
                  unique_id ?
              WHERE episode_num = ?'''
    cur = conn.cursor()
    cur.execute(sql, (episode_nums, episode_names, episode_urls, unique_id))
    conn.commit()

def delete_data(conn, anime_name):
    sql = f'DROP Table {anime_name}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def query_data(conn, anime_name):
    """
    query episode_num, episode_name, episode_url
    :param conn:
    :param anime_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {anime_name} ORDER BY unique_id asc")

    rows = cur.fetchall()
    
    return rows
