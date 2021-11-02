from flask import Blueprint, request, make_response, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from server import read_db, write_db
from grdb.database.models import Author, User
from .utils.jwt import is_valid, assign_token, parse_token

auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    institution = data.get('institution')
    email = data.get('email')
    password = data.get('password')

    if not (first_name and last_name and email and password):
        return make_response('Missing required field.', 400)

    password_hash = generate_password_hash(password)

    db = write_db.Session()
    user = db.query(User).filter_by(email=email).first()

    if not user:
        author = Author(first_name=first_name, last_name=last_name, institution=institution)
        db.add(author)
        db.flush()

        user = User(
            email=email,
            password_hash=password_hash,
            author_id=author.id
        )
        db.add(user)
        db.commit()

        return make_response('User registered.', 201)
    else:
        return make_response('User already exists', 409)


@auth.route("/signin", methods=['post'])
def signin():
    token = request.headers.environ.get('HTTP_AUTHORIZATION')
    if token:
        if is_valid(token):
            email, _ = parse_token(token)
            token = assign_token(email)
            return jsonify({'token': token})
        else:
            return make_response('Token is expired', 400)

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not (email or password):
        return make_response("Missing required fields.", 400)

    db = read_db.Session()
    user = db.query(User).filter_by(email=email).first()
    db.close()
    token = assign_token(user.email)

    if user and check_password_hash(user.password_hash, password):
        return jsonify({'token': token})
    else:
        return make_response('Incorrect username or password', 403)
