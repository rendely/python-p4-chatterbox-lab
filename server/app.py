from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [m.to_dict() for m in Message.query.order_by(Message.created_at).all()]
        return make_response(
            jsonify(messages),
            200,
            {'Content-type': 'application/json'}
        )
    elif request.method == 'POST':
        print(request.form)
        new_message = Message(
            body = request.get_json().get('body'),
            username = request.get_json().get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(
            jsonify(new_message.to_dict()),
            200,
            {'Content-type': 'application/json'}
        )
        

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    

    if request.method == 'PATCH':
        for attr in request.get_json():
            setattr(message, attr, request.get_json().get(attr))

        db.session.commit()
        return  make_response(
            jsonify(message.to_dict()),
            200,
            {'Content-type': 'application/json'}
        )
    if request.method == 'DELETE':
        message_dict = message.to_dict()
        db.session.delete(message)
        db.session.commit()
        return  make_response(
            jsonify(message_dict),
            200,
            {'Content-type': 'application/json'}
        )



if __name__ == '__main__':
    app.run(port=5555, debug=True)
