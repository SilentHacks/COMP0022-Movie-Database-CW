CREATE OR REPLACE FUNCTION calculate_popularity(average_rating NUMERIC, num_reviews BIGINT)
RETURNS FLOAT AS $$
BEGIN
    RETURN COALESCE(average_rating * LOG(num_reviews + 1), 0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE VIEW movies_view AS
	WITH aggregated_movies AS (
		SELECT
		    m.id, m.title, m.imdb_id, m.tmdb_id, m.release_date, m.runtime,
		    m.tagline, m.overview, m.poster_path, m.backdrop_path, m.budget, m.revenue,
		    m.status, m.created_at, m.updated_at,
		    COALESCE(AVG(ur.rating), 0) AS average_rating,
		    COUNT(ur.rating) AS num_reviews,
		    array_agg(DISTINCT g.name) AS genres,
		    COALESCE(
		        (
		            SELECT json_agg(jsonb_build_object('name', p.name, 'role', mp.role, 'character_name', mp.character_name,
		                                                'profile_path', p.profile_path, 'order', mp."order") ORDER BY mp."order")
		            FROM movie_people mp
		            JOIN people p ON mp.person_id = p.id
		            WHERE mp.movie_id = m.id AND mp.role = 'Actor'
		        ),
		        '[]'
		    ) AS actors,
		    COALESCE(
		        (
		            SELECT json_agg(jsonb_build_object('name', p.name, 'role', mp.role, 'profile_path', p.profile_path))
		            FROM movie_people mp
		            JOIN people p ON mp.person_id = p.id
		            WHERE mp.movie_id = m.id AND mp.role = 'Director'
		        ),
		        '[]'
		    ) AS directors
		FROM movies m
		LEFT JOIN movie_genres mg ON m.id = mg.movie_id
		LEFT JOIN genres g ON mg.genre_id = g.id
		LEFT JOIN user_ratings ur ON m.id = ur.movie_id
		GROUP BY m.id
	)
	SELECT
		*,
		calculate_popularity(average_rating, num_reviews) AS popularity
	FROM aggregated_movies;