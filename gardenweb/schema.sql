DROP TABLE IF EXISTS bed;
DROP TABLE IF EXISTS planting;

CREATE TABLE bed (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       top_left REAL NOT NULL,
       x_length REAL NOT NULL,
       y_length REAL NOT NULL
       );

CREATE TABLE planting (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       bed_id INTEGER NOT NULL,
       top_left REAL NOT NULL,
       x_length REAL NOT NULL,
       y_length REAL NOT NULL,
       plant_type TEXT NOT NULL,
       date_planted TEXT NOT NULL,
       date_harvested TEXT NOT NULL,
       FOREIGN KEY (bed_id) REFERENCES bed (id)
       );
