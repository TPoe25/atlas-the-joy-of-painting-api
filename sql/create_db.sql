DROP TABLE IF EXISTS episode_subjects;
DROP TABLE IF EXISTS episode_colors;
DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS colors;
DROP TABLE IF EXISTS subjects;


CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    season INT,
    episode INT,
    air_date DATE,
    month_of_air INT,
    img_url TEXT,
    youtube_url TEXT
);

CREATE TABLE colors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    hex TEXT
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE episode_colors (
    episode_id INT REFERENCES episodes(id) ON DELETE CASCADE,
    color_id INT REFERENCES colors(id) ON DELETE CASCADE,
    PRIMARY KEY (episode_id, color_id)
);

CREATE TABLE episode_subjects (
    episode_id INT REFERENCES episodes(id) ON DELETE CASCADE,
    subject_id INT REFERENCES subjects(id) ON DELETE CASCADE,
    PRIMARY KEY (episode_id, subject_id)
);
