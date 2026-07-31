import os
import json
from flask import Flask
from backend.config import config, get_database_uri
from backend.extensions import db, login_manager, csrf


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "production")
    if config_name not in config:
        config_name = "production"

    app = Flask(
        __name__,
        template_folder=os.path.join(
            os.path.dirname(__file__), "..", "frontend", "templates"
        ),
        static_folder=os.path.join(
            os.path.dirname(__file__), "..", "frontend", "static"
        ),
    )
    app.config.from_object(config[config_name])

    # Always resolve DB URL from environment at runtime
    db_uri = get_database_uri()
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

    # Soften SQLite locking when using the debug reloader
    if db_uri.startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"timeout": 30, "check_same_thread": False}
        }

    # Show which database is in use (helps debug Supabase vs SQLite)
    if "postgresql" in db_uri or "postgres" in db_uri:
        # Mask password in log
        safe = db_uri
        if "@" in safe:
            safe = safe.split("@")[-1]
        print(f"🗄️  Database: PostgreSQL → …@{safe}")
    else:
        print(f"🗄️  Database: SQLite (set DATABASE_URL to use Supabase)")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    def json_loads_filter(data):
        try:
            return json.loads(data) if data else {}
        except Exception:
            return {}

    app.jinja_env.filters["json_loads"] = json_loads_filter

    from backend.routes.main import main_bp
    from backend.routes.auth import auth_bp
    from backend.routes.user import user_bp
    from backend.routes.admin import admin_bp
    from backend.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    from backend.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create tables + seed only once (skip on Flask reloader child process)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        with app.app_context():
            try:
                db.create_all()
                from backend.database_setup import create_default_data
                create_default_data()
            except Exception as e:
                # Ignore "table already exists" / lock races – app still runs
                msg = str(e).lower()
                if "already exists" not in msg and "locked" not in msg:
                    print(f"⚠️ Database init warning: {e}")

    try:
        from backend.cli import add_pins_command
        app.cli.add_command(add_pins_command)
    except Exception:
        pass

    return app


# Used by gunicorn on Render:  web: gunicorn backend:app
app = create_app()
