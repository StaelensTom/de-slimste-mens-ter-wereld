# GitHub Sync Setup Guide

This guide explains how to enable automatic GitHub synchronization for question sets, so that any changes made through the web editor are automatically committed to your GitHub repository.

## Why GitHub Sync?

Without GitHub sync, any question sets created or edited on Render.com will be **lost** when you deploy new code updates. With GitHub sync enabled:

✅ Question sets created on production are saved to GitHub  
✅ Edits made on production persist across deployments  
✅ Full version history of all changes  
✅ No manual download/upload needed  

## Setup Steps

### 1. Create a GitHub Personal Access Token

1. Go to GitHub.com and log in
2. Click your profile picture → **Settings**
3. Scroll down and click **Developer settings** (left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a name: `DSMTW Question Sync`
7. Set expiration: **No expiration** (or 1 year if you prefer)
8. Select scopes:
   - ✅ **repo** (Full control of private repositories)
     - This includes: repo:status, repo_deployment, public_repo, repo:invite, security_events
9. Click **Generate token**
10. **IMPORTANT**: Copy the token immediately! You won't be able to see it again.
    - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. Add Environment Variables to Render

1. Go to your Render.com dashboard
2. Select your **de-slimste-mens-ter-wereld** web service
3. Click **Environment** in the left sidebar
4. Add these environment variables:

| Key | Value | Example |
|-----|-------|---------|
| `GITHUB_TOKEN` | Your personal access token from step 1 | `ghp_xxxxxxxxxxxxxxxxxxxx` |
| `GITHUB_REPO` | Your repository in format `username/repo` | `StaelensTom/de-slimste-mens-ter-wereld` |
| `GITHUB_BRANCH` | Branch to commit to (usually `main`) | `main` |

5. Click **Save Changes**
6. Render will automatically redeploy your application

### 3. Verify It Works

1. Go to your live site
2. Navigate to **Beheer vragenlijsten**
3. Edit a question in the `default` set
4. Click **Opslaan**
5. Check your GitHub repository - you should see a new commit!

## How It Works

When you save questions or create a new question set through the web interface:

1. **Local Save**: Changes are saved to the server's file system
2. **GitHub Commit**: Changes are automatically committed to your GitHub repository
3. **Next Deployment**: When Render rebuilds, it pulls the latest code from GitHub, including your question changes

## Troubleshooting

### "GitHub sync is disabled"

This message appears in the logs if:
- `GITHUB_TOKEN` is not set
- `GITHUB_REPO` is not set
- The token is invalid

**Solution**: Double-check your environment variables in Render.

### "Failed to commit to GitHub"

Possible causes:
- Token doesn't have `repo` permission
- Repository name is incorrect (should be `username/repo-name`)
- Branch doesn't exist

**Solution**: Verify your token permissions and repository name.

### Changes aren't showing up in GitHub

- Check Render logs for error messages
- Verify the token hasn't expired
- Make sure you're looking at the correct branch

## Security Notes

⚠️ **Keep your token secret!**
- Never commit the token to your repository
- Only add it as an environment variable in Render
- If the token is compromised, revoke it immediately and generate a new one

## Local Development

When running locally, GitHub sync is **optional**. If you don't set the environment variables, the app will work normally but won't commit to GitHub. This is perfect for testing!

To enable GitHub sync locally:
1. Create a `.env` file in the project root
2. Add your environment variables:
   ```
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_REPO=StaelensTom/de-slimste-mens-ter-wereld
   GITHUB_BRANCH=main
   ```
3. Make sure `.env` is in `.gitignore` (it already is!)

## Questions?

If you run into issues, check the Render logs for detailed error messages. The GitHub sync module prints helpful messages when it commits files or encounters errors.
