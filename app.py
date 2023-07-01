from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/store_name', methods=['POST'])
def store_name():
    try:
        name = request.json['name']
    except KeyError:
        return jsonify({'error': 'Invalid request. Please provide a "name" field in the request body.'}), 400

    integration_token = 'secret_MgH4QBQvYCoQ9VfBx6yJvYZTOIId7u6HydYequhp1QP'
    database_id = '5dd39b5a3dfd4242971fa05a55c9f908'
    url = 'https://api.notion.com/v1/pages'
    headers = {
        'Authorization': f'Bearer {integration_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }
    data = {
        'parent': {'database_id': database_id},
        'properties': {
            'Name': {'title': [{'text': {'content': name}}]}
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return jsonify({'message': f'Successfully created entry for "{name}" in the Notion database.'}), 200
    else:
        return jsonify({'error': f'Failed to create entry. Status code: {response.status_code}.', 'response': response.text}), 500

@app.route('/response_database', methods=['GET'])
def response_database():
    integration_token = 'secret_MgH4QBQvYCoQ9VfBx6yJvYZTOIId7u6HydYequhp1QP'
    database_id = '5dd39b5a3dfd4242971fa05a55c9f908'
    url = f'https://api.notion.com/v1/databases/{database_id}'
    headers = {
        'Authorization': f'Bearer {integration_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': f'Failed to retrieve database. Status code: {response.status_code}.', 'response': response.text}), 500

if __name__ == '__main__':
    app.run()
