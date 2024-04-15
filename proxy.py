import os
import json
import requests
from flask import Flask, request, Response, stream_with_context

app = Flask(__name__)
OPENAI_API_URL = 'https://api.openai.com'
LOG_FILE = 'logs.jsonl'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"{OPENAI_API_URL}/{path}"
    headers = {k: v for k, v in request.headers.items() if k != 'Host'}
    headers['Host'] = OPENAI_API_URL.split('//')[-1]

    data = request.get_data()
    json_data = json.loads(data.decode('utf-8')) if data else None
    is_stream = json_data.get('stream', False) if json_data else False

    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=data,
            stream=is_stream,
        )

        if request.method == 'POST':
            if is_stream:
                response_chunks = []

                def generate():
                    for chunk in response.iter_content(chunk_size=None):
                        yield chunk
                        response_chunks.append(chunk)

                complete_response = ''.join(chunk.decode('utf-8') for chunk in response_chunks)
                parsed_response = ''.join(
                    json.loads(line[6:])['choices'][0]['delta'].get('content', '')
                    for line in complete_response.split('\n')
                    if line.startswith('data: ')
                )

                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(json.dumps({
                        'request': json_data,
                        'response': parsed_response
                    }) + '\n')

                return Response(stream_with_context(generate()), content_type=response.headers['Content-Type'])
            else:
                response_data = response.json()
                complete_response = response_data['choices'][0]['message']['content']

                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(json.dumps({
                        'request': json_data,
                        'response': complete_response
                    }) + '\n')

                return response_data
        else:
            if is_stream:
                return Response(stream_with_context(response.iter_content(chunk_size=None)), content_type=response.headers['Content-Type'])
            else:
                return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error proxying request: {e}")
        return Response('Internal Server Error', status=500)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(port=port)