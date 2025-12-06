# Moving Repository to Your Own GitHub Account

## Current Situation
Your local repository is linked to: `https://github.com/timdpaep/de-slimste-mens-ter-wereld`

## Goal
Create your own copy on GitHub so you can:
- Push your changes
- Deploy from your own repository
- Have full control

## Method 1: Fork the Repository (Recommended)

### Step 1: Fork on GitHub
1. Go to https://github.com/timdpaep/de-slimste-mens-ter-wereld
2. Click the **"Fork"** button (top right)
3. Select your GitHub account
4. GitHub will create a copy at `https://github.com/YOUR-USERNAME/de-slimste-mens-ter-wereld`

### Step 2: Update Your Local Repository
Open PowerShell in your project directory and run:

```powershell
# Check current remote
git remote -v

# Remove old remote
git remote remove origin

# Add your new remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/de-slimste-mens-ter-wereld.git

# Verify it's changed
git remote -v

# Push your local changes to your fork
git push -u origin main
```

### Step 3: Done!
Your repository is now on your GitHub account and you can push changes anytime.

---

## Method 2: Create New Repository (Alternative)

If you don't want to fork (e.g., you want a different name):

### Step 1: Create New Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `de-slimste-mens-ter-wereld` (or your choice)
3. Description: "De Slimste Mens Ter Wereld game"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **"Create repository"**

### Step 2: Update Your Local Repository
```powershell
# Check current remote
git remote -v

# Remove old remote
git remote remove origin

# Add your new remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/de-slimste-mens-ter-wereld.git

# Push your code
git push -u origin main
```

---

## Verification

After updating, verify everything works:

```powershell
# Check remote is correct
git remote -v
# Should show: https://github.com/YOUR-USERNAME/de-slimste-mens-ter-wereld.git

# Make a test change
echo "# Test" >> test.txt
git add test.txt
git commit -m "Test commit"
git push

# Check on GitHub - you should see the new commit
```

---

## Update Render Deployment

After moving to your own repository:

1. Go to https://render.com
2. When creating the web service, connect to **your** repository
3. The deployment will now use your GitHub account

---

## Keeping in Sync with Original (Optional)

If you want to get updates from the original repository:

```powershell
# Add original as "upstream"
git remote add upstream https://github.com/timdpaep/de-slimste-mens-ter-wereld.git

# To get updates from original:
git fetch upstream
git merge upstream/main

# Push to your fork
git push origin main
```

---

## Common Issues

### "Permission denied" when pushing
- Make sure you're using your own repository URL
- You may need to authenticate with GitHub
- Use a Personal Access Token if prompted for password

### "Branch 'main' doesn't exist"
Try `master` instead:
```powershell
git push -u origin master
```

### Want to rename the repository?
1. Go to your GitHub repository
2. Click **Settings**
3. Change the repository name
4. Update local remote:
```powershell
git remote set-url origin https://github.com/YOUR-USERNAME/NEW-NAME.git
```

---

## Next Steps After Moving

1. ✅ Verify you can push to your repository
2. ✅ Update any documentation that references the old URL
3. ✅ Deploy to Render using your repository
4. ✅ Continue development!
