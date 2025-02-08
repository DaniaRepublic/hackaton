import requests
import sqlite3

API_KEY = "171d9d76f62d4d3e876762b5357bb818"
URL = "https://api.spoonacular.com/"


def fetch_recipe(query: str, n: int = 10):
    uri = "recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "query": query,
        "number": n,
    }
    response = requests.get(URL + uri, params=params)
    return response.json()


def fetch_ingredients(recipeId: int):
    uri = f"recipes/{recipeId}/priceBreakdownWidget.json"
    params = {"apiKey": API_KEY}
    response = requests.get(URL + uri, params=params)
    return response.json()


def insert_recipe(recipe, meal_type, total_cost, total_cost_per_serving):
    conn = sqlite3.connect("food_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO recipes (id, title, image, meal_type, total_cost, total_cost_per_serving) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            recipe["id"],
            recipe["title"],
            recipe["image"],
            meal_type,
            total_cost,
            total_cost_per_serving,
        ),
    )

    conn.commit()
    conn.close()


def insert_ingredients(recipe_id, ingredients):
    conn = sqlite3.connect("food_database.db")
    cursor = conn.cursor()

    for ingredient in ingredients:
        cursor.execute(
            """
            INSERT INTO ingredients 
            (recipe_id, name, image, price, amount_metric_value, amount_metric_unit, amount_us_value, amount_us_unit) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                recipe_id,
                ingredient["name"],
                ingredient["image"],
                ingredient["price"],
                ingredient["amount"]["metric"]["value"],
                ingredient["amount"]["metric"]["unit"],
                ingredient["amount"]["us"]["value"],
                ingredient["amount"]["us"]["unit"],
            ),
        )

    conn.commit()
    conn.close()


def recipe_exists(recipe_id):
    """Check if a recipe already exists in the database."""
    conn = sqlite3.connect("food_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM recipes WHERE id = ?", (recipe_id,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists


def populate_database(foods, meal_type: str):
    recipes_data = foods
    if "results" in recipes_data:
        for recipe in recipes_data["results"]:
            if recipe_exists(recipe["id"]):
                print(f"Skipping existing recipe: {recipe['title']}")
                continue  # Skip fetching ingredients if recipe is already in DB

            print(f"Fetching recipe: {recipe['title']}")

            # Fetch ingredients, which also contains totalCost & totalCostPerServing
            ingredients_data = fetch_ingredients(recipe["id"])
            total_cost = ingredients_data.get("totalCost", 0.0)
            total_cost_per_serving = ingredients_data.get("totalCostPerServing", 0.0)

            # Insert recipe along with cost details
            insert_recipe(recipe, meal_type, total_cost, total_cost_per_serving)

            # Insert ingredients if available
            if "ingredients" in ingredients_data:
                insert_ingredients(recipe["id"], ingredients_data["ingredients"])


breakfast = {
    "results": [
        {
            "id": 649567,
            "title": "Lemon Coconut Granola",
            "image": "https://img.spoonacular.com/recipes/649567-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 632949,
            "title": "Asparagus Quiche",
            "image": "https://img.spoonacular.com/recipes/632949-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 644690,
            "title": "Gingerbread Pancakes",
            "image": "https://img.spoonacular.com/recipes/644690-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 647268,
            "title": "Honey Pine Nuts Muffins",
            "image": "https://img.spoonacular.com/recipes/647268-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 632884,
            "title": "Asian Soft Scrambled Eggs",
            "image": "https://img.spoonacular.com/recipes/632884-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 661758,
            "title": "Strawberry Banana Stuffed Pancakes",
            "image": "https://img.spoonacular.com/recipes/661758-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 637184,
            "title": "Carrot Cake Pancakes",
            "image": "https://img.spoonacular.com/recipes/637184-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 665767,
            "title": "Zucchini Pineapple Muffins",
            "image": "https://img.spoonacular.com/recipes/665767-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 637792,
            "title": "Cherry, Date & Nut Muffins",
            "image": "https://img.spoonacular.com/recipes/637792-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 649300,
            "title": "Latkes; Fried Vegetable Pancakes from Europe and the Middle East",
            "image": "https://img.spoonacular.com/recipes/649300-312x231.jpg",
            "imageType": "jpg",
        },
    ],
    "offset": 0,
    "number": 10,
    "totalResults": 476,
}

lunch_dinner = {
    "results": [
        {
            "id": 642583,
            "title": "Farfalle with Peas, Ham and Cream",
            "image": "https://img.spoonacular.com/recipes/642583-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 660185,
            "title": "Singapore Curry",
            "image": "https://img.spoonacular.com/recipes/660185-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 641836,
            "title": "Easy Baked Parmesan Chicken",
            "image": "https://img.spoonacular.com/recipes/641836-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 636177,
            "title": "Broccoli Cheddar Soup",
            "image": "https://img.spoonacular.com/recipes/636177-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 632502,
            "title": "Apple Cheddar Turkey Burgers With Chipotle Yogurt Sauce",
            "image": "https://img.spoonacular.com/recipes/632502-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 660275,
            "title": "Slow Cooker Beef Barley Soup",
            "image": "https://img.spoonacular.com/recipes/660275-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 667704,
            "title": "Shrimp, Bacon, Avocado Pasta Salad",
            "image": "https://img.spoonacular.com/recipes/667704-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 665446,
            "title": "X-Country Double Lobster Risotto",
            "image": "https://img.spoonacular.com/recipes/665446-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 646870,
            "title": "Home Made Dry-Aged Sirloin Steak with Cheesy Roast Fingerling Potatoes",
            "image": "https://img.spoonacular.com/recipes/646870-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 1095873,
            "title": "Cheesy Tortellini Casserole",
            "image": "https://img.spoonacular.com/recipes/1095873-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 648257,
            "title": "Italian Steamed Artichokes",
            "image": "https://img.spoonacular.com/recipes/648257-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 157021,
            "title": "Gnocci with vegetables and feta",
            "image": "https://img.spoonacular.com/recipes/157021-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 663357,
            "title": "The Unagi Burger",
            "image": "https://img.spoonacular.com/recipes/663357-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 471151,
            "title": "Grilled Pineapple Pork Chops",
            "image": "https://img.spoonacular.com/recipes/471151-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 1096224,
            "title": "Baked Almond-Crusted Cod With Sauteed Bok Choy and Bell Peppers",
            "image": "https://img.spoonacular.com/recipes/1096224-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 1697751,
            "title": "Ridiculously Easy Gourmet Tuna Sandwich",
            "image": "https://img.spoonacular.com/recipes/1697751-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 632778,
            "title": "Artisan Farfalle Pasta With Smoked Salmon and Cream Sauce",
            "image": "https://img.spoonacular.com/recipes/632778-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 642722,
            "title": "Fettuccine With Smashed Peas",
            "image": "https://img.spoonacular.com/recipes/642722-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 633953,
            "title": "Balsamic Wheat & Chicken Salad",
            "image": "https://img.spoonacular.com/recipes/633953-312x231.jpg",
            "imageType": "jpg",
        },
        {
            "id": 641975,
            "title": "Easy Ginger Beef Broccoli",
            "image": "https://img.spoonacular.com/recipes/641975-312x231.jpg",
            "imageType": "jpg",
        },
    ],
    "offset": 0,
    "number": 20,
    "totalResults": 1715,
}

if __name__ == "__main__":
    populate_database(breakfast, "breakfast")
    populate_database(lunch_dinner, "lunch_dinner")
    print("Database populated successfully.")
