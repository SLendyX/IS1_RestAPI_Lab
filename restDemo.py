from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

client = MongoClient('mongodb+srv://slendyx2002_db_user:VISLGZd4agoTGEfB@radu.h35zgvi.mongodb.net/?appName=Radu')
db = client.FacultateDB
collection = db.Studenti

app = Flask(__name__)


@app.route('/entries', methods=['GET'])
def get_all_entries():
    entries = collection.find()
    return dumps(entries), 200

@app.route('/entries', methods=['POST'])
def add_entry():
    data = request.get_json()
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# 2. A modifica o intrare existentă din baza de date (Folosim metoda PUT)
@app.route('/entries/<id>', methods=['PUT'])
def update_entry(id):
    try:
        data = request.get_json()
        
        # Folosim operatorul $set pentru a modifica doar câmpurile trimise,
        # fără a șterge celelalte câmpuri existente în document
        result = collection.update_one(
            {'_id': ObjectId(id)}, 
            {'$set': data}
        )
        
        if result.matched_count > 0:
            return jsonify({'message': 'Document modificat cu succes'}), 200
        else:
            return jsonify({'error': 'Documentul nu a fost găsit'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# 3. A șterge o intrare din baza de date (Folosim metoda DELETE)
@app.route('/entries/<id>', methods=['DELETE'])
def delete_entry(id):
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count > 0:
            return jsonify({'message': 'Document șters cu succes'}), 200
        else:
            return jsonify({'error': 'Documentul nu a fost găsit'}), 404
            
    except Exception as e:
        return jsonify({'error': 'Format de ID invalid'}), 400

if __name__ == '__main__':
    app.run(debug=True)
