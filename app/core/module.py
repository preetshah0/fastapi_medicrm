# app/core/module.py

MODULES = {
    "medical_care": {
        "label": "Patient Care",
        "modules": {
            "patients": {
                "label": "Patient Management",
                "description": "Comprehensive patient records and profile management",
            },
            "appointments": {
                "label": "Appointment Scheduling",
                "description": "Real-time calendar and appointment booking system",
            },
            "prescriptions": {
                "label": "Prescriptions",
                "description": "Digital prescription creation and history tracking",
            },
            "follow-ups": {
                "label": "Follow-up Tracking",
                "description": "Automated and manual follow-up management for patients",
            },
            "patient-notes": {
                "label": "Patient Notes",
                "description": "Clinical consultation notes and medical history logs for patients",
            },
            "patient-reports": {
                "label": "Patient Reports & Attachments",
                "description": "Diagnostic test reports, attachments, and medical documents",
            },
            "lab_referrals": {
                "label": "Laboratory Referrals",
                "description": "Track patient test referrals to external laboratory facilities",
            },
        },
    },

    "inventory_management": {
        "label": "Inventory & Pharmacy",
        "modules": {
            "products": {
                "label": "Product Master",
                "description": "Central repository for medicine and medical supply data",
            },
            "product-categories": {
                "label": "Product Categories",
                "description": "Categorize and classify medicines, drugs, and medical equipment",
            },
            "inventory-batches": {
                "label": "Batch & Expiry Management",
                "description": "Track stock levels by batches, purchase details, and expiry dates",
            },
            "sales": {
                "label": "Sales & Billing",
                "description": "Generate invoices, track sales transactions, and handle billing",
            },
        },
    },

    "operations": {
        "label": "Medical Operations",
        "modules": {
            "medical_representatives": {
                "label": "Medical Representatives (MR)",
                "description": "Manage MR visits, scheduling, and sample distributions",
            },
            "external_laboratories": {
                "label": "Laboratory Facilities",
                "description": "Manage partner laboratory facilities and test catalog details",
            },
            "suppliers": {
                "label": "Suppliers Management",
                "description": "Track suppliers, vendors, and purchase orders",
            },
        },
    },

    "management": {
        "label": "Organization Management",
        "modules": {
            "branches": {
                "label": "Multi-Branch Management",
                "description": "Manage multiple clinic locations and branch settings",
            },
            "team": {
                "label": "Team Management",
                "description": "Assign roles to members and manage team accounts",
            },
            "roles": {
                "label": "Role & Permission Management",
                "description": "Define custom RBAC roles and configure access control permissions",
            },
            "master-options": {
                "label": "Master Options & Settings",
                "description": "Configure system-wide master option types, lookups, and dropdown values",
            }
        },
    },
}

