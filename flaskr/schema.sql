DROP TABLE IF EXISTS usertemp;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS thread;
DROP TABLE IF EXISTS post;

CREATE TABLE usertemp (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

INSERT INTO category (
  title)
VALUES('Spill'),('Dyr'),('Grønnsaker');

CREATE TABLE thread (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category_id INTEGER
    
);

INSERT INTO thread (
  title, category_id)
VALUES('Halo','1'),('League of Legends','1'),("Baldur's Gate 3",'1'),('Katt','2'),('Hund','2'),("Ape",'2'),('Brokkoli','3'),('Gresskar','3'),("Potet",'3');

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  /*title TEXT NOT NULL,*/
  body TEXT NOT NULL,
  thread_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);