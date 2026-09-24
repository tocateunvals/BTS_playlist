import sqlite3
import os

def seed_artists():
    # Ajustar la ruta para que funcione desde cualquier directorio
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'db', 'bts_playlist.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lista de artistas base: (name, artist_type, is_bts_related)
    artists = [
        ('BTS', 'group', 1),
        ('RM', 'solo', 1),
        ('Jin', 'solo', 1),
        ('SUGA', 'solo', 1),
        ('Agust D', 'alias', 1),
        ('j-hope', 'solo', 1),
        ('Jimin', 'solo', 1),
        ('V', 'solo', 1),
        ('Jung Kook', 'solo', 1)
    ]

    # Insertar ignorando duplicados si se corre el script dos veces
    cursor.executemany('''
        INSERT OR IGNORE INTO artists (name, artist_type, is_bts_related)
        VALUES (?, ?, ?)
    ''', artists)

    conn.commit()
    
    # Verificación rápida
    cursor.execute("SELECT COUNT(*) FROM artists")
    count = cursor.fetchone()[0]
    print(f"Éxito. Base de datos poblada con {count} artistas iniciales.")
    
    conn.close()

if __name__ == '__main__':
    seed_artists()