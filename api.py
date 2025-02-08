from fastapi import FastAPI, HTTPException

from db_functions import get_meal_plan, get_meal_by_id, find_replacement_meal

app = FastAPI()


@app.get("/weekly_plan")
def weekly_plan_endpoint(budget: float = 50.0):
    """
    GET /weekly_plan?budget=50.0

    Returns a weekly meal plan for the provided budget (in dollars).
    """
    result = get_meal_plan(budget_cents=int(budget * 100))
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    plan, total_cost = result
    response = {"weekly_plan": plan, "total_cost": total_cost}  # in cents
    return response


@app.get("/replace_meal")
def replace_meal_endpoint(meal_id: int, curr_price: int, budget: int):
    """
    Endpoint to replace a given meal with a similar one within the budget constraints.
    """
    original_meal = get_meal_by_id(meal_id)
    if not original_meal:
        raise HTTPException(status_code=404, detail="Meal not found.")

    replacement_meal = find_replacement_meal(
        meal_type=original_meal["meal_type"],
        exclude_id=original_meal["id"],
        curr_price=curr_price - original_meal["cost"],
        budget=budget,
    )

    if not replacement_meal:
        raise HTTPException(status_code=404, detail="No similar meal found.")

    return {"original_meal": original_meal, "replacement_meal": replacement_meal}


# To run the app, use: uvicorn <this_module_name>:app --reload
