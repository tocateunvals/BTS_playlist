# src/recommender.py
import sqlite3
import os
import math

MOOD_PROFILES = {
    "feliz": [0.8, 0.9, 0.8, 0.1],
    "tranquilo": [0.3, 0.6, 0.4, 0.7],
    "melancólico": [0.3, 0.2, 0.4, 0.6],
    "nocturno": [0.5, 0.3, 0.6, 0.2],
    "energético": [0.9, 0.8, 0.9, 0.1]
}

MOCK_REFERENCE_ARTISTS = {
    "Taylor Swift": [0.65, 0.55, 0.60, 0.25],
    "The Weeknd": [0.75, 0.40, 0.70, 0.05],
    "Billie Eilish": [0.40, 0.35, 0.65, 0.40],
    "Coldplay": [0.60, 0.50, 0.55, 0.20],
    "Bad Bunny": [0.80, 0.70, 0.85, 0.10],
    "Lana Del Rey": [0.35, 0.25, 0.45, 0.50],
    "Arctic Monkeys": [0.70, 0.45, 0.65, 0.15]
}

def get_db_connection():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'db', 'bts_playlist.db')
    return sqlite3.connect(db_path)

def calculate_distance(point_a, point_b):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point_a, point_b)))

def calculate_mean_vector(vectors):
    n = len(vectors)
    if n == 0: return [0, 0, 0, 0]
    dims = len(vectors[0])
    return [sum(vec[i] for vec in vectors) / n for i in range(dims)]

def get_user_profile(artist_names):
    vectors = [MOCK_REFERENCE_ARTISTS[name] for name in artist_names if name in MOCK_REFERENCE_ARTISTS]
    return calculate_mean_vector(vectors)

def get_recommendations(mood=None, artists=None, listens_to_bts="no", limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Lógica simple: si no escucha BTS, solo recomendaremos canciones grupales (is_group = 1)
    # Si ya escucha, podemos incluir solistas también.
    if listens_to_bts == "no":
        cursor.execute('''
            SELECT t.title, a.name, t.energy, t.valence, t.danceability, t.acousticness, t.is_group
            FROM tracks t JOIN artists a ON t.artist_id = a.id
            WHERE t.is_group = 1
        ''')
    else:
        cursor.execute('''
            SELECT t.title, a.name, t.energy, t.valence, t.danceability, t.acousticness, t.is_group
            FROM tracks t JOIN artists a ON t.artist_id = a.id
        ''')
        
    tracks = cursor.fetchall()
    conn.close()

    # Definir el vector objetivo
    target_profile = None
    if mood and artists:
        mood_vector = MOOD_PROFILES.get(mood, [0,0,0,0])
        artist_vector = get_user_profile(artists)
        target_profile = [(m + a) / 2 for m, a in zip(mood_vector, artist_vector)]
    elif mood:
        target_profile = MOOD_PROFILES.get(mood, [0,0,0,0])
    elif artists:
        target_profile = get_user_profile(artists)
    else:
        return [] # Si no hay ni mood ni artistas, no hay perfil

    recommendations = []
    for track in tracks:
        title, artist, energy, valence, danceability, acousticness, is_group = track
        track_profile = [energy, valence, danceability, acousticness]
        distance = calculate_distance(target_profile, track_profile)
        
        # Guardamos también si es grupal o solista para mostrarlo en la UI
        track_type = "Grupal" if is_group else "Solista"
        recommendations.append({
            "title": title, 
            "artist": artist, 
            "type": track_type,
            "distance": distance
        })

    recommendations.sort(key=lambda x: x["distance"])
    return recommendations[:limit]