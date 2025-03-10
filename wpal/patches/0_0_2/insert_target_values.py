import frappe

def execute():
    # version 0.0.1 has these values listed as options in Select field.
    default_targets = ["Back", "Legs"]

    for target in default_targets:
        if not frappe.db.exists("Target", target):  # Avoid duplicates
            doc = frappe.get_doc({
                "doctype": "Target",
                "target": target
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    frappe.msgprint("Default Targets have been inserted successfully!", alert=True)