# Question List Recovery - December 7, 2025

## 🔍 Problem Identified

Two question lists had issues after multiple syncs:
1. **fam-staelens-wang**: Reverted to old/incomplete version
2. **1ste-keer**: Most files reverted to default template questions

## ✅ What Was Recovered

### fam-staelens-wang (FULLY RECOVERED)
- **Source**: Commit `3a0e107` (earlier version with complete questions)
- **Status**: ✅ All files restored with complete custom Christmas/family questions
- **Files recovered**:
  - 3-6-9.json
  - Collectief geheugen.json
  - Galerij.json
  - Open deur.json
  - Puzzel.json

### 1ste-keer (PARTIALLY RECOVERED)
- **Finale.json**: ✅ Has complete custom questions (provinces, Disney princesses, etc.)
- **Galerij.json**: ⚠️ Has correct image references but placeholder answers
- **Other files**: ❌ Still have default template questions

## 📋 What Still Needs Work

### 1ste-keer Question List
The following files need to be recreated with custom questions:
- **3-6-9.json** - Currently has "Question 1", "Answer 1", etc.
- **Collectief geheugen.json** - Has videos/images but default questions
- **Open deur.json** - Has videos/images but default questions
- **Puzzel.json** - Default template
- **Galerij.json** - Has images but answers are "GA1 - Answer 1", etc.

### Available Assets for 1ste-keer
The following media files ARE present and can be used:
- ✅ Galerij images: galerij_1_1.png through galerij_3_10.png (30 images)
- ✅ Open deur videos: open-deur-1.mp4, open-deur-2.mp4, open-deur-3.mp4
- ✅ Open deur thumbnails: open-deur-1.png, open-deur-2.png, open-deur-3.png
- ✅ Collectief geheugen videos: collectief-geheugen-1/2/3.mp4
- ✅ Collectief geheugen thumbnails: collectief-geheugen-1/2/3.jpg

## 🔧 Root Cause Analysis

The issue likely occurred because:
1. **Concurrent editing**: Questions were edited on different devices
2. **Incomplete saves**: JSON files were edited but not saved before syncing
3. **Sync conflicts**: Auto-sync overwrote local changes with older versions
4. **No lock system**: Multiple people could edit simultaneously (now fixed in feature branch)

## 📝 Next Steps

### Option 1: Recreate on Other Laptop
If the questions were created on another laptop and not synced:
1. Check that laptop for local changes
2. Copy the JSON files manually
3. Sync to server

### Option 2: Recreate Using Editor
1. Open the question editor at `/manage_questions`
2. Select "1ste-keer" question set
3. Edit each file to add custom questions matching the media files
4. Save and sync to server

### Option 3: Manual File Edit
Edit the JSON files directly in this repository and commit

## 🚀 To Deploy Recovery

When ready to push the recovered fam-staelens-wang to production:

```bash
# Make sure you're on the recovery branch
git checkout recovery/question-lists

# Push to GitHub
git push origin recovery/question-lists

# Then merge to main
git checkout main
git merge recovery/question-lists
git push origin main
```

## 🔒 Prevention (Feature Branch Available)

A lock system has been implemented in branch `feature/question-set-locking` to prevent this issue:
- Locks question sets when editing
- Shows who is currently editing
- Prevents concurrent edits
- Auto-releases after 30 minutes

Consider merging this feature before creating new question sets.

## 📊 Commit References

- **fam-staelens-wang recovered from**: `3a0e107`
- **Latest (problematic) version was**: `7b2a605`
- **Recovery commit**: `08f4803`
