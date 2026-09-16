from app.db.database import session
from app.model.Role import Permissions
from app.core.module import MODULES


def seed_permissions():
    db = session()
    
    actions = ["view", "create", "edit", "delete"]
    
    no_create_modules = ["follow-ups"]

    modules = [
        module_key
        for group in MODULES.values()
        for module_key in group["modules"].keys()
    ]

    total_created = 0

    try:
        for module in modules:
            for action in actions:
                if action == "create" and module in no_create_modules:
                    continue

                slug = f"{module}.{action}"
                label = f"{action.capitalize()} {module.replace('-', ' ').title()}"

                existing = db.query(Permissions).filter(Permissions.slug == slug).first()
                
                if not existing:
                    perm = Permissions(permission=label, slug=slug)
                    db.add(perm)
                    total_created += 1
                    print(f" Created: {slug}")
                else:
                    print(f" Already exists: {slug}")

        db.commit()
        print(f"\n Permission seeding complete! Created {total_created} new permissions.\n")

    except Exception as e:
        db.rollback()
        print(f"\n Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_permissions()
