from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
# to find db.sqlite file in the current folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
# not to have the warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)

# Activity Schema
class ActivitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'description', 'cost', 'complete')

# Init schema
activity_schema = ActivitySchema()

activities_schema = ActivitySchema(many=True)

# Product Class/Model
class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    location = db.Column(db.String(300))
    description = db.Column(db.String(200))
    cost = db.Column(db.Float)
    complete = db.Column(db.Boolean)

    def __init__(self, name, location, description, cost, complete):
        self.name = name
        self.location = location
        self.description = description
        self.cost = cost
        self.complete = complete

# Create an Activity
@app.route('/activity', methods=['POST'])
def add_activity():
    name = request.json['name']
    location = request.json['location']
    description = request.json['description']
    cost = request.json['cost']
    complete = request.json['complete']

    new_activity = Activity(name, location, description, cost, complete)

    db.session.add(new_activity)
    db.session.commit()

    return activity_schema.jsonify(new_activity)

# Get ALL activities
@app.route('/activity', methods=['GET'])
def get_activities():
    all_activities = Activity.query.all()
    result = activities_schema.dump(all_activities)
    return jsonify(result)

# Get A Single activitiy
@app.route('/activity/<id>', methods=['GET'])
def get_activity(id):
    activity = Activity.query.get(id)
    return activity_schema.jsonify(activity)

# Update an activity
@app.route('/activity/<id>', methods=['PUT'])
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

    db.session.commit()

    return activity_schema.jsonify(activity)

# Delete an activity
@app.route('/activity/<id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    db.session.delete(activity)
    db.session.commit()
    return activity_schema.jsonify(activity)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

