from flask import Flask
from flask_socketio import SocketIO
from erik.dsmtw import DeSlimsteMens
import threading
import time

socketio = SocketIO()

def auto_sync_task(app):
	"""Background task to auto-sync question sets every 30 minutes"""
	with app.app_context():
		while True:
			time.sleep(1800)  # 30 minutes
			try:
				from app.main.routes import sync_all_question_sets
				synced_count = sync_all_question_sets()
				if synced_count > 0:
					print(f"🔄 Auto-sync: {synced_count} question set(s) synced to GitHub")
				app.config['last_sync_time'] = time.time()
			except Exception as e:
				print(f"⚠️ Auto-sync failed: {e}")

def create_app(questions_directory=None, player_names=None, debug=False):
	global global_questions_directory # it's bad but at least I know it's bad
	global global_player_names

	"""Create an application."""
	app = Flask(__name__)
	app.debug = debug
	app.config['SECRET_KEY'] = 'miep'
	app.config['questions_directory'] = questions_directory
	app.config['last_manual_sync'] = 0
	app.config['last_sync_time'] = 0
	app.config['question_set_locks'] = {}  # Store active locks: {directory: {user, timestamp, expires}}
	
	# Only create game if both parameters are provided
	if questions_directory and player_names:
		app.config['game'] = DeSlimsteMens(player_names, questions_directory)
	else:
		app.config['game'] = None

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint, url_prefix='')

	socketio.init_app(app)
	
	# Start background auto-sync task
	sync_thread = threading.Thread(target=auto_sync_task, args=(app,), daemon=True)
	sync_thread.start()
	
	return app