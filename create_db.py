import sqlite3


def create_database():
    conn = sqlite3.connect("food_database.db")
    cursor = conn.cursor()

    # Create recipes table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            image TEXT NOT NULL,
            meal_type TEXT,
            total_cost REAL,
            total_cost_per_serving REAL
        )
    """
    )

    # Create ingredients table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            image TEXT NOT NULL,
            price REAL NOT NULL,
            amount_metric_value REAL NOT NULL,
            amount_metric_unit TEXT NOT NULL,
            amount_us_value REAL NOT NULL,
            amount_us_unit TEXT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """
    )

    conn.commit()
    conn.close()


create_database()
print("Database and tables created (or updated) successfully.")
