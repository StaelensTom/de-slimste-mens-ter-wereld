"""
Updated routes that use Supabase database instead of file system.
This file contains the new database-backed implementations.
"""
import os
from flask import jsonify, request, current_app
from app.db_service import db_service

def get_all_question_sets_db():
    """Get all question sets from database."""
    try:
        question_sets = db_service.get_all_question_sets()
        
        # Calculate max players for each set
        result = []
        for qs in question_sets:
            max_players = calculate_max_players_db(qs['name'])
            result.append({
                'name': qs['name'],
                'max_players': max_players,
                'created_at': qs.get('created_at'),
                'is_template': qs.get('is_template', False)
            })
        
        return result
    except Exception as e:
        print(f"Error getting question sets: {e}")
        return []

def calculate_max_players_db(question_set_name):
    """Calculate max players for a question set from database."""
    try:
        limiting_rounds = ['Collectief geheugen', 'Galerij', 'Open deur', 'Puzzel']
        min_questions = float('inf')
        
        for round_type in limiting_rounds:
            questions = db_service.get_questions_by_set_and_round(question_set_name, round_type)
            if questions:
                min_questions = min(min_questions, len(questions))
        
        return min_questions if min_questions != float('inf') else 10
    except Exception as e:
        print(f"Error calculating max players: {e}")
        return 10

def get_question_files_db(question_set_name):
    """Get list of round types (files) for a question set."""
    try:
        questions = db_service.get_all_questions_for_set(question_set_name)
        
        # Map round types to filenames
        round_to_file = {
            '3-6-9': '3-6-9.json',
            'Open deur': 'Open deur.json',
            'Puzzel': 'Puzzel.json',
            'Galerij': 'Galerij.json',
            'Collectief geheugen': 'Collectief geheugen.json',
            'Finale': 'Finale.json'
        }
        
        files = [round_to_file[round_type] for round_type in questions.keys() if round_type in round_to_file]
        
        # Ensure all standard files are present (even if empty)
        standard_files = list(round_to_file.values())
        for file in standard_files:
            if file not in files:
                files.append(file)
        
        return {'success': True, 'files': sorted(files)}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_questions_db(question_set_name, filename):
    """Get questions for a specific round from database."""
    try:
        # Map filename to round type
        file_to_round = {
            '3-6-9.json': '3-6-9',
            'Open deur.json': 'Open deur',
            'Puzzel.json': 'Puzzel',
            'Galerij.json': 'Galerij',
            'Collectief geheugen.json': 'Collectief geheugen',
            'Finale.json': 'Finale'
        }
        
        round_type = file_to_round.get(filename)
        if not round_type:
            return None
        
        questions = db_service.get_questions_by_set_and_round(question_set_name, round_type)
        return questions
    except Exception as e:
        print(f"Error getting questions: {e}")
        return None

def save_questions_db(question_set_name, filename, questions_data):
    """Save questions to database."""
    try:
        # Map filename to round type
        file_to_round = {
            '3-6-9.json': '3-6-9',
            'Open deur.json': 'Open deur',
            'Puzzel.json': 'Puzzel',
            'Galerij.json': 'Galerij',
            'Collectief geheugen.json': 'Collectief geheugen',
            'Finale.json': 'Finale'
        }
        
        round_type = file_to_round.get(filename)
        if not round_type:
            return {'success': False, 'error': 'Invalid round type'}
        
        success = db_service.save_questions_for_round(question_set_name, round_type, questions_data)
        return {'success': success}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def create_question_set_db(name):
    """Create a new question set in database."""
    try:
        # Validate name
        if not name or not name.strip():
            return {'success': False, 'error': 'Name is required'}
        
        name = name.strip()
        
        if not all(c.isalnum() or c in '-_' for c in name):
            return {'success': False, 'error': 'Name can only contain letters, numbers, - and _'}
        
        # Check if already exists
        existing = db_service.get_question_set_by_name(name)
        if existing:
            return {'success': False, 'error': 'Question set already exists'}
        
        # Create question set
        question_set = db_service.create_question_set(name, is_template=False)
        
        # Copy questions from template
        template_questions = db_service.get_all_questions_for_set('default')
        for round_type, questions in template_questions.items():
            question_data = [q['data'] for q in questions]
            db_service.save_questions_for_round(name, round_type, question_data)
        
        return {'success': True, 'name': name}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def delete_question_set_db(name):
    """Delete a question set from database."""
    try:
        # Prevent deletion of protected sets
        if name in ['default', 'template']:
            return {'success': False, 'error': 'Cannot delete protected question set'}
        
        success = db_service.delete_question_set(name)
        return {'success': success}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def upload_image_db(question_set_name, file):
    """Upload an image to Supabase storage."""
    try:
        if not file:
            return {'success': False, 'error': 'No file provided'}
        
        # Read file data
        file_data = file.read()
        filename = file.filename
        content_type = file.content_type
        
        # Upload to storage
        public_url = db_service.upload_media_file(question_set_name, filename, file_data, content_type)
        
        return {'success': True, 'filename': filename, 'url': public_url}
    except Exception as e:
        return {'success': False, 'error': str(e)}
