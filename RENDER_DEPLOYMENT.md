# Deployment to Render.com - De Slimste Mens Ter Wereld

## Why Render.com? ⭐ RECOMMENDED

- ✅ **Free tier with WebSockets** (unlike PythonAnywhere)
- ✅ Auto-deploy from GitHub (push = automatic deployment)
- ✅ Native Python/Flask support
- ✅ No credit card required
- ✅ Custom domains supported (can use tomstaelens.be subdomain)
- ✅ HTTPS included
- ✅ Better for real-time game features

Your app will be available at: `https://your-app-name.onrender.com`

## Files Already Created ✅

I've already created the necessary configuration files:
- ✅ `render.yaml` - Render deployment configuration
- ✅ Modified `dsmtw.py` - Now supports Render's PORT environment variable

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

First, commit and push all the new files:

```bash
git add .
git commit -m "Add Render.com deployment configuration"
git push origin main
```

### 2. Create Render Account

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (easiest option)
4. Authorize Render to access your repositories

### 3. Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your repository:
   - If you signed up with GitHub, you'll see your repos
   - Find **"de-slimste-mens-ter-wereld"**
   - Click **"Connect"**

### 4. Configure the Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `de-slimste-mens-ter-wereld` (or your choice) |
| **Region** | `Frankfurt (EU Central)` (closest to Belgium) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python dsmtw.py` |
| **Instance Type** | `Free` |

### 5. Add Environment Variable

Scroll down to **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `RENDER` | `true` |

This tells your app it's running on Render.

### 6. Deploy!

1. Click **"Create Web Service"**
2. Render will start building and deploying
3. Watch the logs - it takes 2-5 minutes
4. When you see "Your service is live 🎉", it's ready!

### 7. Visit Your Game!

Click the URL at the top (e.g., `https://de-slimste-mens-ter-wereld.onrender.com`)

## Auto-Deployment 🚀

Now, whenever you push to GitHub:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render automatically:
1. Detects the push
2. Rebuilds your app
3. Deploys the new version
4. Takes about 2-3 minutes

### 📝 Question Management & Syncing

The app includes a **manual sync system** to protect your question sets:

1. **Edit questions** in the online editor ("Beheer vragenlijsten")
2. Click **"Opslaan"** to save locally in browser
3. Click **"💾 Bewaar naar server"** to commit to GitHub
4. **Manually redeploy** on Render (or wait for auto-deploy if you push other changes)

#### Protected Question Sets

The following question sets are **protected** from being overwritten:
- `default` - Template question set
- `template` - Example question set

This prevents accidental loss of reference materials. Create your own question sets by copying these templates.

#### Sync Cooldown

To prevent excessive GitHub commits, the sync button has a **5-minute cooldown** between syncs. This ensures your repository history stays clean and manageable.

## Monitoring Your App

### View Logs
1. Go to your Render dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time application logs

### Check Status
- Green dot = Running
- Yellow dot = Deploying
- Red dot = Failed (check logs)

## Linking from tomstaelens.be

Once deployed, you can redirect from your Siteground site.

### Option 1: Simple Link
In your `tomstaelens.be` website:
```html
<a href="https://de-slimste-mens-ter-wereld.onrender.com">
  Play De Slimste Mens Ter Wereld
</a>
```

### Option 2: Redirect (Recommended)
Create `/public_html/deslimstemensterwereld/.htaccess` on Siteground:
```apache
Redirect 301 / https://de-slimste-mens-ter-wereld.onrender.com
```

Now `tomstaelens.be/deslimstemensterwereld` redirects to your Render app!

### Option 3: Custom Domain (Advanced)
You can use a subdomain like `game.tomstaelens.be`:

1. In Siteground cPanel, add DNS record:
   - Type: `CNAME`
   - Name: `game`
   - Value: `de-slimste-mens-ter-wereld.onrender.com`

2. In Render dashboard:
   - Go to **Settings** → **Custom Domain**
   - Add `game.tomstaelens.be`
   - Render will provide SSL certificate automatically

## Important Notes

### Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- 750 hours/month (enough for most personal projects)
- No credit card required

### Keeping App Awake (Optional)
If you want to prevent sleeping, you can:
1. Upgrade to paid plan ($7/month)
2. Use a service like UptimeRobot to ping your app every 10 minutes
3. Accept the wake-up delay (most common for free tier)

### WebSocket Support
✅ Fully supported on free tier! Your real-time game features will work perfectly.

## Troubleshooting

### Build Failed
- Check **Logs** tab for errors
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Python version mismatch
  - Syntax errors in code

### App Crashes on Start
- Check **Logs** tab
- Look for Python errors
- Verify `dsmtw.py` runs locally first

### Can't Access Game
- Make sure service shows "Live" (green dot)
- Check if app is sleeping (first request takes longer)
- Verify URL is correct

### Real-time Features Not Working
- Check browser console for WebSocket errors
- Verify Socket.IO is connecting
- Check Render logs for connection errors

## Testing Locally

Your app still works locally! Run:

```bash
.\.venv\Scripts\python.exe dsmtw.py
```

It will use `127.0.0.1:10965` locally and `0.0.0.0:$PORT` on Render automatically.

## Next Steps

1. ✅ Commit and push your code
2. ✅ Create Render account
3. ✅ Deploy your service
4. ✅ Test the game
5. ✅ Set up redirect from tomstaelens.be
6. 🎮 Share with friends!

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Your app logs: Available in Render dashboard

---

**Ready to deploy?** Just push your code to GitHub and follow steps 2-6 above!
