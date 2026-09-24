import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def test_connection():
    try:
        # Autenticación (Client Credentials Flow para datos públicos)
        auth_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # Búsqueda de prueba: Buscar a BTS
        results = sp.search(q='artist:BTS', type='artist', limit=1)
        
        if results['artists']['items']:
            artist = results['artists']['items'][0]
            print("✅ Conexión exitosa!")
            print(f"Artista encontrado: {artist['name']}")
            print(f"Spotify ID: {artist['id']}")
            print(f"Géneros: {', '.join(artist['genres'])}")
        else:
            print("❌ No se encontró al artista.")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_connection()