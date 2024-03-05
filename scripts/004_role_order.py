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

    movie_people_update = []

    for movie in data:
        for actor in movie['actors']:
            movie_people_update.append((movie['id'], actor['id'], actor['order']))

    return movie_people_update


async def batch_insert(conn, query, values, batch=1000):
    for i in range(0, len(values), batch):
        print(f"Inserting {i + 1} to {i + batch} of {len(values)}")
        await conn.executemany(query, values[i:i + batch])


async def populate_db():
    movie_people_update = parse_movie_data()

    pool = await db_connect()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await batch_insert(conn,'UPDATE movie_people SET "order" = $3 WHERE movie_id = $1 AND person_id = $2',
                                   movie_people_update)

    await pool.close()


def main():
    asyncio.run(populate_db())


if __name__ == "__main__":
    main()
