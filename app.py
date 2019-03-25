from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('thankyou.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

# from flask_bootstrap import Bootstrap
# from flask import Flask, render_template, request, jsonify, url_for
# from flask_sqlalchemy import SQLAlchemy
# import os
#
# # initialization
# app = Flask(__name__)
# Bootstrap(app)
#
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#
# # extensions
# db = SQLAlchemy(app)
#
# db.session.execute('CREATE TABLE IF NOT EXISTS "users" ('
#                'id INTEGER NOT NULL UNIQUE,'
#                'username TEXT NOT NULL, '
#                'email TEXT NOT NULL, '
#                'PRIMARY KEY (id));')
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(32), index=True)
#     email = db.Column(db.String(32), index=True)
#
#     def __init__(self, email):
#         self.email = email
#         self.username = "anon"
#
#     def __repr__(self):
#         return '<E-mail %r>' % self.email
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# # Save e-mail to database and send to success page
# @app.route('/prereg', methods=['POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(User).filter(User.email == email).count():
#             reg = User(username=username, email=email)
#             db.session.add(reg)
#             db.session.commit()
#             return render_template('thankyou.html')
#     return render_template('index.html')
#
#
# @app.route('/api/users', methods=['POST', 'GET'])
# def signup():
#     username = request.form['username']
#     email = request.form['email']
#
#     if username is None or email is None:
#         abort(400)
#
#     user = User(username=username, email=email)
#     db.session.add(user)
#     db.session.commit()
#
#     return render_template('thankyou.html')
#
# if __name__ == '__main__':
#     if not os.path.exists('db.sqlite'):
#         db.create_all()
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, threaded=True)
#
