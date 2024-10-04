# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    specific_earthquake = Earthquake.query.filter_by(id=id).first()
    if not specific_earthquake:
        return {"message":f"Earthquake {id} not found."},404
    return specific_earthquake.to_dict(),200

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_mag(magnitude):
    quakes =Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_json =[element.to_dict() for element in quakes]
    count = len(quakes_json)
    return {
        "count":count,
        "quakes": quakes_json
    },200




if __name__ == '__main__':
    app.run(port=5555, debug=True)
