# Deployment to PythonAnywhere - De Slimste Mens Ter Wereld

## Why PythonAnywhere?
- ✅ Free tier available
- ✅ Native Python/Flask support
- ✅ WebSocket support
- ✅ Easy GitHub integration
- ✅ No credit card required for free tier

Your app will be available at: `https://yourusername.pythonanywhere.com`

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Sign up with your email

### 2. Clone Your Repository

1. Once logged in, go to **"Consoles"** tab
2. Click **"Bash"** to open a new console
3. Run these commands:

```bash
# Clone your repository
git clone https://github.com/timdpaep/de-slimste-mens-ter-wereld.git

# Navigate to the directory
cd de-slimste-mens-ter-wereld

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Web App

1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Click **"Next"** (accept the default domain)
4. Select **"Manual configuration"**
5. Choose **"Python 3.11"**
6. Click **"Next"**

### 4. Configure the Web App

In the **Web** tab, you'll see a configuration page. Update these sections:

#### A. Source Code
- **Source code**: `/home/yourusername/de-slimste-mens-ter-wereld`
- **Working directory**: `/home/yourusername/de-slimste-mens-ter-wereld`

#### B. Virtualenv
- **Virtualenv**: `/home/yourusername/de-slimste-mens-ter-wereld/venv`

#### C. WSGI Configuration File
1. Click on the **WSGI configuration file** link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
2. **Delete all the content** in the file
3. Replace with this:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/de-slimste-mens-ter-wereld'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables if needed
os.environ['FLASK_APP'] = 'dsmtw.py'

# Import the Flask app
from app import create_app, socketio

# Create the application
application = create_app(None, None, debug=False)

# Note: PythonAnywhere doesn't support WebSockets in free tier
# The app will work but real-time features may be limited
```

4. **Important**: Replace `yourusername` with your actual PythonAnywhere username
5. Click **"Save"**

### 5. Configure Static Files

In the **Web** tab, scroll to **Static files** section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/de-slimste-mens-ter-wereld/app/static/` |

Click **"Save"**

### 6. Reload Your Web App

1. Scroll to the top of the **Web** tab
2. Click the big green **"Reload yourusername.pythonanywhere.com"** button
3. Wait for it to finish

### 7. Visit Your Site!

Go to: `https://yourusername.pythonanywhere.com`

## Important Notes About Free Tier

⚠️ **WebSocket Limitations**:
- PythonAnywhere's free tier **does not support WebSockets**
- Your app will load, but real-time features (Socket.IO) won't work
- Players won't see live updates

**Solutions**:
1. **Upgrade to Paid Plan** ($5/month) - Enables WebSockets
2. **Modify App** - Remove real-time features, use polling instead
3. **Use Different Service** - Heroku, Railway, or Render support WebSockets on free tier

## Updating Your Deployment

When you make changes to your code:

### Option A: Manual Update (Simple)
1. Go to **Consoles** → **Bash**
2. Run:
```bash
cd de-slimste-mens-ter-wereld
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # If dependencies changed
```
3. Go to **Web** tab
4. Click **"Reload"**

### Option B: Automated with GitHub Actions
You can set up automatic deployment, but it requires:
1. SSH key setup on PythonAnywhere
2. GitHub Actions workflow
3. More complex configuration

Let me know if you want help setting this up!

## Troubleshooting

### Error: "Something went wrong"
1. Go to **Web** tab
2. Check **Error log** (click the link)
3. Check **Server log** (click the link)
4. Common issues:
   - Wrong paths in WSGI file
   - Missing dependencies
   - Python version mismatch

### App loads but doesn't work
- Check if you're trying to access game features (they need WebSockets)
- Check browser console for errors
- Verify static files are loading

### Can't connect to game
- Free tier doesn't support the Socket.IO real-time features
- Consider upgrading or using a different service

## Alternative: Deploy to Render.com (Free + WebSockets)

If you need WebSockets on free tier, **Render.com** is a better option:

1. Sign up at https://render.com
2. Connect your GitHub repository
3. Create a new **Web Service**
4. Render will auto-detect Flask and deploy
5. Full WebSocket support on free tier

Would you like instructions for Render.com instead?

## Linking from tomstaelens.be

Once deployed, you can link to your game from your Siteground site:

In your `tomstaelens.be/public_html/index.html`:
```html
<a href="https://yourusername.pythonanywhere.com">
  Play De Slimste Mens Ter Wereld
</a>
```

Or use a redirect in Siteground's `/public_html/deslimstemensterwereld/.htaccess`:
```apache
Redirect 301 /deslimstemensterwereld https://yourusername.pythonanywhere.com
```
