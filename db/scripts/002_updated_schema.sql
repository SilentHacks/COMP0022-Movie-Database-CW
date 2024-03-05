-- This is an interesting design choice. This table acts as an ad-hoc enum type.
-- Although usually you may see an ID column, we can enforce the same constraints
-- by using a primary key on the name column. This removes the extra join needed
-- to get the name of the status while keeping the values much more flexible than the built-in enum type.
-- If the status table were to be large or frequently changing, then an ID column would be more efficient.
-- The same is true for the roles table.
CREATE TABLE IF NOT EXISTS statuses (
    name TEXT PRIMARY KEY
);

ALTER TABLE movies
    ALTER COLUMN status TYPE TEXT USING status::TEXT,
    ADD CONSTRAINT fk_status FOREIGN KEY (status) REFERENCES statuses (name) ON UPDATE CASCADE;

ALTER TABLE roles
    ALTER COLUMN id DROP IDENTITY;
ALTER TABLE roles
    DROP CONSTRAINT roles_pkey CASCADE;
ALTER TABLE roles
    DROP COLUMN id;
ALTER TABLE roles
    ADD PRIMARY KEY (name);

ALTER TABLE people
    ALTER COLUMN id DROP IDENTITY;

ALTER TABLE movie_people
    ALTER COLUMN role_id TYPE TEXT USING role_id::TEXT;
ALTER TABLE movie_people
	RENAME COLUMN role_id TO role;
ALTER TABLE movie_people
	ADD CONSTRAINT movie_people_role_fkey FOREIGN KEY (role) REFERENCES roles (name) ON UPDATE CASCADE;

-- People spend and make more money than int32 lol
ALTER TABLE movies
    ALTER COLUMN budget TYPE BIGINT,
    ALTER COLUMN revenue TYPE BIGINT;

-- Add indexes on commonly queried columns
CREATE INDEX movies_title_idx ON movies (title);