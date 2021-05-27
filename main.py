import smtplib
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from email.message import EmailMessage
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = "super secret key"
engine = create_engine('postgresql://postgres:12341234@localhost/web')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/info')
def info(request_json=None):
    data = request_json
    if data['username']:
        temp = session.query(User).filter(User.username == data['username']).first()
        return jsonify({'surname': temp.surname, 'email': temp.email, 'username': temp.username})

@app.route('/sign_up', methods=['POST'])
def sign_up():
    try:
        data = request.json
        name = data['name']
        surname = data['surname']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        email = data['email']
        if name == '' or surname == '' or username == '' or password1 == '' or password2 == '' or email == '':
            return jsonify({'message': 'Invalid Data'})
        if password1 != password2:
            return jsonify({'message': 'Different passwords'})

        if session.query(User).filter(User.username == data['username']).first() != None:
            return jsonify({'message': 'Username Occupied'})
        temp_user = User(name=name, surname=surname, username=username, password=password1, email=email)
        session.add(temp_user)
        session.commit()
        temp_id = session.query(User).filter(User.username == data['username']).first().id
        return jsonify({'message': 'Success', 'id': temp_id})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        data = request.json
        if data['username'] == "" or data['password'] == "":
            return jsonify({'message': 'Invalid data'})
        temp = session.query(User).filter(User.username == data['username']).first()
        if temp.password == data['password']:
            return jsonify({'message': 'Success', 'id': temp.id, 'role': temp.role, 'username': temp.username,
                            'email': temp.email, 'surname': temp.surname})
    except Exception as e:
        return jsonify({'message': 'User not found'})
    return jsonify({'message': 'Enter correct name/password'})


@app.route('/video_search', methods=['POST'])
def video_search():
    try:
        vid = session.query(Video).filter().all()
        if len(vid) >= 1:
            return jsonify(video_list=[e.serialize() for e in vid])
        return jsonify({'message': 'Error'})
    except Exception as e:
        return jsonify({'message': 'Error'})

@app.route('/add_video', methods=['POST'])
def add_course():
    try:
        data = request.json
        name = data['name']
        description = data['description']
        time = data['time']
        if name == '' or description == '':
            return jsonify({'message': 'Invalid Data'})

        temp_video = Video(name=name, description=description, time=time)
        session.add(temp_video)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})

@app.route('/delete_video', methods=['POST'])
def delete_video():
    try:
        data = request.json
        name = data['name']
        temp1 = session.query(Video).filter(Video.name == name).first()
        if name == '':
            return jsonify({'message': 'Invalid Data'})
        session.delete(temp1)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})

#
# @app.route('/log_out', methods=['POST'])
# def log_out():
#     return jsonify({'message': 'Success'})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html')


@app.errorhandler(405)
def page_not_found(e):
    return render_template('login.html')


@app.route('/menu')
def menu():
    try:
        data = request.json
        if data['username']:
            temp = session.query(User).filter(User.username == data['username']).first()
            return jsonify({'message': 'Success', 'role': temp.role, 'username': temp.username})
        else:
            return jsonify({'message': 'Error !'})
    except Exception as e:
        return jsonify({'message': 'Error !'})




@app.route('/user', methods=['POST'])
def user():
    try:
        data = request.json
        check_user = session.query(User).filter(User.id == data['id']).first()
        password = data['check']
        if password == check_user.password:
            return jsonify({'message': 'Success',
                            'username': check_user.username,
                            'name': check_user.name,
                            'surname': check_user.surname,
                            'email': check_user.email})
        else:
            return jsonify({'message': 'Error !'})
    except Exception as e:
        return jsonify({'message': 'Error !'})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
