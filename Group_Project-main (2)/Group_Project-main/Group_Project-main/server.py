from flask_app import app
from flask_app.controllers import  users, trainers

from flask_app.models import user
from flask_app.models import trainer



if __name__ == "__main__":
    app.run(debug=True,port=5000)