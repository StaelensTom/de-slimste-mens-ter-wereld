# Deployment Guide - tomstaelens.be/deslimstemensterwereld

## Overview
This project is automatically deployed to Siteground hosting via GitHub Actions whenever you push to the `main` branch.

## Initial Setup (One-Time)

### 1. Get Your Siteground FTP Credentials

1. Log in to your Siteground cPanel
2. Go to **Files** → **FTP Accounts**
3. Either use your main cPanel account or create a new FTP account specifically for this deployment
4. Note down:
   - **FTP Server**: Usually `ftp.tomstaelens.be` or similar
   - **FTP Username**: Your FTP username
   - **FTP Password**: Your FTP password

### 2. Add Secrets to GitHub Repository

1. Go to your GitHub repository: https://github.com/timdpaep/de-slimste-mens-ter-wereld
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these three secrets:

   - **Name**: `FTP_SERVER`
     - **Value**: Your FTP server address (e.g., `ftp.tomstaelens.be`)
   
   - **Name**: `FTP_USERNAME`
     - **Value**: Your FTP username
   
   - **Name**: `FTP_PASSWORD`
     - **Value**: Your FTP password

### 3. Prepare Server Directory

1. Log in to Siteground File Manager
2. Navigate to `public_html/`
3. Create a new folder called `deslimstemensterwereld`
4. This is where your files will be deployed

### 4. Server Configuration (Important!)

**Note**: This is a Flask/Python application. Siteground shared hosting typically only supports PHP by default. You have a few options:

#### Option A: Use Siteground Python App (Recommended if available)
1. Check if your Siteground plan supports Python applications
2. In cPanel, look for **Setup Python App**
3. Create a new Python application pointing to `/public_html/deslimstemensterwereld`

#### Option B: Convert to Static HTML (Simplest)
If you want to deploy just the static files (HTML, CSS, JS) without the Python backend, you would need to:
- Generate static HTML pages
- Remove server-side dependencies
- This won't support the real-time game features

#### Option C: Use a Different Hosting Service
For a Flask application with WebSockets, consider:
- **Heroku** (free tier available)
- **PythonAnywhere** (free tier available)
- **DigitalOcean App Platform**
- **Railway.app**
- **Render.com**

## How Deployment Works

1. You make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```
3. GitHub Actions automatically:
   - Detects the push
   - Connects to your Siteground server via FTP
   - Uploads all changed files to `/public_html/deslimstemensterwereld/`
4. Your site is updated at `https://tomstaelens.be/deslimstemensterwereld`

## Monitoring Deployments

1. Go to your GitHub repository
2. Click the **Actions** tab
3. You'll see all deployment runs
4. Click on any run to see detailed logs
5. Green checkmark = successful deployment
6. Red X = failed deployment (check logs for errors)

## Important Notes

⚠️ **Python Application Limitation**: 
- Siteground shared hosting may not support running Python Flask applications
- You may need to upgrade to a VPS or use a Python-specific hosting service
- Contact Siteground support to confirm Python/Flask support

⚠️ **File Permissions**:
- After first deployment, you may need to set file permissions via cPanel
- Python files typically need 644 permissions
- Directories need 755 permissions

⚠️ **Dependencies**:
- The `requirements.txt` file lists all Python dependencies
- These need to be installed on the server (may require SSH access)

## Testing Deployment

After setting up, test the deployment:

1. Make a small change to a file (e.g., add a comment)
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test deployment"
   git push origin main
   ```
3. Go to GitHub Actions tab and watch the deployment
4. Check your website to see if changes appear

## Troubleshooting

### Deployment fails with FTP error
- Check that your FTP credentials in GitHub Secrets are correct
- Verify the FTP server address
- Ensure the target directory exists on the server

### Files uploaded but site doesn't work
- This is likely because Flask/Python isn't running on Siteground
- Consider alternative hosting options listed above

### Need to rollback
- Go to a previous commit in GitHub
- Push that commit to trigger a new deployment

## Alternative: Manual FTP Upload

If GitHub Actions doesn't work, you can manually upload via FTP:

1. Use an FTP client like **FileZilla**
2. Connect to `ftp.tomstaelens.be` with your credentials
3. Navigate to `/public_html/deslimstemensterwereld/`
4. Upload all project files (except `.git`, `.venv`, `__pycache__`)

## Recommended Next Steps

Given that this is a Flask application with WebSockets, I recommend:

1. **Contact Siteground Support** to ask:
   - "Does my hosting plan support Python Flask applications?"
   - "Can I run a Python web server on port 10965?"
   - "Do you support WebSocket connections?"

2. **If Siteground doesn't support Python**:
   - Consider deploying to **PythonAnywhere** (free tier available)
   - Or **Heroku** (also has free tier)
   - Keep `tomstaelens.be` for other content
   - Use a subdomain or different service for this game

3. **If you want to keep it on Siteground**:
   - You may need to convert the application to use PHP
   - Or create a static version without real-time features
