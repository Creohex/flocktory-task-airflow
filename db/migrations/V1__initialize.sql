-- create tables:

CREATE TABLE level(
    level VARCHAR(10) PRIMARY KEY NOT NULL
);

CREATE TABLE logs(
    id SERIAL PRIMARY KEY NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (level) REFERENCES level (level)
);

CREATE TABLE logs_hourly_stats(
    id SERIAL PRIMARY KEY NOT NULL,
    hour TIMESTAMP NOT NULL,
    level VARCHAR(10) NOT NULL,
    num_messages INT NOT NULL CHECK (num_messages > 0),

    FOREIGN KEY (level) REFERENCES level (level)
);

CREATE TABLE incidents(
    id SERIAL PRIMARY KEY NOT NULL,
    --hour TIMESTAMP NOT NULL CHECK ((EXTRACT(MINUTE FROM TIMESTAMP hour)) == 0 AND (EXTRACT(MINUTE FROM TIMESTAMP hour)) == 0),
    hour TIMESTAMP NOT NULL,
    num_errors INT NOT NULL CHECK (num_errors >= 0)
);

-- insert default values:
INSERT INTO level(level) VALUES ('TRACE'), ('DEBUG'), ('INFO'), ('WARN'), ('ERROR');
