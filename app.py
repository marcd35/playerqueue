from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
import os
from queue_tracker import QueueTracker

# Create a Flask app with custom template folder configuration
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), ''),
           static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

# Create queue tracker instance
queue_tracker = QueueTracker()

# Routes
@app.route('/')
def index():
    # Redirect to queue.html
    return send_from_directory('.', 'queue.html')

@app.route('/queue.html')
def queue_page():
    # Serve queue.html directly
    return send_from_directory('.', 'queue.html')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)