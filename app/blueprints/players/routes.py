from flask import jsonify
from . import playersBP

@playersBP.route('/', methods=['GET'])
def indexFunction():
    return jsonify({'message': 'Under construction'})


