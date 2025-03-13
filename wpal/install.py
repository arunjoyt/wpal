import frappe
def after_install():
    default_targets = ['Cardio', 'Triceps', 'Shoulders', 'Chest', 'Biceps', 'Abs', 'Legs', 'Back']
    for target in default_targets:
        if not frappe.db.exists("Target", target):
            doc = frappe.get_doc({
                "doctype" : "Target",
                "target" : target
                }
            )
            doc.insert()