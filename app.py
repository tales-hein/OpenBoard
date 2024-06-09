from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os
import base64

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

    def to_dict(self):
        def binary_to_bits(binary_data):
            int_value = int.from_bytes(binary_data, byteorder='big')
            binary_string = bin(int_value)[2:]
            expected_length = len(binary_data) * 8
            binary_string = binary_string.zfill(expected_length)
            return binary_string

        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'description': self.description,
            'grade': self.grade,
            'route_definition': binary_to_bits(self.route_definition),
            'route_hold_definition': binary_to_bits(self.route_hold_definition),
        }

def get_session():
    return scoped_session(sessionmaker(bind=db.engine))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/repo')
def repo():
    routes = Route.query.all()
    return render_template('repo.html', routes=routes)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/api/v1/route/get-all', methods=['GET'])
def get_all_routes():
    session = get_session()
    try:
        routes = session.all(Route)
        routes = [route.to_dict() for route in routes]
        if routes:
            return jsonify(routes)
        else:
            return jsonify({'message': 'Erro tentando buscar dados de rota.'}), 404
    finally:
        session.remove()

@app.route('/api/v1/route/<int:id>', methods=['GET'])
def get_route(id):
    session = get_session()
    try:
        route = session.get(Route, id)
        route = route.to_dict()
        if route:
            return jsonify(route)
        else:
            return jsonify({'message': 'Erro tentando buscar dados de rota.'}), 404
    finally:
        session.remove()

@app.route('/api/v1/route', methods=['POST'])
def create_route():
    data = request.get_json()
    try:
        new_route = Route(
            name=data['name'],
            author=data['author'],
            description=data['description'],
            grade=data['grade'],
            route_definition=bytes.fromhex(data['route_definition']),
            route_hold_definition=bytes.fromhex(data['route_hold_definition'])
        )
        db.session.add(new_route)
        db.session.commit()
        return jsonify(new_route.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao salvar nova rota.'}), 404

@app.route('/api/v1/route/<int:id>', methods=['PUT'])
def update_route(id):
    data = request.get_json()
    session = get_session()
    try:
        route = session.get(Route, id)
        if route:
            route.name = data.get('name', route.name)
            route.author = data.get('author', route.author)
            route.description = data.get('description', route.description)
            route.grade = data.get('grade', route.grade)
            route.route_definition = bytes.fromhex(data['route_definition'])
            route.route_hold_definition = bytes.fromhex(data['route_hold_definition'])
            session.commit()
            return jsonify(route.to_dict())
        else:
            return jsonify({'message': 'Rota não encontrada.'}), 404
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Erro ao atualizar rota.', 'error': str(e)}), 400
    finally:
        session.remove()

@app.route('/api/v1/route/<int:id>', methods=['DELETE'])
def delete_route(id):
    session = get_session()
    try:
        route = session.get(Route, id)
        if route:
            session.delete(route)
            session.commit()
            return jsonify({'message': 'Rota deletada com sucesso.'})
        else:
            return jsonify({'message': 'Rota não encontrada.'}), 404
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Erro ao deletar rota.', 'error': str(e)}), 400
    finally:
        session.remove()

@app.route('/api/v1/route/create-selection', methods=['POST'])
def create_selection():
    data = {}
    return jsonify(data)

@app.route('/api/v1/route/retrieve-selection', methods=['GET'])
def get_selection():
    data = {}
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        app.run(port=3030, debug=True)
