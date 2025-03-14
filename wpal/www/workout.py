import frappe

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

    # Pass data to the template
    context.targets = targets
    context.target_workouts = target_workouts

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