# src/db_utils.py
import sqlite3
import os

def get_db_connection():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'db', 'bts_playlist.db')
    return sqlite3.connect(db_path)

def save_user_response(listens_bts, mood, artist_1, artist_2, artist_3):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Guardamos la respuesta en la tabla user_responses que creamos en el schema.sql
    cursor.execute('''
        INSERT INTO user_responses (listens_bts, mood, artist_1, artist_2, artist_3)
        VALUES (?, ?, ?, ?, ?)
    ''', (listens_bts, mood, artist_1 or None, artist_2 or None, artist_3 or None))
    
    conn.commit()
    conn.close()