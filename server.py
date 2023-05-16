from flask_app import app
from flask_app.controllers import login_controller


if __name__ == '__main__':
    app.run(debug=True)

# To start, run the below code in cmd
# pipenv install PyMySQL flask flask-bcrypt
# pipenv shell
# python server.py
