import pandas as pd
import csv

def create_user(id, name, passw, dept, email, hod):
    login_data = pd.read_csv('login.csv')
    length_ = len(login_data['id'])
    for x in range(0, length_):
        if login_data['id'][x] == id:
            return False
    employee_data = pd.read_csv('employee_data.csv')
    length_ = len(employee_data['id'])
    for x in range(0, length_):
        if employee_data['id'][x] == id:
            return False
    with open('login.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows([[id, passw]])
    with open('employee_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows([[id, name, dept, hod, email]])

def authorize_login(name, passw):
    load_data = pd.read_csv('login.csv')
    load_data = load_data.applymap(str)
    length_ = len(load_data['id'])
    for x in range(0, length_):
        if(load_data['id'][x] == name):
            if(load_data['passw'][x] == passw):
                if(load_data['admin'][x] == '1'):
                    return '1A'
                else:
                    return '1'
    return False

def find_user(name):
    load_data = pd.read_csv('Employee_Data.csv')
    load_data = load_data.applymap(str)
    length_ = len(load_data['id'])
    for x in range(0, length_):
        if(load_data['id'][x] == name):
            full_name = load_data['name'][x]
            department = load_data['department'][x]
            hod = load_data['hod'][x]
            email = load_data['email'][x]
            employee_dict = {'id': name,
                             'name': full_name,
                             'department': department,
                             'hod': hod,
                             'email': email}
            return employee_dict
