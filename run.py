from app import create_app
from dotenv import load_dotenv

# creating app instance
app = create_app()

if __name__ == '__main__':
    load_dotenv(override=True)
    app.run(debug=True)