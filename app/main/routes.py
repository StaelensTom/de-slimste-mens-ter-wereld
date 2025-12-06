import os
import random
import glob

from flask import session, redirect, url_for, render_template, request, send_file, jsonify
from . import main

from flask import current_app
from erik.dsmtw import DeSlimsteMens

@main.route('/')
def landing():
	# Get available question directories
	question_dirs = []
	for item in os.listdir('.'):
		if os.path.isdir(item) and not item.startswith('.') and not item.startswith('_'):
			# Check if directory contains JSON files
			if glob.glob(os.path.join(item, '*.json')):
				question_dirs.append(item)
	
	return render_template('landing.html', 
						   global_questions_directory=current_app.config["questions_directory"],
						   question_dirs=question_dirs,
						   game_initialized=current_app.config.get('game') is not None)

@main.route('/host')
def host(callback=None):
	return render_template('game.html', host=True)

@main.route('/player')
def player(callback=None):
	return render_template('game.html', host=False)

@main.route('/resources/<string:filename>')
def display_label_image(filename):
	global_questions_directory = current_app.config["questions_directory"]

	if not os.path.isabs(global_questions_directory):
		path = os.path.join("..", global_questions_directory, filename)
	else:
		path = os.path.join(global_questions_directory, filename)

	return send_file(path)

@main.route('/initialize_game', methods=['POST'])
def initialize_game():
	"""Initialize the game with selected question directory and players"""
	data = request.get_json()
	questions_directory = data.get('questions_directory')
	player_names = data.get('player_names', [])
	
	if not questions_directory or not player_names:
		return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
	
	# Validate question directory exists
	if not os.path.isdir(questions_directory):
		return jsonify({'success': False, 'error': 'Invalid question directory'}), 400
	
	# Initialize the game
	try:
		current_app.config['questions_directory'] = questions_directory
		current_app.config['game'] = DeSlimsteMens(player_names, questions_directory)
		return jsonify({'success': True})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/reset_configuration', methods=['POST'])
def reset_configuration():
	"""Reset the game configuration to allow reconfiguring players and questions"""
	current_app.config['game'] = None
	current_app.config['questions_directory'] = None
	return jsonify({'success': True})