from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/twitter/<user_name>', methods=['GET'])
def get_twitter_data(user_name):
    # 模拟返回推特数据
    mock_data = {
        "id": int(datetime.now().timestamp()),
        "user_name": user_name,
        "content": f"Hello from {user_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    return jsonify(mock_data)

if __name__ == "__main__":
    app.run(port=5000)
