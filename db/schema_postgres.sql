-- schema_postgres.sql
-- Esquema adaptado para PostgreSQL (Neon.tech)

CREATE TABLE IF NOT EXISTS artists (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    artist_type TEXT CHECK(artist_type IN ('group', 'solo', 'alias')) NOT NULL,
    is_bts_related BOOLEAN DEFAULT TRUE,
    spotify_artist_id TEXT
);

CREATE TABLE IF NOT EXISTS tracks (
    id SERIAL PRIMARY KEY,
    spotify_track_id TEXT UNIQUE,
    artist_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    album TEXT,
    is_group BOOLEAN DEFAULT FALSE,
    is_solo BOOLEAN DEFAULT FALSE,
    popularity INTEGER DEFAULT 0,
    energy REAL,
    valence REAL,
    danceability REAL,
    acousticness REAL,
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE IF NOT EXISTS user_responses (
    id SERIAL PRIMARY KEY,
    listens_bts TEXT CHECK(listens_bts IN ('yes', 'no')) NOT NULL,
    mood TEXT NOT NULL,
    artist_1 TEXT,
    artist_2 TEXT,
    artist_3 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);