from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///danhgia.db'
db = SQLAlchemy(app)

class DanhGia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

class AdditionalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/danhgia', methods=['POST'])
def danhgia():
    data = request.get_json()

    try:
        save_to_danhgia(data['student_id'])
        filename_to_download = save_to_additional_data(data['filename'], data['content'])
        return jsonify({'status': 'success', 'filename': filename_to_download})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_danhgia')
def get_danhgia():
    danhgia_data = DanhGia.query.order_by(DanhGia.id.desc()).all()
    return jsonify([{'id': entry.id, 'student_id': entry.student_id, 'time': entry.time} for entry in danhgia_data])

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

def save_to_danhgia(student_id):
    with app.app_context():
        # Lưu vào bảng DanhGia
        entry_danhgia = DanhGia(student_id=student_id)
        db.session.add(entry_danhgia)
        db.session.commit()

def save_to_additional_data(filename, content):
    with app.app_context():
        # Lưu vào bảng AdditionalData
        entry_additional = AdditionalData(filename=filename, content=content)
        db.session.add(entry_additional)
        db.session.commit()
    return filename

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
