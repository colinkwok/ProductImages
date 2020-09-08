DROP TABLE IF EXISTS PRODUCT;

CREATE TABLE PRODUCT (
  id INTEGER PRIMARY KEY,
  gender TEXT,
  masterCategory TEXT,
  subCategory TEXT,
  articleType TEXT,
  baseColour TEXT,
  season TEXT,
  year INTEGER,
  usage TEXT,
  productDisplayName TEXT
);