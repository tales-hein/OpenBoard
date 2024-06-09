from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_HOST')
database = os.getenv('DATABASE_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Route(db.Model):
    id                    = db.Column(db.Integer, primary_key=True)
    name                  = db.Column(db.String(30), nullable=False)
    author                = db.Column(db.String(20), nullable=False)
    description           = db.Column(db.String(400), nullable=False)
    grade                 = db.Column(db.String(4), nullable=False)
    route_definition      = db.Column(db.BINARY(25), nullable=False)
    route_hold_definition = db.Column(db.BINARY(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/repo')
def repo():
    routes = Route.query.all()
    return render_template('repo.html', routes=routes)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/api/v1/route/get-all', methods=['GET'])
def get_all_routes():
    all_routes = Route.query.all()
    return all_routes

@app.route('/api/v1/route/<int:id>', methods=['GET'])
def get_route(id):
    route = Route.query.get(id)
    if route:
        print(route)
    else:
        return jsonify({'message': 'Erro tentando buscar dados de rota.'}), 404

@app.route('/api/v1/route', methods=['POST'])
def create_route():
    data = {}
    return jsonify(data)

@app.route('/api/v1/route', methods=['PUT'])
def update_route():
    data = {}
    return jsonify(data)

@app.route('/api/v1/route', methods=['DELETE'])
def delete_route():
    data = {}
    return jsonify(data)

@app.route('/api/v1/route/create-selection', methods=['POST'])
def create_selection():
    data = {}
    return jsonify(data)

@app.route('/api/v1/route/retrieve-selection', methods=['GET'])
def get_selection():
    data = {}
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=3030, debug=True)
