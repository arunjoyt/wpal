import frappe

def get_context(context):
    context.workouts = frappe.get_all("Workout", fields=["workout_name"])

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