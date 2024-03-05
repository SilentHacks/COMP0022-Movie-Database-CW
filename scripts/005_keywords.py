import asyncio
import json
import os

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

    keywords = {}
    movie_keywords_insert = []

    for movie in data:
        for keyword in movie['keywords']['keywords']:
            keywords[keyword['id']] = keyword['name']
            movie_keywords_insert.append((movie['id'], keyword['id']))

    keywords_insert = [(k, v) for k, v in keywords.items()]

    return keywords_insert, movie_keywords_insert


async def batch_insert(conn, query, values, batch=1000):
    for i in range(0, len(values), batch):
        print(f"Inserting {i + 1} to {i + batch} of {len(values)}")
        await conn.executemany(query, values[i:i + batch])


async def populate_db():
    keywords_insert, movie_keywords_insert = parse_movie_data()

    pool = await db_connect()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await batch_insert(conn,'INSERT INTO keywords (id, name) VALUES ($1, $2)', keywords_insert)
            await batch_insert(conn,'INSERT INTO movie_keywords (movie_id, keyword_id) VALUES ($1, $2)',
                                   movie_keywords_insert)

    await pool.close()


def main():
    asyncio.run(populate_db())


if __name__ == "__main__":
    main()
