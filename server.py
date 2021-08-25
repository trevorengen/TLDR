from flask_app.controllers.notebooks import notebooks
from flask_app import app
from flask_app.controllers import users, notebooks

if __name__=='__main__':
    app.run(debug=True)
