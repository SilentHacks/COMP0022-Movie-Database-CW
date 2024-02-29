ALTER TABLE users
    ADD COLUMN openness REAL CHECK (openness >= 0 AND openness <= 7),
    ADD COLUMN agreeableness REAL CHECK (agreeableness >= 0 AND agreeableness <= 7),
    ADD COLUMN emotional_stability REAL CHECK (emotional_stability >= 0 AND emotional_stability <= 7),
    ADD COLUMN conscientiousness REAL CHECK (conscientiousness >= 0 AND conscientiousness <= 7),
    ADD COLUMN extraversion REAL CHECK (extraversion >= 0 AND extraversion <= 7);