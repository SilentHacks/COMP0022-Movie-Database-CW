ALTER TABLE movies
ALTER COLUMN created_at TYPE timestamptz USING created_at AT TIME ZONE 'UTC',
ALTER COLUMN updated_at TYPE timestamptz USING updated_at AT TIME ZONE 'UTC';

ALTER TABLE people
ALTER COLUMN created_at TYPE timestamptz USING created_at AT TIME ZONE 'UTC',
ALTER COLUMN updated_at TYPE timestamptz USING updated_at AT TIME ZONE 'UTC';

ALTER TABLE users
ALTER COLUMN created_at TYPE timestamptz USING created_at AT TIME ZONE 'UTC',
ALTER COLUMN updated_at TYPE timestamptz USING updated_at AT TIME ZONE 'UTC';

ALTER TABLE user_ratings
ALTER COLUMN created_at TYPE timestamptz USING created_at AT TIME ZONE 'UTC',
ALTER COLUMN updated_at TYPE timestamptz USING updated_at AT TIME ZONE 'UTC';

ALTER TABLE keywords
ALTER COLUMN created_at TYPE timestamptz USING created_at AT TIME ZONE 'UTC',
ALTER COLUMN updated_at TYPE timestamptz USING updated_at AT TIME ZONE 'UTC';