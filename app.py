from flask import Flask, render_template, request, jsonify, url_for
import os
from queue_tracker import QueueTracker

app = Flask(__name__)

# Create queue tracker instance
queue_tracker = QueueTracker()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_queue', methods=['POST'])
def start_queue():
    data = request.get_json()
    queue_size = int(data.get('queue_size', 0))
    
    if queue_size <= 0:
        return jsonify({"success": False, "message": "Queue size must be greater than 0"})
    
    queue_tracker.start_queue(queue_size)
    return jsonify({"success": True, "status": queue_tracker.get_status()})

@app.route('/update_queue', methods=['POST'])
def update_queue():
    data = request.get_json()
    queue_size = int(data.get('queue_size', 0))
    
    if not queue_tracker.is_active:
        return jsonify({"success": False, "message": "No active queue"})
    
    queue_tracker.update_queue(queue_size)
    return jsonify({"success": True, "status": queue_tracker.get_status()})

@app.route('/get_status')
def get_status():
    return jsonify(queue_tracker.get_status())

# Create necessary directories and files if they don't exist
def setup_app():
    # Create templates directory
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create static directory and subdirectories
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    js_dir = os.path.join(static_dir, 'js')
    os.makedirs(js_dir, exist_ok=True)
    
    # Create index.html if it doesn't exist
    index_path = os.path.join(templates_dir, 'index.html')
    if not os.path.exists(index_path):
        with open(index_path, 'w') as f:
            # Use the HTML template from the index_template artifact
            f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Queue Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        /* CSS styles here */
    </style>
</head>
<body>
    <div class="container">
        <h1>Queue Tracker</h1>
        <!-- HTML content here -->
    </div>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
            ''')
    
    # Create main.js if it doesn't exist
    js_path = os.path.join(js_dir, 'main.js')
    if not os.path.exists(js_path):
        with open(js_path, 'w') as f:
            # Use the JavaScript from the static_js artifact
            f.write('''
// Queue Tracker Client-side JavaScript
// JavaScript content here
            ''')

if __name__ == '__main__':
    setup_app()
    # Get port from environment variable or use default 5000
    port = int(os.environ.get('PORT', 5000))
    # Get debug mode from environment variable (default to False for production)
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)