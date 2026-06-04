-- Database schema for Smart-Gate
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS access_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL, -- 'AUTHORIZED', 'DENIED'
    confidence REAL,
    image_path TEXT, -- Path to photo if intruder or record
    FOREIGN KEY (user_id) REFERENCES users(id)
);
