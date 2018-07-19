from flask import Flask, render_template, g, redirect, flash, url_for, session, request, flash, send_file
from flask_mail import Mail, Message
import os, datetime
import login_handler, database_handler

app = Flask(__name__)

app.config.update(DEBUG=True,
                  MAIL_SERVER='smtp.gmail.com',
                  MAIL_PORT=465,
                  MAIL_USE_SSL=True,
                  MAIL_USERNAME = '<>',
                  MAIL_PASSWORD = '<>')

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        name = request.form['employee_ID']
        passw = request.form['employee_pass']
        check = login_handler.authorize_login(name, passw)
        if check == False:
            flash('Invalid Details')
            return redirect(url_for('login'))
        else:
            session['logged_in'] = True
            session['id'] = name
            session['important_details'] = login_handler.find_user(name)
            session['admin'] = False
            if 'A' in check:
                session['admin'] = True
            return redirect(url_for('employee_screen'))
    return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method=='POST':
        id = request.form['id']
        name = request.form['name']
        passw = request.form['passw']
        dept = request.form['dept']
        email = request.form['email']
        hod = request.form['hod']
        check_ = login_handler.create_user(id, name, passw, dept, email, hod)
        if check_ == False:
            flash('User Already Exists')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/employee', methods=['GET', 'POST'])
def employee_screen():
    if session['logged_in'] == True:
        if request.method == 'POST':
            id = session['important_details']['id']
            database_handler.generate(id)
            fname = '{} Employee Record.csv'.format(id)
            return send_file(fname, mimetype='text/csv', as_attachment=True, attachment_filename="Employee_Record.csv")
        return render_template('employee.html', username=session['important_details']['id'],
                                           name=session['important_details']['name'],
                                           dept=session['important_details']['department'],
                                           hod_email=session['important_details']['hod'],
                                           email=session['important_details']['email'])
    return redirect(url_for('login'))

@app.route('/leave', methods=['GET', 'POST'])
def leave_screen():
    if session['logged_in'] == True:
        if request.method=='POST':
            leave_type = request.form['LeaveType']
            leave_length = request.form['LeaveLength']
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            reason = request.form['reason']
            mail = Mail(app)
            message = "{} from {} will be on a leave from {} to {}. The reason stated as, {}".format(session['important_details']['name'],
                                                                            session['important_details']['department'], start_date, end_date,
                                                                            reason)
            subject = "Leave - {}".format(session['important_details']['name'])
            msg = Message(subject,
                          sender="<"+session['important_details']['name']+">",
                          recipients=[session['important_details']['hod']])
            msg.body = message
            mail.send(msg)
            database_handler.leave(session['important_details']['id'], start_date, end_date, leave_type, leave_length, reason)
    return render_template('leave.html')

@app.route('/fieldtrip', methods=['GET', 'POST'])
def fieldtrip_screen():
    if session['logged_in'] == True:
        if request.method=='POST':
            place = request.form['place_']
            city = request.form['city_']
            state = request.form['state_']
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            region = "{}, {}, {}".format(place, city, state)
            mail = Mail(app)
            message = "{} from {} will be on a field trip from {} to {}. The location is {}".format(session['important_details']['name'],
                                                                             session['important_details']['department'], start_date, end_date,
                                                                            region)
            subject = "Field Trip - {}".format(session['important_details']['name'])
            msg = Message(subject,
                          sender="<"+session['important_details']['name']+">",
                          recipients=[session['important_details']['hod']])
            msg.body = message
            mail.send(msg)
            database_handler.leave(session['important_details']['id'], startdate, enddate, 'Field Trip', '', region)
    return render_template('fieldtrip.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_screen():
    if session['admin'] == True:
        if request.method =='POST':
            id = request.form['generate_report_id']
            database_handler.generate(id)
            fname = '{} Employee Record.csv'.format(id)
            return send_file(fname, mimetype='text/csv', as_attachment=True, attachment_filename="Employee_Record.csv")
        return render_template('admin.html')
    else:
        flash('You are not an ADMIN')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = os.urandom(36)
    app.run(debug=True)
