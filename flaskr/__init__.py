'''
export FLASK_APP=flaskr
export FLASK_ENV=development
export DB_USER=postgres
export DB_PASSWORD=password
export DB_HOST=localhost:5432
'''

from flask import Flask, jsonify, request, abort
from sqlalchemy.sql import exists
from models import *
from flask_cors import CORS
import sys
from functools import wraps
from auth import AuthError, requires_auth
from datetime import datetime, timedelta


RECORDS_PER_PAGE = 8

def paginate_records(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RECORDS_PER_PAGE
    end = start + RECORDS_PER_PAGE

    records = [record.format() for record in selection]
    current_selections = records[start:end]

    return current_selections

# https://stackoverflow.com/questions/53460391/passing-a-date-as-a-url-parameter-to-a-flask-route
def toDate(dateString):
    dt = datetime.strptime(dateString, "%Y-%m-%d").date()
    time_part = datetime.min.time()
    retval = datetime.combine(dt, time_part)
    return retval

def default_dtstart_dtend():
    dtstart = datetime.now() - timedelta(days=datetime.now().weekday())
    dtend = dtstart + timedelta(days=6)

    return dtstart, dtend

def dateToString(dt):
    year = dt.strftime("%Y")
    month = dt.strftime("%b")
    day = dt.strftime("%d")
    strDate = day + "/" + month + "/" + year

    return strDate

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response


    @app.route('/timesheets')
    def get_timesheets():
        def_dtstart, def_dtend = default_dtstart_dtend()
        dtstart = request.args.get('dtstart', def_dtstart, type=toDate) 
        dtend = request.args.get('dtend', def_dtend, type=toDate) 
        approvedonly_par = request.args.get('approvedonly', "True")
        approvedonly = False
        
        if approvedonly_par.lower() == "true":
            approvedonly = True

        if approvedonly:
            selection = Timesheet.query\
                    .filter(Timesheet.dttimeenter >= dtstart)\
                    .filter(Timesheet.dttimeenter <= dtend)\
                    .filter(~exists().where(Approval.timesheetid == Timesheet.timesheetid))\
                    .order_by(Timesheet.timesheetid).all()

        else:        
            selection = Timesheet.query\
                    .filter(Timesheet.dttimeenter >= dtstart)\
                    .filter(Timesheet.dttimeenter <= dtend)\
                    .order_by(Timesheet.timesheetid).all()

        cur = paginate_records(request, selection)

        if len(cur) == 0:
            abort(404)

        return jsonify({
                'success': True, 
                'timesheets': cur,
                'total_records': len(selection)
            })

    
    @app.route('/timesheets/<int:userid>', methods=['POST'])
    def add_timesheet_entry(userid):
        body = request.get_json()

        useradding = User.query.filter(User.userid == userid).one_or_none()
        dttimeenter = datetime.now()
        inout = body.get('inout', None)

        try:
           timetoadd = Timesheet(user=useradding, dttimeenter=dttimeenter, inout=inout)
           timetoadd.addEntry()

           selection = Timesheet.query.order_by(Timesheet.timesheetid).all()
           cur = paginate_records(request, selection)

           return jsonify({
                'success': True, 
                'timesheets': timetoadd.timesheetid,
                'total_records': len(selection),
               })

        except:
            # abort(422)
            msg = sys.exc_info()
            return jsonify({
                    'success': False, 
                    'message': str(msg),
                    'status_code': 422, 
                })


    @app.route('/approvals/<int:userid>', methods=['POST'])
    def timesheet_approval(userid):
        body = request.get_json()

        approver = User.query.filter(User.userid == userid).one_or_none()
        dttimeenter = datetime.now()
        approval = body.get('approval', None)
        timesheetid = body.get('timesheetid', None)

        try:
            timesheet = Timesheet.query\
                        .filter(Timesheet.timesheetid == timesheetid)\
                        .one_or_none()
            toapprove = Approval(timesheet=timesheet, 
                            user=approver, 
                            dttimeenter=dttimeenter,
                            approval=approval)
            toapprove.addEntry()

            selection = Approval.query.order_by(Approval.timesheetid).all()
            cur = paginate_records(request, selection)

            return jsonify({
                'success': True,
                'approvals': toapprove.timesheetid,
                })

        except:
            msg = sys.exc_info()
            return jsonify({
                'success': False, 
                'message': str(msg),
                'status_code': 422,
                })

 
    @app.route('/approvals/<int:userid>', methods=['GET'])
    def view_approvals(userid, approved=True):
        def_dtstart, def_dtend = default_dtstart_dtend()
        dtstart = request.args.get('dtstart', def_dtstart, type=toDate)
        dtend = request.args.get('dtend', def_dtend, type=toDate)

        selection = Timesheet.query\
                .join(Approval)\
                .all()

        cur = paginate_records(request, selection)
        
        
        return jsonify({
            'success': True,
            'timesheets': cur,
            })


    # 127.0.0.1:5000/reports/24?dtstart=2021-1-1&dtend=2021-1-20
    @app.route('/reports/<int:userid>', methods=['GET'])
    def get_summarized_report(userid):
        def_dtstart, def_dtend = default_dtstart_dtend()
        
        dtstart = request.args.get('dtstart', def_dtstart, type=toDate)
        dtend = request.args.get('dtend', def_dtend, type=toDate)
        dtstart_str = dateToString(dtstart)
        dtend_str = dateToString(dtend)
        
        fn_name = 'get_summary_rate'        
        data = DBUtil.call_db_function(fn_name, dtstart_str, dtend_str, userid)
        print("Result: {}".format(data))
        
        ret = DBUtil.fmt_data_from_fn(fn_name, data)

        return jsonify({
                'success': True,
                'data': ret
            })






    #####################
    #                   #
    #   ERROR Handling  #
    #                   #
    #####################
    

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
