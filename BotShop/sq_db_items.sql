CREATE TABLE IF NOT EXISTS items (
item_id INTEGER PRIMARY KEY AUTOINCREMENT,
item_name TEXT NOT NULL,
item_descr TEXT NOT NULL,
item_picid TEXT NOT NULL,
item_price INTEGER NOT NULL,
item_category TEXT NOT NULL
);