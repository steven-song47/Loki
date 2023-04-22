# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from flask import Flask
from flask_migrate import Migrate
from app import create_app, db
from app.model import case_model


app = create_app(config_name="default")
migrate = Migrate(app, db)


@app.route("/")
def index():
    return "Welcome"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6001, debug=True)
