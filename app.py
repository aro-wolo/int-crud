from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(256), nullable=False)
  active = db.Column(db.Boolean, default=True)


with app.app_context():
  db.create_all()

@app.route('/user', methods=['POST'])
def create_user():
  data = request.json 
  new_user = User(username=data['username'], password=data['password'], active = True)
  db.session.add(new_user)
  db.session.commit()

  return jsonify({'message': 'User was created successfully'}), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
  user = User.query.get_or_404(id)
  return jsonify({'id': user.id, 'username': user.username, 'active': user.active}), 200

@app.route('/users', methods=['GET'])
def get_users():
  users = User.query.all()
  return jsonify(
    [{
      'id': user.id, 'username': user.username, 'active': user.active
    } for user in users]
  ), 200

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
  user = User.query.get_or_404(id)
  data = request.json
  user.username = data['username']
  user.password = data['password']
  db.session.commit()
  return jsonify({'message': 'User was updated successfully'}), 200

@app.route('/user/<int:id>/deactivate', methods=['PATCH'])
def deactivate(id):
  activate_disactive(id, False)
  return jsonify({'message': 'User now de-activated'}), 200

@app.route('/user/<int:id>/activate', methods=['PATCH'])
def activate(id):
  activate_disactive(id, True)
  return jsonify({'message': 'User now activated'}), 200

def activate_disactive(id: int,  value:bool):
  user = User.query.get_or_404(id)
  user.active = value
  db.session.commit()

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get_or_404(id)
  db.session.delete(user)
  db.session.commit()
  return jsonify({'message': 'User was deleted successfully'}), 200

if __name__ == '__main__':
  app.run(debug=True)