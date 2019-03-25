from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# initialization
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)

db.session.execute('CREATE TABLE IF NOT EXISTS "users" ('
               'id INTEGER NOT NULL UNIQUE,'
               'username TEXT NOT NULL, '
               'email TEXT NOT NULL, '
               'PRIMARY KEY (id));')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    email = db.Column(db.String(32), index=True)

    # password_hash = db.Column(db.String(64))

    # def hash_password(self, password):
    #     self.password_hash = pwd_context.encrypt(password)

    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash)

    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({'id': self.id})

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None    # valid token, but expired
    #     except BadSignature:
    #         return None    # invalid token
    #     user = User.query.get(data['id'])
    #     return user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['POST', 'GET'])
def signup():
    username = request.form['username']
    email = request.form['email']

    if username is None or email is None:
        abort(400)

    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return render_template('thankyou.html')

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

