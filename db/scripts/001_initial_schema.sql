-- Create the initial schema for the Postgres database

CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY,
    title TEXT NOT NULL
);

INSERT INTO movies (id, title) VALUES
(1, 'The Shawshank Redemption');