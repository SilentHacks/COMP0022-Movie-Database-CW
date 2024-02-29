ALTER TABLE movie_people
    ADD COLUMN "order" INTEGER DEFAULT 0 NOT NULL;

CREATE INDEX movie_people_order_idx ON movie_people ("order");