CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    artist_type TEXT CHECK(artist_type IN ('group', 'solo', 'alias')) NOT NULL,
    is_bts_related BOOLEAN DEFAULT 1,
    spotify_artist_id TEXT
);

CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    album TEXT,
    release_date TEXT,
    is_group BOOLEAN DEFAULT 0,
    is_solo BOOLEAN DEFAULT 0,
    is_collab BOOLEAN DEFAULT 0,
    is_remix BOOLEAN DEFAULT 0,
    popularity INTEGER DEFAULT 0,
    energy REAL,
    valence REAL,
    danceability REAL,
    acousticness REAL,
    spotify_track_id TEXT,
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    UNIQUE(artist_id, title, album)
);

CREATE TABLE IF NOT EXISTS user_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    listens_bts TEXT CHECK(listens_bts IN ('yes', 'no')),
    mood TEXT,
    artist_1 TEXT,
    artist_2 TEXT,
    artist_3 TEXT
);