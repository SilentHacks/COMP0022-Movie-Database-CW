CREATE MATERIALIZED VIEW rating_over_expected_by_genre AS
	WITH MovieAvgRatingsExclUser AS (
	    SELECT
	        r1.movie_id,
	        r1.user_id,
	        CASE
	        	WHEN COUNT(r2.rating) - 1 = 0 THEN NULL
	            ELSE (SUM(r2.rating) - r1.rating) / NULLIF(COUNT(r2.rating) - 1, 0)
			END AS avg_rating_excl_user
	    FROM
	        user_ratings r1
	    JOIN
	        user_ratings r2 ON r1.movie_id = r2.movie_id AND r1.user_id != r2.user_id
	    GROUP BY
	        r1.movie_id, r1.user_id, r1.rating
	),
	UserRatingAboveExpected AS (
	    SELECT
	        mar.movie_id,
	        mar.user_id,
	        r.rating - mar.avg_rating_excl_user AS rating_above_expected
	    FROM
	        MovieAvgRatingsExclUser mar
	    JOIN
			user_ratings r ON mar.movie_id = r.movie_id AND mar.user_id = r.user_id
	),
	UserGenreRatingAboveExpected AS (
	    SELECT
	        urae.user_id,
	        g.name,
	        AVG(urae.rating_above_expected) AS avg_rating_above_expected
	    FROM
	        UserRatingAboveExpected urae
	    JOIN
	        movie_genres mg ON urae.movie_id = mg.movie_id
	    JOIN
	        genres g ON mg.genre_id = g.id
	    GROUP BY
	        urae.user_id, g.name
	)
	SELECT
	    *
	FROM
	    UserGenreRatingAboveExpected
	ORDER BY
	    user_id, avg_rating_above_expected DESC;