import uuid
from passlib.context import CryptContext
from app.db.database import session
from app.model.User import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin():
    db = session()
    try:
        existing = db.query(User).filter(User.role == "admin").first()
        if existing:
            print("✅ Admin already exists:", existing.email)
            return
        password = "password"
        admin = User(
            id=str(uuid.uuid4()),
            name="Super Admin",
            email="admin@medicrm.com",
            password = pwd_context.hash(password[:72]),
            role="admin",
            specialization="Administration",
            status=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin created successfully!")
        print("📧 Email   : admin@medicrm.com")
        print("🔑 Password: password")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()