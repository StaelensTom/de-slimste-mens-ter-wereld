# Supabase Database Migration Plan

## Overview
Migrate from file-based question storage to Supabase PostgreSQL database for persistent, instant-update question management.

## Goals
- ✅ Single source of truth for all questions
- ✅ Instant updates without redeployment
- ✅ Persistent storage across Render redeployments
- ✅ Maintain all existing functionality
- ✅ Keep file-based backup capability

## Database Schema Design

### Table: `question_sets`
Stores metadata about question sets (formerly directories).

```sql
CREATE TABLE question_sets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_template BOOLEAN DEFAULT FALSE
);
```

### Table: `questions`
Stores all questions with their metadata and content.

```sql
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_set_id UUID REFERENCES question_sets(id) ON DELETE CASCADE,
    round_type VARCHAR(50) NOT NULL, -- '3-6-9', 'Open deur', 'Puzzel', 'Galerij', 'Collectief geheugen', 'Finale'
    position INTEGER NOT NULL, -- Order within the round
    data JSONB NOT NULL, -- Flexible JSON storage for question data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(question_set_id, round_type, position)
);

CREATE INDEX idx_questions_set_round ON questions(question_set_id, round_type);
CREATE INDEX idx_questions_data ON questions USING GIN(data);
```

### Table: `media_files`
Track uploaded media files (images, videos) for cleanup and management.

```sql
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_set_id UUID REFERENCES question_sets(id) ON DELETE CASCADE,
    filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(50), -- 'image', 'video'
    file_size BIGINT,
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(question_set_id, filename)
);
```

## Migration Steps

### Phase 1: Setup & Configuration (30 minutes)
1. ✅ Create new Git branch: `feature/supabase-database-migration`
2. ⏳ Set up Supabase project and database
3. ⏳ Install Python dependencies
4. ⏳ Create database connection module
5. ⏳ Create database schema (tables, indexes)

### Phase 2: Data Migration (45 minutes)
6. ⏳ Create migration script to read existing JSON files
7. ⏳ Load all question sets into database
8. ⏳ Verify data integrity
9. ⏳ Create backup export functionality

### Phase 3: Backend Updates (2 hours)
10. ⏳ Create database service layer (`app/db_service.py`)
11. ⏳ Update question loading logic in routes
12. ⏳ Update question saving logic in routes
13. ⏳ Update question set creation/deletion
14. ⏳ Update media upload handling
15. ⏳ Remove GitHub sync dependency for questions

### Phase 4: Frontend Updates (1 hour)
16. ⏳ Update question editor to work with database IDs
17. ⏳ Update question list loading
18. ⏳ Update save buttons (remove "Save to Server")
19. ⏳ Add real-time update indicators

### Phase 5: Testing (1 hour)
20. ⏳ Test question loading in game
21. ⏳ Test question editing and saving
22. ⏳ Test question set creation/deletion
23. ⏳ Test media upload
24. ⏳ Test all round types (3-6-9, Open deur, etc.)

### Phase 6: Deployment (30 minutes)
25. ⏳ Update `requirements.txt` with new dependencies
26. ⏳ Update Render environment variables
27. ⏳ Create deployment documentation
28. ⏳ Test on Render staging (if available)
29. ⏳ Deploy to production

### Phase 7: Cleanup & Documentation (30 minutes)
30. ⏳ Document new workflow
31. ⏳ Create database backup strategy
32. ⏳ Update README with database info
33. ⏳ Archive old GitHub sync code

## Technical Implementation Details

### New Python Dependencies
```
psycopg2-binary==2.9.9  # PostgreSQL adapter
supabase==2.3.0         # Supabase Python client
python-dotenv==1.0.0    # Environment variable management
```

### Environment Variables Needed
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key (for admin operations)
```

### File Structure Changes
```
app/
├── db_service.py          # NEW: Database service layer
├── db_models.py           # NEW: Database models/schemas
├── migrations/            # NEW: Database migration scripts
│   └── 001_initial_schema.sql
│   └── 002_migrate_data.py
├── main/
│   └── routes.py          # UPDATED: Use database instead of files
└── templates/
    └── manage_questions.html  # UPDATED: Remove GitHub sync UI
```

### Backward Compatibility
- Keep file-based loading as fallback for localhost development
- Add export functionality to backup questions to JSON files
- Maintain existing question format in JSONB for easy migration

## Rollback Plan
If issues arise:
1. Switch back to `main` branch
2. Redeploy previous version
3. Questions remain in database (no data loss)
4. Can export from database to files if needed

## Success Criteria
- ✅ All existing question sets loaded into database
- ✅ Game loads questions from database successfully
- ✅ Question editor saves to database instantly
- ✅ No deployment needed for question changes
- ✅ All round types work correctly
- ✅ Media files upload and display correctly
- ✅ Performance is equal or better than file-based system

## Timeline
- **Total estimated time:** 6-7 hours
- **Testing buffer:** +2 hours
- **Target completion:** 1 working day

## Risk Assessment

### Low Risk
- Database connection issues (easy to debug)
- Schema changes (can be migrated)

### Medium Risk
- Data migration errors (mitigated by keeping original files)
- Performance issues (mitigated by proper indexing)

### High Risk (Mitigated)
- Data loss (mitigated by keeping files as backup)
- Breaking existing functionality (mitigated by thorough testing)

## Next Steps
1. Follow Supabase setup guide below
2. Run migration scripts
3. Test locally
4. Deploy to Render
