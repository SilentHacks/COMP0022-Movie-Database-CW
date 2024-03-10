ALTER TABLE movie_people
    ADD COLUMN "order" INTEGER DEFAULT 0 NOT NULL;
ALTER TABLE movie_people
    DROP CONSTRAINT movie_people_pkey;
ALTER TABLE movie_people
    ADD PRIMARY KEY (movie_id, person_id, role, "order");