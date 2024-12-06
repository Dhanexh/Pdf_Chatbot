from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db


def register_routes(app):
    # Register User
    @app.route('/register', methods=['POST'])
    def register_user():
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'User already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], password=hashed_password)


        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    # Login User 
    @app.route('/login', methods=['POST'])
    def login_user():
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400

        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        session['user_id'] = user.id
        print(user.id)

        return jsonify({
            'message': 'Login successful',
            'user': {
                'username': user.username,
                'userId': user.id
            }
            
        }), 200
    