# src/seed_tracks.py
import sqlite3
import os

def seed_tracks():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'db', 'bts_playlist.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def get_artist_id(name):
        cursor.execute("SELECT id FROM artists WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    # Lista ampliada de tracks mockeados
    # Formato: (artist_name, title, album, is_group, is_solo, popularity, energy, valence, danceability, acousticness)
    tracks_data = [
        # --- BTS (Grupo) ---
        ('BTS', 'Dynamite', 'BE', 1, 0, 95, 0.85, 0.92, 0.80, 0.02),
        ('BTS', 'Spring Day', 'You Never Walk Alone', 1, 0, 88, 0.45, 0.30, 0.55, 0.25),
        ('BTS', 'Blood Sweat & Tears', 'Wings', 1, 0, 85, 0.65, 0.35, 0.68, 0.10),
        ('BTS', 'Mikrokosmos', 'Map of the Soul: Persona', 1, 0, 82, 0.60, 0.50, 0.60, 0.15),
        ('BTS', 'IDOL', 'Love Yourself 結 Answer', 1, 0, 90, 0.90, 0.75, 0.75, 0.05),
        ('BTS', 'Black Swan', 'Map of the Soul: 7', 1, 0, 80, 0.50, 0.20, 0.55, 0.35),
        ('BTS', 'ON', 'Map of the Soul: 7', 1, 0, 86, 0.95, 0.40, 0.75, 0.05),
        ('BTS', 'Life Goes On', 'BE', 1, 0, 84, 0.30, 0.45, 0.40, 0.85),
        ('BTS', 'Butter', 'Butter', 1, 0, 96, 0.80, 0.90, 0.85, 0.05),
        ('BTS', 'Fake Love', 'Love Yourself 轉 Tear', 1, 0, 87, 0.85, 0.25, 0.70, 0.10),
        ('BTS', 'DNA', 'Love Yourself 承 Her', 1, 0, 89, 0.80, 0.85, 0.85, 0.05),
        ('BTS', 'Not Today', 'You Never Walk Alone', 1, 0, 83, 0.90, 0.50, 0.75, 0.05),
        ('BTS', 'Euphoria', 'Love Yourself 結 Answer', 1, 0, 85, 0.80, 0.85, 0.75, 0.10),
        ('BTS', 'Singularity', 'Love Yourself 轉 Tear', 1, 0, 81, 0.35, 0.25, 0.50, 0.60),

        # --- RM ---
        ('RM', 'Wild Flower', 'Indigo', 0, 1, 78, 0.40, 0.30, 0.45, 0.75),
        ('RM', 'Still Life', 'Indigo', 0, 1, 75, 0.50, 0.40, 0.55, 0.40),
        ('RM', 'Seoul', 'mono.', 0, 1, 70, 0.40, 0.35, 0.65, 0.45),

        # --- Jin ---
        ('Jin', 'The Astronaut', 'The Astronaut', 0, 1, 84, 0.65, 0.45, 0.50, 0.15),
        ('Jin', 'Super Tuna', 'Super Tuna', 0, 1, 72, 0.80, 0.95, 0.70, 0.10),

        # --- SUGA / Agust D ---
        ('Agust D', 'Daechwita', 'D-2', 0, 1, 85, 0.88, 0.55, 0.80, 0.01),
        ('Agust D', 'Haegeum', 'D-DAY', 0, 1, 82, 0.85, 0.50, 0.80, 0.10),
        ('SUGA', 'People Pt.2', 'D-DAY', 0, 1, 79, 0.60, 0.45, 0.65, 0.30),

        # --- j-hope ---
        ('j-hope', 'MORE', 'Jack In The Box', 0, 1, 80, 0.90, 0.60, 0.85, 0.05),
        ('j-hope', 'Arson', 'Jack In The Box', 0, 1, 78, 0.92, 0.40, 0.75, 0.05),
        ('j-hope', 'Chicken Noodle Soup', 'Chicken Noodle Soup', 0, 1, 80, 0.92, 0.80, 0.85, 0.05),

        # --- Jimin ---
        ('Jimin', 'Like Crazy', 'FACE', 0, 1, 88, 0.70, 0.60, 0.75, 0.15),
        ('Jimin', 'Filter', 'Map of the Soul: 7', 0, 1, 82, 0.75, 0.85, 0.82, 0.10),
        ('Jimin', 'Set Me Free Pt.2', 'FACE', 0, 1, 84, 0.85, 0.55, 0.70, 0.10),

        # --- V ---
        ('V', 'Slow Dancing', 'Layover', 0, 1, 88, 0.55, 0.60, 0.65, 0.30),
        ('V', 'Love Me Again', 'Layover', 0, 1, 85, 0.60, 0.70, 0.65, 0.20),
        ('V', 'Rainy Days', 'Layover', 0, 1, 80, 0.30, 0.35, 0.40, 0.80),

        # --- Jung Kook ---
        ('Jung Kook', 'Seven', 'Golden', 0, 1, 96, 0.78, 0.80, 0.75, 0.12),
        ('Jung Kook', 'Still With You', 'Golden', 0, 1, 85, 0.35, 0.25, 0.40, 0.85),
        ('Jung Kook', '3D', 'Golden', 0, 1, 90, 0.70, 0.75, 0.80, 0.10),
        ('Jung Kook', 'Standing Next to You', 'Golden', 0, 1, 92, 0.85, 0.80, 0.85, 0.05)
    ]

    inserted_count = 0
    for track in tracks_data:
        artist_name = track[0]
        artist_id = get_artist_id(artist_name)
        
        if artist_id:
            try:
                # INSERT OR IGNORE evita duplicados si el script se corre varias veces
                cursor.execute('''
                    INSERT OR IGNORE INTO tracks 
                    (artist_id, title, album, is_group, is_solo, popularity, energy, valence, danceability, acousticness)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (artist_id, track[1], track[2], track[3], track[4], track[5], track[6], track[7], track[8], track[9]))
                if cursor.rowcount > 0:
                    inserted_count += 1
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    print(f"Éxito. Se insertaron {inserted_count} nuevos tracks en la base de datos.")
    conn.close()

if __name__ == '__main__':
    seed_tracks()