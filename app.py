from flask import Flask, render_template, jsonify, request
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('API_KEY')
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
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'description': self.description,
            'grade': self.grade,
            'route_definition': decimal_to_binary(self.route_definition),
            'route_hold_definition': decimal_to_binary(self.route_hold_definition),
        }
    
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key or api_key != api_key:
            return jsonify({"message": "Acesso restrito: request com API key errada ou faltando."}), 403
        return f(*args, **kwargs)
    return decorated_function

def get_session():
    return scoped_session(sessionmaker(bind=db.engine))

def decimal_to_binary(n):
    return bin(n).replace("0b", "")

def bit_to_byte_array(binary_string):
    byte_array = bytearray()
    for bit_position in range(0, len(binary_string), 8):
        byte = int(binary_string[bit_position:bit_position+8], 2)
        byte_array.append(byte)
    return bytes(byte_array)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/footer', methods=['GET'])
def footer():
    return render_template('footer.html')

@app.route('/repo', methods=['GET'])
def repo():
    routes = Route.query.all()
    return render_template('repo.html', routes=routes)

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')

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
    name = request.form.get('name')
    author = request.form.get('author') if request.form.get('author') else "Anônimo"
    description = request.form.get('description')
    grade = request.form.get('grade')
    holds = request.form.get('holds').split(',')

    decimal_base_route_definition = (1 << 200) - 1
    for hold in holds:
        decimal_base_route_definition &= ~(1 << int(hold))
    try:
        new_route = Route(
            name=name,
            author=author,
            description=description,
            grade=grade,
            route_definition=bit_to_byte_array(decimal_to_binary(decimal_base_route_definition)),
            route_hold_definition=bytes(0),
        )
        db.session.add(new_route)
        db.session.commit()
        return success()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao salvar nova rota.', 'error': str(e)}), 404

@app.route('/api/v1/route/<int:id>', methods=['PUT'])
@require_api_key
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
@require_api_key
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
@require_api_key
def get_selection():
    data = {}
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        app.run(port=3030, debug=True)
