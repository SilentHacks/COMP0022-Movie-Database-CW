import asyncio
import json
import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv

load_dotenv()

credentials = {
    "user": os.getenv('POSTGRESQL_USERNAME'),
    "password": os.getenv('POSTGRESQL_PASSWORD'),
    "database": os.getenv('POSTGRESQL_DATABASE'),
    "port": 5432
}


async def db_connect():
    return await asyncpg.create_pool(**credentials)


def parse_movie_data():
    with open('./scripts/data/formatted_movies.json') as f:
        data = json.load(f)

    genres = {}
    people = {}
    movie_genres_insert = []
    movies_insert = []
    movie_people_insert = []

    for movie in data:
        for genre in movie['genres']:
            genres[genre['id']] = genre['name']  # Doesn't matter if we overwrite, we just want the unique ones
            movie_genres_insert.append((movie['id'], genre['id']))

        for actor in movie['actors']:
            people[actor['id']] = (actor['name'], actor['profile_path'])
            movie_people_insert.append((movie['id'], actor['id'], 'Actor', actor['character']))

        for director in movie['directors']:
            people[director['id']] = (director['name'], director['profile_path'])
            movie_people_insert.append((movie['id'], director['id'], 'Director', None))

        release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')
        movies_insert.append((movie['id'], movie['title'], movie['imdb_id'], movie['tmdb_id'], release_date,
                              movie['runtime'], movie['tagline'], movie['overview'], movie['poster_path'],
                              movie['backdrop_path'], movie['budget'], movie['revenue'], movie['status']))

    return genres, people, movies_insert, movie_people_insert, movie_genres_insert


async def batch_insert(conn, query, values, batch=1000):
    for i in range(0, len(values), batch):
        print(f"Inserting {i + 1} to {i + batch} of {len(values)}")
        await conn.executemany(query, values[i:i + batch])


async def populate_db():
    genres, people, movies_insert, movie_people_insert, movie_genres_insert = parse_movie_data()
    genres_insert = [(genre_id, name) for genre_id, name in genres.items()]
    people_insert = [(person_id, *value) for person_id, value in people.items()]

    pool = await db_connect()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await batch_insert(conn, 'INSERT INTO movies (id, title, imdb_id, tmdb_id, release_date, runtime, tagline, '
                                   'overview, poster_path, backdrop_path, budget, revenue, status) '
                                   'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) '
                                   'ON CONFLICT DO NOTHING', movies_insert)
            await batch_insert(conn,'INSERT INTO people (id, name, profile_path) '
                                   'VALUES ($1, $2, $3) ON CONFLICT DO NOTHING', people_insert)
            await batch_insert(conn,'INSERT INTO movie_people (movie_id, person_id, role, character_name) '
                                   'VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING', movie_people_insert)
            await batch_insert(conn,'INSERT INTO genres (id, name) '
                                   'VALUES ($1, $2) ON CONFLICT DO NOTHING', genres_insert)
            await batch_insert(conn,'INSERT INTO movie_genres (movie_id, genre_id) '
                                   'VALUES ($1, $2) ON CONFLICT DO NOTHING', movie_genres_insert)

    await pool.close()


def main():
    asyncio.get_event_loop().run_until_complete(populate_db())


if __name__ == "__main__":
    main()
