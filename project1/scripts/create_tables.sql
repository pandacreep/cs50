CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  user_name VARCHAR NOT NULL,
  user_pass VARCHAR NOT NULL
);

INSERT INTO accounts (user_name, user_pass) VALUES ('dima', 'dima');
INSERT INTO accounts (user_name, user_pass) VALUES ('bob', 'bob');
