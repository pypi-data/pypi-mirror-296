import os
import json
import base64
import boto3
import argparse
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['CHAT_HISTORY_FILE'] = 'chat_history.json'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_chat_history():
    if os.path.exists(app.config['CHAT_HISTORY_FILE']):
        with open(app.config['CHAT_HISTORY_FILE'], 'r') as f:
            return json.load(f)
    return {}

def save_chat_history(chat_history):
    with open(app.config['CHAT_HISTORY_FILE'], 'w') as f:
        json.dump(chat_history, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    image_file = request.files.get('image')
    aws_region = request.form['aws_region']
    profile_name = request.form['profile_name']
    model_id = request.form['model_id']
    chat_id = request.form['chat_id']
    
    chat_history = load_chat_history()
    if chat_id not in chat_history:
        chat_history[chat_id] = []

    try:
        # Set up Bedrock client with the provided AWS region and profile name
        dev_session = boto3.Session(profile_name=profile_name)
        bedrock = dev_session.client(
            service_name='bedrock-runtime',
            region_name=aws_region
        )

        # Prepare the user message content
        user_content = [{"type": "text", "text": message}]

        # If an image is uploaded, add it to the user message content
        if image_file and allowed_file(image_file.filename):
            image_content = base64.b64encode(image_file.read()).decode('utf-8')
            user_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_file.content_type,
                    "data": image_content
                }
            })

        # Prepare the messages list with a single user message
        messages = [{"role": "user", "content": user_content}]

        # Prepare the request body for the selected model
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages
        })

        print(f"Sending request to Bedrock with body: {body}")

        # Use the Messages API to get a response from Bedrock
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=body
        )

        print(f"Received response from Bedrock: {response}")

        # Process the response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        ai_response = response_body['content'][0]['text']

        print(f"Final AI response: {ai_response}")

        if not ai_response:
            ai_response = "I apologize, but I couldn't generate a response. Please try again."
        else:
            # Wrap the response in markdown code blocks if it contains code
            if '```' in ai_response:
                ai_response = f"```markdown\n{ai_response}\n```"

        # Save the conversation to chat history
        chat_history[chat_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        chat_history[chat_id].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        save_chat_history(chat_history)

    except ClientError as e:
        print(f"AWS ClientError: {str(e)}")
        ai_response = f"I'm sorry, but I encountered an error while connecting to the language model: {str(e)}"
    except Exception as e:
        print(f"Error: {str(e)}")
        ai_response = f"I'm sorry, but I encountered an unexpected error while processing your request: {str(e)}"

    return jsonify({'response': ai_response})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': f'File {filename} uploaded successfully'})
    return jsonify({'error': 'File type not allowed'})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    chat_history = load_chat_history()
    return jsonify(chat_history)

@app.route('/clear_all_chats', methods=['POST'])
def clear_all_chats():
    save_chat_history({})
    return jsonify({'success': 'All chats cleared'})

@app.route('/delete_chat', methods=['POST'])
def delete_chat():
    chat_id = request.form['chat_id']
    chat_history = load_chat_history()
    if chat_id in chat_history:
        del chat_history[chat_id]
        save_chat_history(chat_history)
        return jsonify({'success': f'Chat {chat_id} deleted'})
    return jsonify({'error': 'Chat not found'})

def main():
    parser = argparse.ArgumentParser(description='Run the Chat App')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app on (default: 5000)')
    args = parser.parse_args()
    
    port = args.port
    print(f"Starting the Chat App on port {port}")
    app.run(port=port)

if __name__ == '__main__':
    main()