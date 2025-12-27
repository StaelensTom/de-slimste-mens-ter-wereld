"""
Database service layer for Supabase operations.
Handles all database interactions for question sets, questions, and media files.
"""
import os
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
from supabase import create_client, Client
import json

# Load environment variables
load_dotenv()

class DatabaseService:
    """Service class for database operations."""
    
    def __init__(self):
        """Initialize Supabase client."""
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment")
        
        self.supabase: Client = create_client(url, key)
        self.storage_bucket = "question-media"
    
    # Question Set Operations
    
    def get_all_question_sets(self) -> List[Dict[str, Any]]:
        """Get all question sets."""
        response = self.supabase.table('question_sets').select("*").order('name').execute()
        return response.data
    
    def get_question_set_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a question set by name."""
        response = self.supabase.table('question_sets').select("*").eq('name', name).execute()
        return response.data[0] if response.data else None
    
    def create_question_set(self, name: str, is_template: bool = False) -> Dict[str, Any]:
        """Create a new question set."""
        data = {
            'name': name,
            'is_template': is_template
        }
        response = self.supabase.table('question_sets').insert(data).execute()
        return response.data[0]
    
    def delete_question_set(self, name: str) -> bool:
        """Delete a question set and all its questions (cascade)."""
        question_set = self.get_question_set_by_name(name)
        if not question_set:
            return False
        
        # Delete will cascade to questions and media_files
        self.supabase.table('question_sets').delete().eq('id', question_set['id']).execute()
        return True
    
    # Question Operations
    
    def get_questions_by_set_and_round(self, question_set_name: str, round_type: str) -> List[Dict[str, Any]]:
        """Get all questions for a specific question set and round type."""
        question_set = self.get_question_set_by_name(question_set_name)
        if not question_set:
            return []
        
        response = (self.supabase.table('questions')
                   .select("*")
                   .eq('question_set_id', question_set['id'])
                   .eq('round_type', round_type)
                   .order('position')
                   .execute())
        
        # Extract just the data field from each question
        return [q['data'] for q in response.data]
    
    def get_questions_for_round(self, question_set_name: str, round_type: str) -> List[Dict[str, Any]]:
        """Alias for get_questions_by_set_and_round for game compatibility."""
        return self.get_questions_by_set_and_round(question_set_name, round_type)
    
    def get_all_questions_for_set(self, question_set_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get all questions for a question set, organized by round type."""
        question_set = self.get_question_set_by_name(question_set_name)
        if not question_set:
            return {}
        
        response = (self.supabase.table('questions')
                   .select("*")
                   .eq('question_set_id', question_set['id'])
                   .order('round_type, position')
                   .execute())
        
        # Organize by round type
        questions_by_round = {}
        for q in response.data:
            round_type = q['round_type']
            if round_type not in questions_by_round:
                questions_by_round[round_type] = []
            questions_by_round[round_type].append(q)
        
        return questions_by_round
    
    def save_questions_for_round(self, question_set_name: str, round_type: str, questions: List[Dict[str, Any]]) -> bool:
        """Save questions for a specific round. Replaces all existing questions for that round."""
        question_set = self.get_question_set_by_name(question_set_name)
        if not question_set:
            # Create question set if it doesn't exist
            question_set = self.create_question_set(question_set_name)
        
        # Delete existing questions for this round
        (self.supabase.table('questions')
         .delete()
         .eq('question_set_id', question_set['id'])
         .eq('round_type', round_type)
         .execute())
        
        # Insert new questions
        if questions:
            questions_data = [
                {
                    'question_set_id': question_set['id'],
                    'round_type': round_type,
                    'position': idx,
                    'data': question
                }
                for idx, question in enumerate(questions)
            ]
            self.supabase.table('questions').insert(questions_data).execute()
        
        return True
    
    def delete_questions_for_round(self, question_set_name: str, round_type: str) -> bool:
        """Delete all questions for a specific round."""
        question_set = self.get_question_set_by_name(question_set_name)
        if not question_set:
            return False
        
        (self.supabase.table('questions')
         .delete()
         .eq('question_set_id', question_set['id'])
         .eq('round_type', round_type)
         .execute())
        
        return True
    
    # Storage Operations
    
    def upload_media_file(self, question_set_name: str, file_name: str, file_data: bytes, content_type: str = None) -> str:
        """Upload a media file to storage and track it in the database."""
        # Upload to storage
        file_path = f"{question_set_name}/{file_name}"
        
        options = {}
        if content_type:
            options['content-type'] = content_type
        
        self.supabase.storage.from_(self.storage_bucket).upload(
            file_path,
            file_data,
            options
        )
        
        # Get public URL
        public_url = self.supabase.storage.from_(self.storage_bucket).get_public_url(file_path)
        
        # Track in database
        question_set = self.get_question_set_by_name(question_set_name)
        if question_set:
            file_type = 'image' if content_type and content_type.startswith('image/') else 'video'
            media_data = {
                'question_set_id': question_set['id'],
                'filename': file_name,
                'file_type': file_type,
                'file_size': len(file_data),
                'url': public_url
            }
            
            # Upsert (insert or update if exists)
            self.supabase.table('media_files').upsert(media_data).execute()
        
        return public_url
    
    def get_media_files_for_set(self, question_set_name: str) -> List[Dict[str, Any]]:
        """Get all media files for a question set."""
        question_set = self.get_question_set_by_name(question_set_name)
        if not question_set:
            return []
        
        response = (self.supabase.table('media_files')
                   .select("*")
                   .eq('question_set_id', question_set['id'])
                   .execute())
        
        return response.data
    
    def delete_media_file(self, question_set_name: str, file_name: str) -> bool:
        """Delete a media file from storage and database."""
        file_path = f"{question_set_name}/{file_name}"
        
        try:
            # Delete from storage
            self.supabase.storage.from_(self.storage_bucket).remove([file_path])
            
            # Delete from database
            question_set = self.get_question_set_by_name(question_set_name)
            if question_set:
                (self.supabase.table('media_files')
                 .delete()
                 .eq('question_set_id', question_set['id'])
                 .eq('filename', file_name)
                 .execute())
            
            return True
        except Exception as e:
            print(f"Error deleting media file: {e}")
            return False
    
    # Utility Methods
    
    def health_check(self) -> bool:
        """Check if database connection is healthy."""
        try:
            self.supabase.table('question_sets').select("id").limit(1).execute()
            return True
        except Exception:
            return False


# Global instance
db_service = DatabaseService()
