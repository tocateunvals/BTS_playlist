# src/fetch_spotify_data.py
import os
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Cargar credenciales
load_dotenv()

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    ))

def get_db_connection():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'db', 'bts_playlist.db')
    return sqlite3.connect(db_path)

def get_or_create_artist(cursor, name, artist_type):
    """Busca el artista en la DB. Si no existe, lo crea."""
    cursor.execute("SELECT id FROM artists WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    
    # Si no existe, lo insertamos (sin spotify_id por ahora para simplificar)
    cursor.execute(
        "INSERT INTO artists (name, artist_type, is_bts_related) VALUES (?, ?, 1)", 
        (name, artist_type)
    )
    return cursor.lastrowid

def fetch_and_save_data():
    sp = get_spotify_client()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Lista de artistas a buscar
    artists_to_fetch = [
        ("BTS", "group"),
        ("RM", "solo"),
        ("Jin", "solo"),
        ("SUGA", "solo"),
        ("Agust D", "alias"), # A veces Spotify lo lista separado
        ("j-hope", "solo"),
        ("Jimin", "solo"),
        ("V", "solo"),
        ("Jung Kook", "solo")
    ]

    for artist_name, artist_type in artists_to_fetch:
        print(f" Buscando artista: {artist_name}...")
        
        # 1. Buscar ID de Spotify
        results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
        if not results['artists']['items']:
            print(f"  ⚠️ No se encontró a {artist_name}. Saltando.")
            continue
            
        artist_data = results['artists']['items'][0]
        spotify_artist_id = artist_data['id']
        print(f"  ✅ Encontrado: {artist_data['name']} (ID: {spotify_artist_id})")

        # Actualizar el ID en nuestra DB
        cursor.execute("UPDATE artists SET spotify_artist_id = ? WHERE name = ?", (spotify_artist_id, artist_name))
        
        # Obtener ID local de nuestra DB
        local_artist_id = get_or_create_artist(cursor, artist_name, artist_type)

        # 2. Obtener Top Tracks
        # Nota: artist_top_tracks requiere un código de país. Usamos 'AR' (Argentina) o 'US'.
        top_tracks = sp.artist_top_tracks(spotify_artist_id, country='AR')
        
        track_ids = [track['id'] for track in top_tracks['tracks']]
        
        # 3. Obtener Audio Features (Energy, Valence, etc.)
        # Dividimos en lotes de 50 porque la API tiene ese límite por llamada
        features_list = []
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i+50]
            features = sp.audio_features(batch)
            features_list.extend(features)

        # 4. Guardar en SQLite
        for track, features in zip(top_tracks['tracks'], features_list):
            if not features: continue # Si no hay features, saltar
            
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO tracks 
                    (spotify_track_id, artist_id, title, album, popularity, energy, valence, danceability, acousticness, is_group, is_solo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    track['id'],
                    local_artist_id,
                    track['name'],
                    track['album']['name'],
                    track['popularity'],
                    features['energy'],
                    features['valence'],
                    features['danceability'],
                    features['acousticness'],
                    1 if artist_type == 'group' else 0,
                    1 if artist_type == 'solo' else 0
                ))
            except Exception as e:
                print(f"   Error guardando track {track['name']}: {e}")

        print(f"  💾 Guardados {len(top_tracks['tracks'])} tracks de {artist_name}.")

    conn.commit()
    conn.close()
    print("\n🎉 ¡Proceso de extracción y carga finalizado!")

if __name__ == "__main__":
    fetch_and_save_data()