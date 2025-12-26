"""
Migration script to load existing question sets from JSON files into Supabase database.
Run this once to migrate all your existing questions.
"""
import os
import json
import glob
from app.db_service import db_service

# Round type mapping from filename to database round_type
ROUND_TYPE_MAP = {
    '3-6-9.json': '3-6-9',
    'Open deur.json': 'Open deur',
    'Puzzel.json': 'Puzzel',
    'Galerij.json': 'Galerij',
    'Collectief geheugen.json': 'Collectief geheugen',
    'Finale.json': 'Finale'
}

def get_question_directories():
    """Get all question set directories (exclude system directories)."""
    excluded = {'.git', '.github', '.venv', 'app', 'erik', 'gameshow', 'scripts', 'template', '__pycache__'}
    
    directories = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.') and not item.startswith('_') and item not in excluded:
            # Check if it has JSON files
            json_files = glob.glob(os.path.join(item, '*.json'))
            if json_files:
                directories.append(item)
    
    return directories

def migrate_question_set(directory_name):
    """Migrate a single question set to the database."""
    print(f"\n{'='*60}")
    print(f"Migrating: {directory_name}")
    print(f"{'='*60}")
    
    # Check if question set already exists
    existing = db_service.get_question_set_by_name(directory_name)
    if existing:
        print(f"⚠️  Question set '{directory_name}' already exists in database")
        response = input(f"   Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print(f"   Skipped {directory_name}")
            return False
        print(f"   Overwriting...")
    else:
        # Create question set
        is_template = (directory_name == 'default')
        db_service.create_question_set(directory_name, is_template=is_template)
        print(f"✅ Created question set: {directory_name}")
    
    # Migrate each round type
    total_questions = 0
    for filename, round_type in ROUND_TYPE_MAP.items():
        filepath = os.path.join(directory_name, filename)
        
        if not os.path.exists(filepath):
            print(f"   ⏭️  Skipping {round_type} (file not found)")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            
            if not isinstance(questions, list):
                print(f"   ❌ Invalid format in {filename} (expected list)")
                continue
            
            # Save to database
            db_service.save_questions_for_round(directory_name, round_type, questions)
            total_questions += len(questions)
            print(f"   ✅ {round_type}: {len(questions)} questions")
            
        except json.JSONDecodeError as e:
            print(f"   ❌ Error parsing {filename}: {e}")
        except Exception as e:
            print(f"   ❌ Error migrating {filename}: {e}")
    
    print(f"\n📊 Total questions migrated: {total_questions}")
    return True

def migrate_all():
    """Migrate all question sets."""
    print("="*60)
    print("Question Set Migration to Supabase")
    print("="*60)
    
    # Check database connection
    print("\n🔗 Checking database connection...")
    if not db_service.health_check():
        print("❌ Cannot connect to database. Check your .env file.")
        return
    print("✅ Database connection OK")
    
    # Get all question directories
    directories = get_question_directories()
    
    if not directories:
        print("\n⚠️  No question directories found!")
        return
    
    print(f"\n📁 Found {len(directories)} question set(s):")
    for d in directories:
        print(f"   - {d}")
    
    print("\n" + "="*60)
    response = input("Proceed with migration? (y/n): ").strip().lower()
    if response != 'y':
        print("Migration cancelled.")
        return
    
    # Migrate each directory
    migrated = 0
    for directory in directories:
        if migrate_question_set(directory):
            migrated += 1
    
    print("\n" + "="*60)
    print(f"✅ Migration complete! {migrated}/{len(directories)} question sets migrated.")
    print("="*60)
    
    # Show summary
    print("\n📊 Database Summary:")
    question_sets = db_service.get_all_question_sets()
    for qs in question_sets:
        questions = db_service.get_all_questions_for_set(qs['name'])
        total = sum(len(q_list) for q_list in questions.values())
        print(f"   - {qs['name']}: {total} questions across {len(questions)} rounds")

if __name__ == "__main__":
    migrate_all()
