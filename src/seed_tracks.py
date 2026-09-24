import sqlite3
import os

def seed_tracks():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'db', 'bts_playlist.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Función auxiliar para obtener el ID del artista por su nombre
    def get_artist_id(name):
        cursor.execute("SELECT id FROM artists WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    # Lista de tracks mockeados
    # Formato: (artist_name, title, album, is_group, is_solo, popularity, energy, valence, danceability, acousticness)
    # Nota: energy, valence, danceability, acousticness van de 0.0 a 1.0
    # popularity va de 0 a 100
    
    tracks_data = [
        ('BTS', 'Dynamite', 'BE', 1, 0, 95, 0.85, 0.92, 0.80, 0.02),  # Feliz, Fiesta
        ('BTS', 'Spring Day', 'You Never Walk Alone', 1, 0, 88, 0.45, 0.30, 0.55, 0.25),  # Melancólico, Nostalgia
        ('BTS', 'Blood Sweat & Tears', 'Wings', 1, 0, 85, 0.65, 0.35, 0.68, 0.10),  # Nocturno, Intenso
        ('BTS', 'Mikrokosmos', 'Map of the Soul: Persona', 1, 0, 82, 0.60, 0.50, 0.60, 0.15),  # Esperanzador, Nocturno
        ('BTS', 'IDOL', 'Love Yourself 結 Answer', 1, 0, 90, 0.90, 0.75, 0.75, 0.05),  # Energético, Fiesta
        ('RM', 'Seoul', 'mono.', 0, 1, 70, 0.40, 0.35, 0.65, 0.45),  # Introspectivo, Tranquilo
        ('Agust D', 'Daechwita', 'D-2', 0, 1, 85, 0.88, 0.55, 0.80, 0.01),  # Hip Hop, Energético
        ('j-hope', 'Chicken Noodle Soup', 'Chicken Noodle Soup', 0, 1, 80, 0.92, 0.80, 0.85, 0.05),  # Fiesta, Hype
        ('Jimin', 'Filter', 'Map of the Soul: 7', 0, 1, 82, 0.75, 0.85, 0.82, 0.10),  # Feliz, Latino/Pop
        ('V', 'Slow Dancing', 'Layover', 0, 1, 88, 0.55, 0.60, 0.65, 0.30),  # R&B, Nocturno
        ('Jung Kook', 'Seven', 'Golden', 0, 1, 96, 0.78, 0.80, 0.75, 0.12),  # Pop, Energético
        ('Jung Kook', 'Still With You', 'Golden', 0, 1, 85, 0.35, 0.25, 0.40, 0.85),  # Melancólico, Acústico
        ('Jin', 'The Astronaut', 'The Astronaut', 0, 1, 84, 0.65, 0.45, 0.50, 0.15),  # Espacial, Medio
    ]

    inserted_count = 0
    for track in tracks_data:
        artist_name = track[0]
        artist_id = get_artist_id(artist_name)
        
        if artist_id:
            try:
                cursor.execute('''
                    INSERT INTO tracks 
                    (artist_id, title, album, is_group, is_solo, popularity, energy, valence, danceability, acousticness)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (artist_id, track[1], track[2], track[3], track[4], track[5], track[6], track[7], track[8], track[9]))
                inserted_count += 1
            except sqlite3.IntegrityError:
                pass # Ignorar si ya existe

    conn.commit()
    print(f"Éxito. Se insertaron {inserted_count} tracks en la base de datos.")
    conn.close()

if __name__ == '__main__':
    seed_tracks()