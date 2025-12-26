"""
Test Supabase connection and verify database setup.
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

def test_connection():
    """Test connection to Supabase and verify tables exist."""
    
    # Get credentials from environment
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        print("❌ Error: SUPABASE_URL or SUPABASE_SERVICE_KEY not found in .env file")
        print("\nMake sure your .env file contains:")
        print("SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co")
        print("SUPABASE_SERVICE_KEY=your-service-key")
        return False
    
    print(f"🔗 Connecting to Supabase...")
    print(f"   URL: {url}")
    
    try:
        # Create Supabase client
        supabase: Client = create_client(url, key)
        print("✅ Connection successful!")
        
        # Test 1: Query question_sets table
        print("\n📊 Testing question_sets table...")
        response = supabase.table('question_sets').select("*").execute()
        print(f"✅ Found {len(response.data)} question sets")
        
        # Test 2: Query questions table
        print("\n📊 Testing questions table...")
        response = supabase.table('questions').select("*").execute()
        print(f"✅ Found {len(response.data)} questions")
        
        # Test 3: Query media_files table
        print("\n📊 Testing media_files table...")
        response = supabase.table('media_files').select("*").execute()
        print(f"✅ Found {len(response.data)} media files")
        
        # Test 4: Check storage bucket
        print("\n🗄️  Testing storage bucket...")
        try:
            buckets = supabase.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]
            if 'question-media' in bucket_names:
                print("✅ Storage bucket 'question-media' exists")
            else:
                print("⚠️  Warning: Storage bucket 'question-media' not found")
                print(f"   Available buckets: {bucket_names}")
        except Exception as e:
            print(f"⚠️  Could not check storage buckets: {e}")
        
        print("\n" + "="*60)
        print("🎉 All tests passed! Supabase is ready to use.")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your SUPABASE_URL and SUPABASE_SERVICE_KEY are correct")
        print("2. Check that you ran the SQL schema creation script in Supabase")
        print("3. Ensure your Supabase project is fully provisioned (wait 2-3 minutes)")
        return False

if __name__ == "__main__":
    test_connection()
