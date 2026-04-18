CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

INSERT INTO users (username, password) VALUES
('admin', 'supersecret'),
('user1', 'password123'),
('guest', 'guestpass');