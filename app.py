from flask import Flask, render_template, request
from ga.ga_engine import run_weekly_ga, calculate_day_totals, validate_calories

app = Flask(__name__)

# ---------------- PAGE 1 ----------------
@app.route("/", methods=["GET"])
def form():
    return render_template("form.html")

# ---------------- PAGE 2 ----------------
@app.route("/generate", methods=["POST"])

def generate():
    target_calories = int(request.form["target_calories"])
    goal = request.form["goal"]
    budget = float(request.form["budget"])
    diet_type = request.form["diet_type"]
    meal_count = int(request.form["meals"])
    meals = int(request.form["meals"])

    allergies_input = request.form.get("allergies", "")
    allergies = [a.strip().lower() for a in allergies_input.split(",") if a]

    # Goal adjustment
    if goal == "weight_loss":
        target_calories -= 300
    elif goal == "weight_gain":
        target_calories += 300

    user = {
        "target_calories": target_calories,
        "target_protein": 75,
        "target_carbs": 250,
        "target_fats": 70,
        "budget": budget,
        "diet_type": diet_type,
        "allergies": allergies,
        "meals": meal_count,
        "meals": meals
    }

    weekly_plan = run_weekly_ga(user)

    week_data = []
    for day in weekly_plan:
        totals = calculate_day_totals(day)
        valid = validate_calories(totals["calories"], target_calories)

        week_data.append({
            "meals": day,
            "totals": totals,
            "valid": valid
        })

    return render_template(
        "result.html",
        week=week_data,
        target=target_calories
    )

if __name__ == "__main__":
    app.run(debug=True)
