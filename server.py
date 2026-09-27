from flask import Flask, request, jsonify
from redis import Redis
import json
import os
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'), 
    port=int(os.getenv('REDIS_PORT', 6380)), 
    decode_responses=True
)

# @app.route('/papers/chunk/<int:x>/<int:y>/<int:z>', methods=['GET'])
# def getChunk(x: int, y: int, z: int):


@app.route('/papers/user/<int:uid>', methods=['GET'])
def createdByUser(uid: int):
    try:
        papers = database.zrange('papers:v2:user:' + str(uid) + ':ids', 0, -1)
        return jsonify({'papers': papers,
                        'total': len(papers)}), 200
    except Exception as e:
        logger.error(f"Error in get_user_papers: {e}")
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )