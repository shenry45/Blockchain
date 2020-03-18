import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain with the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # Create the block_string
        block_string = json.dumps(block, sort_keys=True)
        string_in_bytes = block_string.encode()

        # Hash this string using sha256
        hash_object = hashlib.sha256(string_in_bytes)
        hash_string = hash_object.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # Return the hashed block string in hexadecimal format
        return hash_string

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 6
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f'{block_string}{proof}'.encode()

        guess_hash = hashlib.sha256(guess).hexdigest()
        
        # return True or False if leading 3 zeros
        return guess_hash[:6] == '000000'

    @property
    def last_block(self):
        return self.chain[-1]

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    print(data)

    if data is None or "proof" not in data and "id" not in data:
        response = {
            'message': 'All required fields not found.'
        }

        return jsonify(response), 400

    # Run the proof of work algorithm to get the next proof
    block = blockchain.last_block

    if blockchain.valid_proof(data["id"], data["proof"]):
        # Forge the new Block by adding it to the chain with the proof
        block_hash = blockchain.hash(block)
        blockchain.new_block(data["proof"], block_hash)

        response = {
            'message': 'New Block Forged'
        }

        return jsonify(response), 200
    else:
        return jsonify({'message': 'Proof unsuccessful. Try again.'}), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'chain_length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/last-block', methods=['GET'])
def last_block():
    response = {
        'block': blockchain.last_block
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5030)
