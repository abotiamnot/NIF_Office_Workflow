from flask import Flask, render_template, g, redirect, flash, url_for, session, request, flash
from flask_mail import Mail, Message
import os
import login_handler

app = Flask(__name__)

app.config.update(DEBUG=True,
                  MAIL_SERVER='smtp.gmail.com',
                  MAIL_PORT=465,
                  MAIL_USE_SSL=True,
                  MAIL_USERNAME = 'FILLITTTT',
                  MAIL_PASSWORD = 'FILLITTTT')

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
            message = "{} from {} will be on a leave from {} to {}.".format(session['important_details']['name'],
                                                                            start_date, end_date, session['important_details']['department'])
            subject = "Leave - {}".format(session['important_details']['name'])
            msg = Message(subject,
                          sender="<"+session['important_details']['name']+">",
                          recipients=[session['important_details']['hod']])
            msg.body = message
            mail.send(msg)
    return render_template('leave.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(36)
    app.run(debug=True)
