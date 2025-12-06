# dsmtw
# by Anthe Sevenants
# started on 2022-12-03
# 100% functional on 2022-12-13
# based on the 2016 version in PHP


from flask_socketio import SocketIO
import argparse
import os

from app import create_app, socketio


#
# Arguments
#

parser = argparse.ArgumentParser(description='Play De Slimste Mens Ter Wereld')
parser.add_argument('function', type=str, nargs='?', default='listen',
					help='listen')
parser.add_argument('questions_directory', type=str, nargs='?', default=None,
					help='tafelquiz (optional, can be selected on landing page)')
parser.add_argument('player_names', type=str, nargs='?', default=None,
					help='list of the player names, separated by commas (optional, can be entered on landing page)')

args = parser.parse_args();

if args.function == "listen":
	player_names = args.player_names.split(",") if args.player_names else None

	# Use environment variable for production, default to 10965 for local dev
	port = int(os.environ.get('PORT', 10965))
	# Use environment variable to determine if in production
	is_production = os.environ.get('RENDER', False)
	debug_mode = not is_production

	app = create_app(args.questions_directory, player_names, debug=debug_mode)
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True

	# Render requires binding to 0.0.0.0
	host = '0.0.0.0' if is_production else '127.0.0.1'
	socketio.run(app, host=host, port=port, debug=debug_mode, allow_unsafe_werkzeug=True)