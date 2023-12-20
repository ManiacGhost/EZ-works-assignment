
from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta
import smtplib
import os
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'apple'  # Change the secret key
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///secure_file_sharing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    is_opers = db.Column(db.Boolean, default=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)

def generate_token(user_id, is_opers):
    payload = {
        'user_id': user_id,
        'is_opers': is_opers,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/ops-user/login', methods=['POST'])
def opers_login():
    username = request.headers.get('username')
    password = request.headers.get('password')

    user = User.query.filter_by(username=username, password=password, is_opers=True).first()

    if user:
        token = generate_token(user.id, True)
        return jsonify({"message": "Login Successful", 'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/ops-user/upload-file', methods=['POST'])
def opers_upload_file():
    opers_token = request.headers.get('Authorization')
    print(opers_token)
    try:
        opers_data = jwt.decode(opers_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(opers_data)
        if opers_data['is_opers']:
            file = request.files['file']

            allowed_extensions = ['pptx', 'docx', 'xlsx']
            if file and '.' in file.filename and file.filename.split('.')[-1].lower() in allowed_extensions:
                file.save(os.path.join('uploads', file.filename))

                new_file = File(filename=file.filename, filepath=os.path.join('uploads', file.filename),
                                uploaded_by=opers_data['user_id'])
                db.session.add(new_file)
                db.session.commit()

                return jsonify({'message': 'File uploaded successfully'})
            else:
                return jsonify({'message': 'Invalid File type. Allowed file types: pptx, doc, xlsx'})
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid Token'}), 401

@app.route('/client-user/signup', methods=['POST'])
def client_user_signup():
    username = request.headers.get('username')
    password = request.headers.get('password')
    email = request.headers.get('email')

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    token = generate_token(new_user.id, False)
    api_url = 'http://127.0.0.1:5000'
    verification_url = f'{api_url}/verify-email/{token}'

    my_email = "your-email@gmail.com"
    password_ = "your-password"

    connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    connection.login(user=my_email, password=password_)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=email,
        msg=f"Subject: Verification email\n\nClick the link to verify your email: {verification_url}")
    connection.close()

    return jsonify({'message': 'Check your email for verification'})

# Other routes remain unchanged...

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)



