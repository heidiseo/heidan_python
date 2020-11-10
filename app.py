from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os

# Init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
# to find db.sqlite file in the current folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
# not to have the warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db for activity and user
activity_db = SQLAlchemy(app)
user_db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)

# Activity Schema
class ActivitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'description', 'cost', 'complete')

# Init schema
activity_schema = ActivitySchema()

activities_schema = ActivitySchema(many=True)

# Activity Class/Model
class Activity(activity_db.Model):
    __tablename__ = 'activities'
    id = activity_db.Column(activity_db.Integer, primary_key=True)
    name = activity_db.Column(activity_db.String(100), unique=True)
    location = activity_db.Column(activity_db.String(300))
    description = activity_db.Column(activity_db.String(200))
    cost = activity_db.Column(activity_db.Float)
    complete = activity_db.Column(activity_db.Boolean)

    def __init__(self, name, location, description, cost, complete):
        self.name = name
        self.location = location
        self.description = description
        self.cost = cost
        self.complete = complete

# Create an Activity
@app.route('/activity', methods=['POST'])
@cross_origin()
def add_activity():
    name = request.json['name']
    location = request.json['location']
    description = request.json['description']
    cost = request.json['cost']
    complete = request.json['complete']

    new_activity = Activity(name, location, description, cost, complete)

    activity_db.session.add(new_activity)
    activity_db.session.commit()

    return activity_schema.jsonify(new_activity)

# Get ALL activities
@app.route('/activities', methods=['GET'])
@cross_origin()
def get_activities():
    all_activities = Activity.query.all()
    result = activities_schema.dump(all_activities)
    return jsonify(result)


# Get A Single activitiy
@app.route('/activity/<id>', methods=['GET'])
@cross_origin()
def get_activity(id):
    activity = Activity.query.get(id)
    return activity_schema.jsonify(activity)

# Update an activity
@app.route('/activity/<id>', methods=['PUT'])
@cross_origin()
def update_activity(id):
    activity = Activity.query.get(id)

    name = request.json['name']
    location = request.json['location']
    description = request.json['description']
    cost = request.json['cost']
    complete = request.json['complete']

    activity.name = name
    activity.location = location
    activity.description = description
    activity.cost = cost
    activity.complete = complete

    activity_db.session.commit()

    return activity_schema.jsonify(activity)

# Delete an activity
@app.route('/activity/<id>', methods=['DELETE'])
@cross_origin()
def delete_activity(id):
    activity = Activity.query.get(id)
    activity_db.session.delete(activity)
    activity_db.session.commit()

    return activity_schema.jsonify(activity)


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields=('id', 'first_name', 'last_name', 'email', 'photo_url')


# Init schema
user_schema = UserSchema()

users_schema = UserSchema(many=True)

# User Model
class User(user_db.Model):
    __tablename__ = 'users'
    id = user_db.Column(user_db.Integer, primary_key=True)
    first_name = user_db.Column(user_db.String(30))
    last_name = user_db.Column(user_db.String(30))
    email = user_db.Column(user_db.String(50))
    photo_url = user_db.Column(user_db.String(200))

    def __init__(self, first_name, last_name, email, photo_url):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self. photo_url = photo_url

# Create a User
@app.route('/user', methods=['POST'])
@cross_origin()
def add_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    photo_url = request.json['photo_url']

    new_user = User(first_name, last_name, email, photo_url)

    user_db.session.add(new_user)
    user_db.session.commit()

    return user_schema.jsonify(new_user)


# Get ALL users
@app.route('/users', methods=['GET'])
@cross_origin()
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get a single user
@app.route('/user/<id>', methods=['GET'])
@cross_origin()
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# Update a User
@app.route('/user/<id>', methods=['PUT'])
@cross_origin()
def update_user(id):
    user = User.query.get(id)

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    photo_url = request.json['photo_url']

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.photo_url = photo_url

    user_db.session.commit()

    return user_schema.jsonify(user)

# Delete a User
@app.route('/user/<id>', methods=['DELETE'])
@cross_origin()
def delete_user(id):
    user = User.query.get(id)
    user_db.session.delete(user)
    user_db.session.commit()

    return user_schema.jsonify(user)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

