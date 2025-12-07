# De Slimste Mens Ter Wereld 🎮

An interactive web-based game show application based on the popular Belgian quiz show "De Slimste Mens Ter Wereld" (The Smartest Person in the World).

This repository was forked from [AntheSevenants](https://github.com/AntheSevenants/dsmtw)

## ✨ Features

- **Dual-screen setup**: Separate views for host (presenter) and players (audience display)
- **Online question management**: Create and edit questions through a web interface
- **Multiple game rounds**: 3-6-9, Open deur, Puzzel, Galerij, Collectief geheugen, and Finale
- **YouTube integration**: Use YouTube videos instead of file uploads to save storage
- **Real-time gameplay**: Socket.io-based live updates across all connected devices
- **Customizable intros**: Manual control over game show intros and bumpers

## 🎯 Game Rounds

1. **3-6-9**: Answer questions for 3, 6, or 9 points based on difficulty
2. **Open deur**: Choose from multiple video questions
3. **Puzzel**: Solve word puzzles with hints
4. **Galerij**: Identify items from a series of images
5. **Collectief geheugen**: List items from a category after watching a video
6. **Finale**: Final showdown with accumulated points as time

## 🚀 Deployment on Render (Free Tier)

This application can be deployed for **free** on [Render](https://render.com):

1. **Fork this repository** to your GitHub account
2. **Create a Render account** at [render.com](https://render.com)
3. **Create a new Web Service**:
   - Connect your GitHub repository
   - Select the forked repository
   - Render will auto-detect the Python environment
   - Deploy with default settings
4. **Access your game** at the provided Render URL

### ⚠️ Storage Limitations

Render's free tier has **limited ephemeral storage**. To avoid issues:
- ✅ **Use YouTube URLs** for videos (Open deur, Collectief geheugen)
- ✅ **Use image URLs** from external sources (Imgur, image hosting services)
- ❌ **Avoid uploading** large files directly to the server

The question editor supports both uploads and URLs, but **URLs are strongly recommended** for production use.

## 🎮 How to Play

### Setup

1. **Navigate to the landing page** at your deployed URL
2. **Select a question set** from the available directories
3. **Enter player names** (2-4 players recommended)
4. **Click "Start Game"**

### Dual-Screen Setup

Open **two browser windows**:

1. **Player View** (for audience/screen):
   - Full URL: `https://your-app.onrender.com/game`
   - Shows questions, answers, scores, and media
   - Display this on a TV or projector

2. **Host View** (for presenter):
   - Add `?host=true` to URL: `https://your-app.onrender.com/game?host=true`
   - Shows control buttons and debug information
   - Keep this on the presenter's device

Both views stay synchronized in real-time!

## 📝 Managing Questions

### Online Editor

1. Navigate to **"Beheer vragenlijsten"** (Manage Questions)
2. Select a question set to edit
3. Create or modify questions for each round
4. Click **"Opslaan"** (Save) to save locally
5. Click **"💾 Bewaar naar server"** to sync to GitHub (manual deploy required)

### Question Format

Each round has its own JSON file with specific formats:

- **3-6-9.json**: Questions with point values and answers
- **Open deur.json**: Questions with YouTube URLs and multiple answers
- **Puzzel.json**: Word puzzles with hints and keywords
- **Galerij.json**: Image URLs with corresponding answers
- **Collectief geheugen.json**: YouTube URLs with lists of answers
- **Finale.json**: Final round questions with answers

### Best Practices

- Use **YouTube URLs** for videos (auto-extracts thumbnails)
- Use **image hosting URLs** (Imgur, Cloudinary, etc.) for images
- Test questions in the editor before playing
- Create backup copies of your question sets

## 💻 Local Development

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/de-slimste-mens-ter-wereld.git
   cd de-slimste-mens-ter-wereld
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python dsmtw.py
   ```

4. Open your browser at `http://localhost:5000`

## 🎨 Customization

- **Question sets**: Create new folders with JSON files for custom question sets
- **Styling**: Modify CSS in `app/static/css/`
- **Sounds**: Replace audio files in `app/static/sounds/`
- **Game logic**: Edit Python files in `erik/` and `gameshow/`

## 📦 Project Structure

```
├── app/                    # Flask application
│   ├── main/              # Routes and socket events
│   ├── static/            # CSS, JS, sounds, images
│   └── templates/         # HTML templates
├── erik/                  # Game logic (De Slimste Mens)
├── gameshow/              # Base gameshow framework
├── default/               # Default question set
├── [custom-sets]/         # Your custom question sets
└── requirements.txt       # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Create custom question sets

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- Original concept: [AntheSevenants](https://github.com/AntheSevenants/dsmtw)
- Based on the Belgian TV show "De Slimste Mens Ter Wereld"

---

**Enjoy hosting your own game show! 🎉**
- On [this location](https://drive.google.com/drive/folders/12WWNlmYh9vjv9atfELKr7bAB-YRkfpPX?usp=drive_link) you can find some open sourced questions and assets. **Please note that you need to create own videos for the "Open Deur" round.**

## Start The Game

Open up the application by: `python3 dsmtw.py listen [PATH OF QUESTIONS] [LIST OF PLAYERS]`. If you want to open up the default questions, this command should work: `python3 dsmtw.py listen "./default" "Alfred,Marie,Carla"`
