import os

# Optional: load .env file if present (pip install python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from backend import create_app

app = create_app("development")

if __name__ == "__main__":
    if not os.environ.get("DATABASE_URL"):
        print()
        print("💡 Tip: To use Supabase PostgreSQL, set DATABASE_URL first:")
        print('   PowerShell:  $env:DATABASE_URL="postgresql://USER:PASS@HOST:5432/postgres"')
        print('   CMD:         set DATABASE_URL=postgresql://USER:PASS@HOST:5432/postgres')
        print("   Then run:    python run.py")
        print()
    app.run(debug=True, host="0.0.0.0", port=5000)
