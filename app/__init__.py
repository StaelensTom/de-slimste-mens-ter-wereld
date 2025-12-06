from flask import Flask
from flask_socketio import SocketIO
from erik.dsmtw import DeSlimsteMens

socketio = SocketIO()

def create_app(questions_directory=None, player_names=None, debug=False):
	global global_questions_directory # it's bad but at least I know it's bad
	global global_player_names

	"""Create an application."""
	app = Flask(__name__)
	app.debug = debug
	app.config['SECRET_KEY'] = 'miep'
	app.config['questions_directory'] = questions_directory
	
	# Only create game if both parameters are provided
	if questions_directory and player_names:
		app.config['game'] = DeSlimsteMens(player_names, questions_directory)
	else:
		app.config['game'] = None

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint, url_prefix='')

	socketio.init_app(app)
	return app