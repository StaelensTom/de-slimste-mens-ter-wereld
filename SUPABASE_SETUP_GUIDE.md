# Supabase Setup Guide

## Step 1: Create Supabase Project

1. **Log in to Supabase**
   - Go to https://supabase.com
   - Sign in with your existing account

2. **Create New Project**
   - Click **"New Project"** button
   - Fill in the details:
     - **Name:** `de-slimste-mens-ter-wereld` (or your preference)
     - **Database Password:** Choose a strong password (save this!)
     - **Region:** `Europe (Frankfurt)` or closest to Belgium
     - **Pricing Plan:** Free tier (500MB storage, 500MB bandwidth)
   - Click **"Create new project"**
   - Wait 2-3 minutes for provisioning

## Step 2: Get Connection Details

1. **Navigate to Project Settings**
   - Click the **Settings** icon (⚙️) in the left sidebar
   - Click **"API"** in the settings menu

2. **Copy These Values** (you'll need them later):
   
   **Project URL:**
   ```
   https://xxxxxxxxxxxxx.supabase.co
   ```
   
   **API Keys:**
   - **anon/public key:** `eyJhbGc...` (for client-side, read operations)
   - **service_role key:** `eyJhbGc...` (for server-side, admin operations)
   
   ⚠️ **IMPORTANT:** Keep the `service_role` key secret! Never commit it to Git.

3. **Get Database Connection String** (optional, for direct PostgreSQL access)
   - Click **"Database"** in settings menu
   - Copy the **Connection string** under "Connection pooling"
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`

## Step 3: Create Database Schema

1. **Open SQL Editor**
   - Click **"SQL Editor"** in the left sidebar
   - Click **"New query"**

2. **Run Schema Creation Script**
   - Copy and paste the following SQL:

```sql
-- Create question_sets table
CREATE TABLE question_sets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_template BOOLEAN DEFAULT FALSE
);

-- Create questions table
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_set_id UUID REFERENCES question_sets(id) ON DELETE CASCADE,
    round_type VARCHAR(50) NOT NULL,
    position INTEGER NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(question_set_id, round_type, position)
);

-- Create indexes for performance
CREATE INDEX idx_questions_set_round ON questions(question_set_id, round_type);
CREATE INDEX idx_questions_data ON questions USING GIN(data);
CREATE INDEX idx_questions_position ON questions(position);

-- Create media_files table
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_set_id UUID REFERENCES question_sets(id) ON DELETE CASCADE,
    filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(question_set_id, filename)
);

-- Create index for media files
CREATE INDEX idx_media_files_set ON media_files(question_set_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers to auto-update updated_at
CREATE TRIGGER update_question_sets_updated_at BEFORE UPDATE ON question_sets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON questions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) - optional for now
ALTER TABLE question_sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE media_files ENABLE ROW LEVEL SECURITY;

-- Create policies to allow service_role full access
CREATE POLICY "Enable all access for service role" ON question_sets
    FOR ALL USING (true);

CREATE POLICY "Enable all access for service role" ON questions
    FOR ALL USING (true);

CREATE POLICY "Enable all access for service role" ON media_files
    FOR ALL USING (true);
```

3. **Execute the Script**
   - Click **"Run"** button (or press `Ctrl+Enter`)
   - Verify success message appears
   - Check that tables are created

4. **Verify Tables Created**
   - Click **"Table Editor"** in the left sidebar
   - You should see: `question_sets`, `questions`, `media_files`

## Step 4: Configure Storage (for media files)

1. **Create Storage Bucket**
   - Click **"Storage"** in the left sidebar
   - Click **"New bucket"**
   - **Name:** `question-media`
   - **Public bucket:** ✅ Yes (so images/videos are accessible)
   - Click **"Create bucket"**

2. **Set Bucket Policies**
   - Click on the `question-media` bucket
   - Click **"Policies"** tab
   - Click **"New policy"**
   - Select **"Allow public read access"**
   - Click **"Review"** → **"Save policy"**

## Step 5: Set Up Local Environment Variables

1. **Create `.env` file** in your project root:

```bash
# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...your-anon-key...
SUPABASE_SERVICE_KEY=eyJhbGc...your-service-role-key...

# Optional: Direct PostgreSQL connection
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

2. **Add `.env` to `.gitignore`** (if not already there):

```bash
echo ".env" >> .gitignore
```

## Step 6: Verify Connection (After Python Setup)

Once we install the Python packages, you can test the connection with:

```python
from supabase import create_client
import os

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

# Test query
response = supabase.table('question_sets').select("*").execute()
print(f"Connection successful! Found {len(response.data)} question sets.")
```

## Step 7: Configure Render Environment Variables

When deploying to Render, add these environment variables:

1. Go to Render dashboard
2. Select your service
3. Click **"Environment"** tab
4. Add these variables:
   - `SUPABASE_URL` = `https://xxxxxxxxxxxxx.supabase.co`
   - `SUPABASE_ANON_KEY` = `eyJhbGc...`
   - `SUPABASE_SERVICE_KEY` = `eyJhbGc...`

## Security Best Practices

### ✅ DO:
- Use `service_role` key only on the backend
- Keep `service_role` key in environment variables
- Use `anon` key for client-side if needed
- Enable RLS policies for production
- Regularly rotate keys

### ❌ DON'T:
- Commit keys to Git
- Share `service_role` key publicly
- Use `service_role` key in frontend JavaScript
- Disable RLS without proper policies

## Troubleshooting

### Connection Issues
- Verify URL and keys are correct
- Check if project is fully provisioned (wait 2-3 minutes)
- Ensure no typos in environment variables

### Permission Errors
- Verify RLS policies are set correctly
- Use `service_role` key for admin operations
- Check table permissions in Supabase dashboard

### Query Errors
- Check SQL syntax in Supabase SQL Editor
- Verify table names and column names
- Check data types match schema

## Next Steps

After completing this setup:
1. ✅ Verify all tables are created
2. ✅ Save your connection details securely
3. ✅ Create `.env` file with credentials
4. ⏳ Return to main terminal - we'll install Python packages next
5. ⏳ Run migration script to load existing questions

---

**Ready?** Once you've completed these steps, let me know and we'll proceed with the Python implementation!
