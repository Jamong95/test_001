from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/allowed-date')
def allowed_date():
    allowed_date_str = "2023-04-12"  # Replace with your desired date

    response = {
        "allowed_date": allowed_date_str
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
