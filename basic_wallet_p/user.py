import uuid
from flask import Flask, jsonify, request

class User():
    def __init__(self, balance=0):
        self.id = uuid.uuid4().hex
        self.balance = balance

    def __str__(self):
        return f"Your account id: {self.id}"  

    def update_user(self, id):
        self.id = id

        return self.id == id

    def current_balance(self, id):
        if self.id != id:
            return "Invalid ID"

        return self.balance

    def get_transactions(self):
        # call blockchain URL
        # store chain in List
        # iterate through List for user transactions
        # return transactions
        pass
        
# init app
app = Flask(__name__)
# init user
user = User()
print(user)

@app.route('/update', methods=["POST"])
def update():
    data = request.get_json()

    if "id" not in data:
        reponse = {
            "message": "All required fiels not found."
        }
        return jsonify(response), 400

    updated = user.update_user(id=data["id"])

    response = {
        "message": f"Your update result is {update}"
    } 
    return jsonify(response), 200 


@app.route('/balance', methods=["GET"])
def balance():
    data = request.get_json()

    if data is None or "id" not in data:
        response = {
            "message": "All required fiels not found."
        }
        return jsonify(response), 400

    balance = user.current_balance(data["id"])
    
    response = {
        "balance": balance
    }

    return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5020)
