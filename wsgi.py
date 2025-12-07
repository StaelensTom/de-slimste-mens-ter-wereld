"""
WSGI entry point for production deployment with Gunicorn
"""
import os
from app import create_app, socketio

# Create the Flask app
app = create_app(
    questions_directory=None,  # Will be selected via web interface
    player_names=None,  # Will be entered via web interface
    debug=False
)

if __name__ == "__main__":
    # This is only used for local development
    # In production, Gunicorn will use the 'app' object directly
    port = int(os.environ.get('PORT', 10965))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
