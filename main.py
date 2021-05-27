import smtplib
from flask import Flask, render_template, request, jsonify, session as ss
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'super secret key'
engine = create_engine('postgresql://postgres:12341234@localhost/web')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "" or request.form['password'] == "":
            return jsonify({'message': 'Invalid data'})
        try:
            temp = session.query(User).filter(User.username == request.form['username']).first()
            if temp.password == request.form['password']:
                ss['username'] = request.form['username']
                ss['password'] = request.form['password']
                ss['id'] = temp.id
                return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'User not found'})
        return jsonify({'message': 'Enter correct name/password'})
    return render_template('login.html')

@app.route('/log_out',methods=['POST'])
def log_out():
    ss['username'] = None
    ss['password'] = None
    ss['id'] = None
    return jsonify({'message': 'Success'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html')

@app.errorhandler(405)
def page_not_found(e):
    return render_template('login.html')

@app.route('/menu')
def menu():
    if ss['username']:
        temp = session.query(User).filter(User.username == ss['username']).first()
        return render_template('menu.html', role=temp.role, username=temp.username)
    else:
        return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        try:
            name = request.form['name']
            surname = request.form['surname']
            username = request.form['username']
            password1 = request.form['password1']
            password2 = request.form['password2']
            email = request.form['email']
            if name == '' or surname == '' or username == '' or password1 == '' or password2 == '' or email == '':
                return jsonify({'message': 'Invalid Data'})
            if password1 != password2:
                return jsonify({'message': 'Different passwords'})
            temp_user = User(name=name, surname=surname, username=username, password=password1, email=email)
            session.add(temp_user)
            ss['id'] = session.query(User).filter(User.username == request.form['username']).first().id
            session.commit()
            return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'Error'})
    return render_template('sign_up.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/info')
def info():
    if ss['username']:
        temp = session.query(User).filter(User.username == ss['username']).first()
        return render_template('info.html', username=temp.username, email=temp.email, surname=temp.surname)
    else:
        return render_template('info.html')

@app.route('/user', methods=['POST'])
def user():
    check_user = session.query(User).filter(User.username == ss['username']).first()
    password = request.form['check']
    if password == check_user.password:
        return jsonify({'message': 'Success',
                        'username': ss['username'],
                        'name': check_user.name,
                        'surname': check_user.surname,
                        'email': check_user.email})
    else:
        return jsonify({'message': 'Error !'})

@app.route('/delete_account', methods=['POST'])
def delete_account():
    try:
        user_ = session.query(User).filter(User.id == ss['id']).first()
        events = session.query(Event).filter(Event.owner_id == ss['id']).all()
        for event in events:
            session.delete(event)
        session.delete(user_)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
