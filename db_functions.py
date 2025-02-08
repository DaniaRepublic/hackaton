import sqlite3
import random


def get_all_recipes():
    """
    Fetch all recipes from the database that have a valid total_cost_per_serving.
    Each recipe is returned as a dictionary with 'cost' (in cents) as total_cost_per_serving.
    """
    conn = sqlite3.connect("food_database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, image, total_cost_per_serving, meal_type
        FROM recipes
        WHERE total_cost_per_serving IS NOT NULL
        """
    )
    rows = cursor.fetchall()
    conn.close()

    recipes = [
        {
            "id": row[0],
            "title": row[1],
            "image": row[2],
            "cost": row[3],  # total_cost_per_serving, in cents
            "meal_type": row[4],
        }
        for row in rows
    ]
    return recipes


def get_meal_plan(budget_cents):
    """
    Generates a weekly meal plan (7 days x 3 meals = 21 meals) such that:
      - 7 breakfast meals (meal_type == "breakfast")
      - 14 lunch/dinner meals (meal_type == "lunch_dinner")
    and the sum of their total_cost_per_serving does not exceed the provided budget (in cents).

    Returns:
      weekly_plan: a list of 7 days (each day is a list [breakfast, lunch, dinner])
      total_cost: total cost of the selected meals (in cents)
    """
    recipes = get_all_recipes()
    if not recipes:
        return {"error": "No recipes available."}

    # Partition recipes into two groups.
    breakfast_recipes = [r for r in recipes if r["meal_type"] == "breakfast"]
    lunch_dinner_recipes = [r for r in recipes if r["meal_type"] == "lunch_dinner"]

    if len(breakfast_recipes) == 0:
        return {"error": "No breakfast recipes available."}
    if len(lunch_dinner_recipes) == 0:
        return {"error": "No lunch/dinner recipes available."}

    # Compute the cheapest cost in each group.
    cheapest_breakfast = min(r["cost"] for r in breakfast_recipes)
    cheapest_lunch_dinner = min(r["cost"] for r in lunch_dinner_recipes)

    # Check if the budget is sufficient for the minimum required meals.
    if budget_cents < (cheapest_breakfast * 7 + cheapest_lunch_dinner * 14):
        return {"error": "Budget too low to select required meals."}

    # Selection for breakfast: need 7 meals.
    selected_breakfast = []
    remaining_budget = budget_cents
    max_attempts = 1000
    attempts = 0

    while len(selected_breakfast) < 7 and attempts < max_attempts:
        attempts += 1

        # Get all breakfast recipes affordable with the current remaining budget.
        affordable = [
            meal for meal in breakfast_recipes if meal["cost"] <= remaining_budget
        ]
        if not affordable:
            # If none is affordable, remove the most expensive selected breakfast to free up some budget.
            if selected_breakfast:
                most_expensive = max(selected_breakfast, key=lambda m: m["cost"])
                selected_breakfast.remove(most_expensive)
                remaining_budget += most_expensive["cost"]
                print(
                    f"Removed expensive breakfast: {most_expensive['title']} to free up budget."
                )
                continue
            else:
                return {"error": "Unable to build a breakfast plan within the budget."}

        # If the remaining budget is very low, pick the cheapest affordable breakfast.
        if remaining_budget < cheapest_breakfast * 2:
            meal = min(affordable, key=lambda m: m["cost"])
        else:
            meal = random.choice(affordable)

        selected_breakfast.append(meal)
        remaining_budget -= meal["cost"]

    # Selection for lunch/dinner: need 14 meals.
    selected_lunch_dinner = []
    attempts = 0
    while len(selected_lunch_dinner) < 14 and attempts < max_attempts:
        attempts += 1
        affordable = [
            meal for meal in lunch_dinner_recipes if meal["cost"] <= remaining_budget
        ]
        if not affordable:
            if selected_lunch_dinner:
                most_expensive = max(selected_lunch_dinner, key=lambda m: m["cost"])
                selected_lunch_dinner.remove(most_expensive)
                remaining_budget += most_expensive["cost"]
                print(
                    f"Removed expensive lunch/dinner: {most_expensive['title']} to free up budget."
                )
                continue
            else:
                return {
                    "error": "Unable to build a lunch/dinner plan within the budget."
                }
        if remaining_budget < cheapest_lunch_dinner * 2:
            meal = min(affordable, key=lambda m: m["cost"])
        else:
            meal = random.choice(affordable)
        selected_lunch_dinner.append(meal)
        remaining_budget -= meal["cost"]

    if len(selected_breakfast) < 7 or len(selected_lunch_dinner) < 14:
        return {
            "error": "Unable to select required meals within the budget after many attempts."
        }

    # Construct the weekly plan.
    # Each day gets one breakfast and two lunch/dinner meals.
    weekly_plan = []
    for i in range(7):
        day_breakfast = selected_breakfast[i]
        day_lunch = selected_lunch_dinner[i * 2]
        day_dinner = selected_lunch_dinner[i * 2 + 1]
        weekly_plan.append([day_breakfast, day_lunch, day_dinner])

    total_cost = budget_cents - remaining_budget
    return weekly_plan, total_cost


# Example usage:
if __name__ == "__main__":
    budget_dollars = 50
    result = get_meal_plan(budget_cents=budget_dollars * 100)

    if isinstance(result, dict) and "error" in result:
        print("Error:", result["error"])
    else:
        plan, total_cost = result
        print(f"Total cost: {total_cost / 100:.2f}")
        for day_index, day in enumerate(plan, start=1):
            print(f"Day {day_index}:")
            for meal in day:
                print(
                    f"  - {meal['meal_type']} {meal['title']} (${meal['cost'] / 100:.2f})"
                )
