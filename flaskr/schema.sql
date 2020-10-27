DROP TABLE IF EXISTS usertemp CASCADE;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS thread;
DROP TABLE IF EXISTS post;

CREATE TABLE usertemp (
  ID  SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE category (
    ID  SERIAL PRIMARY KEY,
    title TEXT NOT NULL
);

INSERT INTO category (
  title)
VALUES('Spill'),('Dyr'),('Grønnsaker');

CREATE TABLE thread (
    ID  SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category_id INTEGER
    
);

INSERT INTO thread (
  title, category_id)
VALUES('Halo','1'),('League of Legends','1'),('Katt','2'),('Hund','2'),('Brokkoli','3'),('Gresskar','3');

CREATE TABLE post (
  ID  SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  post_username TEXT UNIQUE NOT NULL,
  body TEXT NOT NULL,
  thread_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES usertemp (id),
  FOREIGN KEY (post_username) REFERENCES usertemp (username)
);