import asyncio
import os
from datetime import datetime

import asyncpg
import pandas as pd
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


def parse_ratings():
    ratings_insert = []
    ratings_df = pd.read_csv('./scripts/data/ratings.csv')
    for row in ratings_df.itertuples():
        ratings_insert.append((row[1], row[2], row[3], datetime.strptime(row[4].strip(), '%Y-%m-%d %H:%M:%S')))

    users_insert = []
    personality_df = pd.read_csv('./scripts/data/personality-data.csv')
    for row in personality_df.itertuples():
        users_insert.append((row[1], row[2], row[3], row[4], row[5], row[6]))

    return users_insert, ratings_insert


async def populate_db():
    users_insert, ratings_insert = parse_ratings()

    pool = await db_connect()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany('INSERT INTO users (id, openness, agreeableness, emotional_stability, '
                                   'conscientiousness, extraversion) VALUES ($1, $2, $3, $4, $5, $6) '
                                   'ON CONFLICT (id) DO NOTHING', users_insert)

            # Filter ratings_insert to include only rows with valid movie_ids
            # because the dataset somehow contains ratings for movies that don't exist in the movies dataset
            # that they THEMSELVES provide
            valid_movie_ids = await conn.fetch('SELECT id FROM movies')
            valid_movie_ids_set = {row['id'] for row in valid_movie_ids}
            valid_ratings_insert = [rating for rating in ratings_insert if rating[1] in valid_movie_ids_set]

            await conn.executemany('INSERT INTO user_ratings (user_id, movie_id, rating, created_at, updated_at) '
                                   'VALUES ($1, $2, $3, $4, $4) ON CONFLICT (user_id, movie_id) DO NOTHING',
                                   valid_ratings_insert)

    await pool.close()


def main():
    asyncio.run(populate_db())


if __name__ == "__main__":
    main()
