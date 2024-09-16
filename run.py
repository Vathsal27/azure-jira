from azurejira import app
from azurejira.ms_graph import subscribe_to_folder

with app.app_context():
    subscribe_to_folder()

if __name__ == "__main__":
    app.run(debug=True)