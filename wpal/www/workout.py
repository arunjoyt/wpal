import frappe
from datetime import datetime, timedelta

def get_context(context):
    # Fetch all targets
    targets = frappe.get_all("Target", fields=["name as target_name"])

    # Fetch all workouts with their target
    workouts = frappe.get_all("Workout", fields=["name as workout_name", "target"])

    # Organize workouts by target
    target_workouts = {}
    for workout in workouts:
        target = workout["target"]
        if target not in target_workouts:
            target_workouts[target] = []
        target_workouts[target].append(workout["workout_name"])

    # Fetch last 10 workout entries
    workout_history = frappe.get_all(
        "Workout Entry",
        fields=["date", "time", "workout", "comments"],
        order_by="date desc, time desc",
        limit_page_length=10
    )

    # Get the start of the current week (Monday)
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week

    # Fetch unique targets along with date and day for workouts done in the current week
    weekly_targets = frappe.db.sql("""
        SELECT DISTINCT WE.date, DAYNAME(WE.date) AS day, W.target 
        FROM `tabWorkout Entry` WE
        JOIN `tabWorkout` W ON WE.workout = W.name
        WHERE WE.date >= %s
        ORDER BY WE.date ASC
    """, (start_of_week.strftime('%Y-%m-%d')), as_dict=True)

    # Pass data to the template
    context.targets = targets
    context.target_workouts = target_workouts
    context.workout_history = workout_history
    context.weekly_targets = weekly_targets
    
@frappe.whitelist()
def create_workout_entry(date, time, workout, comments, sets):
    try:
        # Convert JSON string to Python list
        sets = frappe.parse_json(sets)

        # Create the Workout Entry document
        doc = frappe.get_doc({
            "doctype": "Workout Entry",
            "date": date,
            "time": time,
            "workout": workout,
            "comments": comments,
            "table_tqlh": sets  # Child table data
        })
        doc.insert()

        return {"status": "success", "message": "Workout Entry Saved!"}

    except Exception as e:
        frappe.log_error(f"Workout Entry Error: {str(e)}")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def create_workout(workout_name, target):
    # Check if workout already exists
    if frappe.db.exists("Workout", workout_name):
        return {"status": "error", "message": "Workout already exists."}

    # Create a new Workout document
    workout = frappe.get_doc({
        "doctype": "Workout",
        "workout_name": workout_name,
        "target": target
    })

    try:
        workout.insert()
        return {"status": "success", "message": "Workout created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}