'''
export FLASK_APP=flaskr
export FLASK_ENV=development

'''

from flask import Flask, jsonify, request, abort
from models import *
from flask_cors import CORS
import sys

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    @app.route('/users')
    def get_users():
        users = User.query.all()
        formatted_users = [user.format() for user in users]
        return jsonify({
                'success': True,
                'total_users': len(User.query.all()),
            })


    @app.route('/users', methods=["POST"])
    def create_user():
        data = request.get_json()
        username = data.get("username", None)
        firstname = data.get("firstname", None)
        lastname = data.get("lastname", None)
        
        try:
            user = User(
                username = username, 
                firstname = firstname,
                lastname = lastname
                    )
            user.insert()    
        
            return jsonify({
                'success': True,
                "userid": user.userid,
            })
        except:
            msg = sys.exc_info()
            print(sys.exc_info())
            return jsonify({
                    'success': False,
                    'message': str(msg), 
                })
            

    return app
