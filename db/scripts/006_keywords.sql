CREATE TABLE IF NOT EXISTS keywords (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movie_keywords (
    movie_id INT NOT NULL,
    keyword_id INT NOT NULL,
    PRIMARY KEY (movie_id, keyword_id),
    FOREIGN KEY (movie_id) REFERENCES movies (id),
    FOREIGN KEY (keyword_id) REFERENCES keywords (id)
);