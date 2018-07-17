from flask import Flask, render_template, g, redirect, flash, url_for, session, request, flash
from flask_mail import Mail, Message
import os, datetime
import login_handler, database_handler

app = Flask(__name__)

app.config.update(DEBUG=True,
                  MAIL_SERVER='smtp.gmail.com',
                  MAIL_PORT=465,
                  MAIL_USE_SSL=True,
                  MAIL_USERNAME = 'fillit',
                  MAIL_PASSWORD = 'fillit')

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
            return redirect(url_for('employee_screen'))
    return render_template('signin.html')

@app.route('/employee')
def employee_screen():
    if session['logged_in'] == True:
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
                                                                            start_date, end_date, session['important_details']['department'],
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

@app.route('/admin', methods=['GET', 'POST'])
def admin_screen():
    if session['admin'] == True:
        if request.method =='POST':
            id = request.form['generate_report_id']
            database_handler.generate(id)
        return render_template('admin.html')
    else:
        flash('You are not an ADMIN')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = os.urandom(36)
    app.run(debug=True)
