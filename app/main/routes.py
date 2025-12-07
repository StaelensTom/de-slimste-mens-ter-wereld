import os
import random
import glob
import json

from flask import session, redirect, url_for, render_template, request, send_file, jsonify
from . import main

from flask import current_app
from erik.dsmtw import DeSlimsteMens
from app.github_sync import github_sync

@main.route('/')
def landing():
	# Get available question directories (exclude template) with max players
	question_dirs = []
	for item in os.listdir('.'):
		if os.path.isdir(item) and not item.startswith('.') and not item.startswith('_') and item != 'template':
			# Check if directory contains JSON files
			if glob.glob(os.path.join(item, '*.json')):
				# Calculate max players for this directory
				max_players = calculate_max_players(item)
				question_dirs.append({'name': item, 'max_players': max_players})
	
	return render_template('landing.html', 
						   global_questions_directory=current_app.config["questions_directory"],
						   question_dirs=question_dirs,
						   game_initialized=current_app.config.get('game') is not None)

def calculate_max_players(directory):
	"""Helper function to calculate max players for a directory"""
	try:
		limiting_files = ['Collectief geheugen.json', 'Galerij.json', 'Open deur.json', 'Puzzel.json']
		min_questions = float('inf')
		
		for filename in limiting_files:
			filepath = os.path.join(directory, filename)
			if os.path.isfile(filepath):
				with open(filepath, 'r', encoding='utf-8') as f:
					questions = json.load(f)
					question_count = len(questions)
					min_questions = min(min_questions, question_count)
		
		if min_questions == float('inf'):
			return 10
		else:
			return min_questions
	except:
		return 10

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
		path = os.path.abspath(os.path.join("..", global_questions_directory, filename))
	else:
		path = os.path.abspath(os.path.join(global_questions_directory, filename))

	return send_file(path)

@main.route('/resources/<string:directory>/<string:filename>')
def display_directory_image(directory, filename):
	"""Serve images from a specific question directory"""
	# Get absolute path
	abs_directory = os.path.abspath(directory)
	
	if not os.path.isdir(abs_directory):
		return "Directory not found", 404
	
	filepath = os.path.join(abs_directory, filename)
	if not os.path.isfile(filepath):
		return "File not found", 404
	
	return send_file(filepath)

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

@main.route('/get_max_players/<string:directory>')
def get_max_players(directory):
	"""Calculate maximum number of players based on question counts"""
	if not os.path.isdir(directory):
		return jsonify({'success': False, 'error': 'Directory not found'}), 404
	
	try:
		# Files that limit player count (need at least 1 question per player)
		limiting_files = ['Collectief geheugen.json', 'Galerij.json', 'Open deur.json', 'Puzzel.json']
		
		min_questions = float('inf')
		
		for filename in limiting_files:
			filepath = os.path.join(directory, filename)
			if os.path.isfile(filepath):
				with open(filepath, 'r', encoding='utf-8') as f:
					questions = json.load(f)
					question_count = len(questions)
					min_questions = min(min_questions, question_count)
		
		# If no limiting files found, default to unlimited (or reasonable max like 10)
		if min_questions == float('inf'):
			max_players = 10
		else:
			max_players = min_questions
		
		return jsonify({'success': True, 'max_players': max_players})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/manage_questions')
def manage_questions():
	"""Show question management interface"""
	# Get available question directories (exclude template)
	question_dirs = []
	for item in os.listdir('.'):
		if os.path.isdir(item) and not item.startswith('.') and not item.startswith('_') and item != 'template':
			# Check if directory contains JSON files
			if glob.glob(os.path.join(item, '*.json')):
				question_dirs.append(item)
	
	return render_template('manage_questions.html', question_dirs=question_dirs)

@main.route('/get_question_files/<string:directory>')
def get_question_files(directory):
	"""Get list of JSON files in a question directory"""
	if not os.path.isdir(directory):
		return jsonify({'success': False, 'error': 'Directory not found'}), 404
	
	files = glob.glob(os.path.join(directory, '*.json'))
	file_names = [os.path.basename(f) for f in files]
	return jsonify({'success': True, 'files': file_names})

@main.route('/get_questions/<string:directory>/<string:filename>')
def get_questions(directory, filename):
	"""Get questions from a specific JSON file"""
	filepath = os.path.join(directory, filename)
	
	if not os.path.isfile(filepath):
		return jsonify({'success': False, 'error': 'File not found'}), 404
	
	try:
		with open(filepath, 'r', encoding='utf-8') as f:
			questions = json.load(f)
		return jsonify(questions)
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/save_questions/<string:directory>/<string:filename>', methods=['POST'])
def save_questions(directory, filename):
	"""Save questions to a JSON file (local only, synced to GitHub periodically)"""
	filepath = os.path.join(directory, filename)
	
	if not os.path.isdir(directory):
		return jsonify({'success': False, 'error': 'Directory not found'}), 404
	
	try:
		data = request.get_json()
		questions_data = data.get('questions')
		
		# Write to local file with pretty formatting
		with open(filepath, 'w', encoding='utf-8') as f:
			json.dump(questions_data, f, indent=2, ensure_ascii=False)
		
		# Note: GitHub sync happens via periodic background task or manual trigger
		
		return jsonify({'success': True})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/create_question_set', methods=['POST'])
def create_question_set():
	"""Create a new question set from template"""
	import shutil
	
	data = request.get_json()
	new_name = data.get('name', '').strip()
	
	if not new_name:
		return jsonify({'success': False, 'error': 'Naam is verplicht'}), 400
	
	# Validate name (alphanumeric, hyphens, underscores only)
	if not all(c.isalnum() or c in '-_' for c in new_name):
		return jsonify({'success': False, 'error': 'Naam mag alleen letters, cijfers, - en _ bevatten'}), 400
	
	# Check if directory already exists
	if os.path.exists(new_name):
		return jsonify({'success': False, 'error': 'Deze naam bestaat al'}), 400
	
	# Check if template exists
	if not os.path.isdir('template'):
		return jsonify({'success': False, 'error': 'Template niet gevonden'}), 404
	
	try:
		# Copy template to new directory
		shutil.copytree('template', new_name)
		
		# Remove README from the copy
		readme_path = os.path.join(new_name, 'README.md')
		if os.path.exists(readme_path):
			os.remove(readme_path)
		
		# Note: GitHub sync happens via periodic background task or manual trigger
		
		return jsonify({'success': True, 'name': new_name})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/delete_question_set/<string:directory>', methods=['POST'])
def delete_question_set(directory):
	"""Delete a question set (except default and template)"""
	import shutil
	
	# Protect default and template
	if directory in ['default', 'template']:
		return jsonify({'success': False, 'error': 'Kan default of template niet verwijderen'}), 403
	
	# Check if directory exists
	if not os.path.isdir(directory):
		return jsonify({'success': False, 'error': 'Vragenset niet gevonden'}), 404
	
	try:
		# Delete local directory
		shutil.rmtree(directory)
		
		# Delete from GitHub by deleting all files
		commit_message = f"Delete question set: {directory}"
		
		# Get all files in the directory from GitHub and delete them
		if github_sync.enabled:
			try:
				contents = github_sync.repo.get_contents(directory, ref=github_sync.branch)
				for content_file in contents:
					github_sync.repo.delete_file(
						path=content_file.path,
						message=commit_message,
						sha=content_file.sha,
						branch=github_sync.branch
					)
				print(f"✅ Deleted {directory} from GitHub")
			except Exception as e:
				print(f"⚠️ Could not delete from GitHub: {e}")
		
		return jsonify({'success': True})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/sync_to_github', methods=['POST'])
def sync_to_github():
	"""Manually trigger GitHub sync with cooldown"""
	import time
	
	# Check cooldown (5 minutes = 300 seconds)
	last_sync_time = current_app.config.get('last_manual_sync', 0)
	current_time = time.time()
	cooldown_seconds = 300  # 5 minutes
	
	if current_time - last_sync_time < cooldown_seconds:
		remaining = int(cooldown_seconds - (current_time - last_sync_time))
		minutes = remaining // 60
		seconds = remaining % 60
		return jsonify({
			'success': False, 
			'error': f'Wacht nog {minutes}m {seconds}s voordat je opnieuw kunt opslaan'
		}), 429
	
	# Perform sync
	try:
		synced_count = sync_all_question_sets()
		current_app.config['last_manual_sync'] = current_time
		current_app.config['last_sync_time'] = current_time
		
		return jsonify({
			'success': True, 
			'message': f'{synced_count} vragenset(s) opgeslagen naar server',
			'synced_count': synced_count
		})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

def sync_all_question_sets():
	"""Sync all question sets to GitHub"""
	if not github_sync.enabled:
		print("⚠️ GitHub sync is disabled")
		return 0
	
	synced_count = 0
	
	# Get all question directories (exclude template)
	for item in os.listdir('.'):
		if os.path.isdir(item) and not item.startswith('.') and not item.startswith('_') and item != 'template':
			if glob.glob(os.path.join(item, '*.json')):
				try:
					commit_message = f"Auto-sync: {item}"
					if github_sync.commit_directory(item, commit_message):
						synced_count += 1
						print(f"✅ Synced {item} to GitHub")
				except Exception as e:
					print(f"⚠️ Failed to sync {item}: {e}")
	
	return synced_count

@main.route('/upload_image/<string:directory>', methods=['POST'])
def upload_image(directory):
	"""Upload an image file to a question directory"""
	if not os.path.isdir(directory):
		return jsonify({'success': False, 'error': 'Directory not found'}), 404
	
	if 'image' not in request.files:
		return jsonify({'success': False, 'error': 'No image file provided'}), 400
	
	file = request.files['image']
	if file.filename == '':
		return jsonify({'success': False, 'error': 'No file selected'}), 400
	
	# Validate file extension
	allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
	file_ext = os.path.splitext(file.filename)[1].lower()
	if file_ext not in allowed_extensions:
		return jsonify({'success': False, 'error': 'Invalid file type. Use PNG, JPG, or GIF'}), 400
	
	try:
		# Generate unique filename
		import uuid
		unique_filename = f"{uuid.uuid4().hex[:8]}{file_ext}"
		filepath = os.path.join(directory, unique_filename)
		
		# Save file
		file.save(filepath)
		
		return jsonify({'success': True, 'filename': unique_filename})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/lock_question_set/<string:directory>', methods=['POST'])
def lock_question_set(directory):
	"""Attempt to lock a question set for editing"""
	import time
	
	data = request.get_json()
	username = data.get('username', 'Anonymous')
	
	locks = current_app.config['question_set_locks']
	current_time = time.time()
	
	# Check if lock exists and is still valid
	if directory in locks:
		lock = locks[directory]
		if lock['expires'] > current_time:
			# Lock is still active
			return jsonify({
				'success': False,
				'locked': True,
				'lockedBy': lock['user'],
				'lockedAt': lock['timestamp'],
				'expiresIn': int(lock['expires'] - current_time)
			})
	
	# Create new lock (30 minutes)
	locks[directory] = {
		'user': username,
		'timestamp': current_time,
		'expires': current_time + 1800  # 30 minutes
	}
	
	return jsonify({
		'success': True,
		'locked': False,
		'lockedBy': username
	})

@main.route('/unlock_question_set/<string:directory>', methods=['POST'])
def unlock_question_set(directory):
	"""Release lock on a question set"""
	locks = current_app.config['question_set_locks']
	
	if directory in locks:
		del locks[directory]
	
	return jsonify({'success': True})

@main.route('/get_lock_status/<string:directory>', methods=['GET'])
def get_lock_status(directory):
	"""Check if a question set is locked"""
	import time
	
	locks = current_app.config['question_set_locks']
	current_time = time.time()
	
	if directory in locks:
		lock = locks[directory]
		if lock['expires'] > current_time:
			return jsonify({
				'locked': True,
				'lockedBy': lock['user'],
				'lockedAt': lock['timestamp'],
				'expiresIn': int(lock['expires'] - current_time)
			})
		else:
			# Lock expired, remove it
			del locks[directory]
	
	return jsonify({'locked': False})

@main.route('/refresh_lock/<string:directory>', methods=['POST'])
def refresh_lock(directory):
	"""Refresh lock expiration (called periodically by frontend)"""
	import time
	
	locks = current_app.config['question_set_locks']
	current_time = time.time()
	
	if directory in locks:
		lock = locks[directory]
		# Extend lock by 30 minutes
		lock['expires'] = current_time + 1800
		return jsonify({'success': True, 'expiresIn': 1800})
	
	return jsonify({'success': False, 'error': 'Lock not found'}), 404