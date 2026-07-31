from backend.extensions import db
from backend.models import User
from werkzeug.security import generate_password_hash
from datetime import datetime


def create_default_data():
    """Create only system + admin if they don't exist. No demo/test users."""
    try:
        # System user (needed for international transfers)
        if not User.query.filter_by(username="system").first():
            system = User(
                username="system",
                email="system@unitedbankofamerica.com",
                password_hash=generate_password_hash("System@2026!Secure"),
                pin_hash=generate_password_hash("123456"),
                is_admin=False,
                balance=0.0,
                is_active=True,
                is_verified=True,
                created_at=datetime.utcnow(),
            )
            db.session.add(system)
            db.session.commit()
            print("✅ System user created.")

        # Admin – only if none exists
        if not User.query.filter_by(is_admin=True).first():
            admin = User(
                username="bankmanager",
                email="unitedbankofamericasupport@gmail.com",
                password_hash=generate_password_hash("Bankmanager@2026"),
                pin_hash=generate_password_hash("123456"),
                is_admin=True,
                balance=0.0,
                is_active=True,
                is_verified=True,
                created_at=datetime.utcnow(),
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin created: bankmanager / Bankmanager@2026 / PIN: 123456")
        else:
            print("✅ Admin already exists.")
    except Exception as e:
        db.session.rollback()
        msg = str(e).lower()
        if "locked" in msg or "already exists" in msg:
            pass  # harmless on SQLite reloader
        else:
            print(f"⚠️ Seed warning: {e}")
