CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  user_name VARCHAR NOT NULL,
  user_pass VARCHAR NOT NULL
);

INSERT INTO accounts (user_name, user_pass) VALUES ('dima', 'dima');
INSERT INTO accounts (user_name, user_pass) VALUES ('bob', 'bob');

CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbh VARCHAR NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  isbh VARCHAR NOT NULL,
  rate_score INTEGER NOT NULL,
  rate_text VARCHAR NOT NULL
);

INSERT INTO reviews (user_id, isbh, rate_score, rate_text) VALUES (1, '0743234413', 5, 'Very interesting book');
INSERT INTO reviews (user_id, isbh, rate_score, rate_text) VALUES (2, '0743234413', 4, 'New ideas can be seen');
