'''
export FLASK_APP=flaskr
export FLASK_ENV=development
export DB_USER=postgres
export DB_PASSWORD=password
export DB_HOST=localhost:5432
'''

from flask import Flask, jsonify, request, abort
from models import *
from flask_cors import CORS
import sys
from functools import wraps
from auth import AuthError, requires_auth

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
            

    @app.route('/userrole', methods=["POST"])
    def add_user_role():
        data = request.get_json()
        userid = data.get("userid", None)
        roleid = data.get("roleid", None)

        try:
            usertoadd = db.session.query(User).filter(User.userid == userid).one_or_none()
            roletoadd = db.session.query(Role).filter(Role.roleid == roleid).one_or_none()
            userrole = UserRole(
                        user = usertoadd,
                        role = roletoadd,
                        valid = True
                    )             
            userrole.addUserRole()

            return jsonify({
                    'success':True,
                    'userid': userrole.userid,
                    'roleid': userrole.roleid,
                })
        except:
            msg = sys.exc_info()
            print(sys.exc_info())
            return jsonify({
                    'success': False,
                    'message': str(msg), 
                })



    @app.route('/admin_reports')
    @requires_auth('getauth')
    def view_admin_report(payload):
        # do stuff that 
        return jsonify({
                'success': True, 
                'header': payload,
            })


    #######################################################################
    #
    # ERROR Handling
    #
    #######################################################################
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable",
            }), 422
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found",
            }), 404
 
    @app.errorhandler(405)
    def not_supported(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not supported",
            }), 404
    
    @app.errorhandler(AuthError)
    def auth_error(AuthError):
        return jsonify({
            "success": False, 
            "error code": AuthError.status_code,
            "description": AuthError.error,
            }), AuthError.status_code
    
   

    return app



