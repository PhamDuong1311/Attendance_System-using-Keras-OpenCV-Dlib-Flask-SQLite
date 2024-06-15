from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import os
from Capture_Images import takeImages

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///danhgia.db'
db = SQLAlchemy(app)


class DanhGia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    vector = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/capture')
def capture():
    takeImages('example_id', 'example_name')
    return render_template('capture.html')

@app.route('/danhgia', methods=['POST'])
def danhgia():
    data = request.get_json()

    try:
        save_to_database(data['student_id'])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_danhgia')
def get_danhgia():
    try:
        selected_date = request.args.get('date')
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
        danhgia_data = DanhGia.query.filter(DanhGia.time >= selected_date, DanhGia.time < selected_date + timedelta(days=1)).order_by(DanhGia.id.desc()).all()
        return jsonify([{'id': entry.id, 'student_id': entry.student_id, 'time': entry.time} for entry in danhgia_data])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


data_folder = 'data'
@app.route('/get_embeddings', methods=['GET'])
def get_embeddings():
    embeddings_data = {}
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)

        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r') as file:
                try:
                    embedding_data = json.load(file)
                    embeddings_data[filename] = embedding_data
                except json.JSONDecodeError as e:
                    print(f'Lỗi khi giải mã JSON trong tệp {filename}: {str(e)}')

    return jsonify(embeddings_data)

def save_to_database(student_id):
    with app.app_context():
        entry = DanhGia(student_id=student_id)
        db.session.add(entry)
        db.session.commit()

def save_embeddings_to_database(name, user_id, vector):
    with app.app_context():
        existing_entry = Data.query.filter_by(name=name, user_id=user_id).first()

        if existing_entry:
            existing_entry.vector = vector
            db.session.commit()
        else:
            entry = Data(name=name, user_id=user_id, vector=vector)
            db.session.add(entry)
            db.session.commit()


def process_data_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r') as file:
                try:
                    embedding_data = json.load(file)
                    name = embedding_data.get('name')
                    user_id = embedding_data.get('Id')
                    vector = embedding_data.get('vector')
                    save_embeddings_to_database(name, user_id, vector)
                except json.JSONDecodeError as e:
                    print(f'Lỗi khi giải mã JSON trong tệp {filename}: {str(e)}')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    process_data_folder('data')

    app.run(host='0.0.0.0', port=5000, debug=True)

