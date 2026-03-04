# 3D Word Cloud Visualization

An interactive 3D word cloud application that analyzes news articles and visualizes article topics in an immersive 3D environment. Enter any news article URL, and watch the most important topics and keywords come to life in a beautiful, interactive 3D word cloud.

## 🎯 Features

- **Interactive 3D Visualization**: Rotate, zoom, and hover over words to explore topics
- **Automatic Article Analysis**: Powered by NLP (Natural Language Processing)
- **Real-time Processing**: Get instant insights from any news article
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Color-Coded Importance**: Words colored by relevance (blue → red gradient)
- **Frequency Indicators**: See how many times each term appears in the article

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript, Three.js, React Three Fiber, Vite
- **Backend**: FastAPI (Python), BeautifulSoup4, scikit-learn, NLTK
- **Deployment**: Vercel (Frontend), Render (Backend)

## 🚀 Live Demo

Visit the live application and start analyzing articles instantly!

## 📖 How It Works

1. **Input**: Paste a news article URL
2. **Scraping**: Backend fetches and extracts article content
3. **Analysis**: Text is processed using NLP techniques (tokenization, stop word removal, TF-IDF)
4. **Visualization**: Keywords are rendered in 3D space, sized and colored by importance
5. **Interaction**: Explore the word cloud with your mouse and scroll wheel

## 🎮 How to Use

1. Enter any news article URL in the input field
2. Click **Analyze** or press Enter
3. Wait a few seconds for processing
4. Explore the 3D word cloud:
   - **Left-click + drag** to rotate
   - **Scroll** to zoom in/out
   - **Hover** over words to see frequency and importance

## 💻 Local Development Setup

If you prefer to set up manually:

#### Backend Setup

```bash
cd Backend
python -m venv venv

# Activate virtual environment
# On Unix/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"

# Run the backend
uvicorn main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Backend will be available at http://localhost:8000 (API docs at http://localhost:8000/docs)
Frontend will be available at http://localhost:5173

## 🔧 Troubleshooting

### Frontend Issues
- **Module not found**: Run `npm install` in the frontend directory
- **Build errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- **Port already in use**: Vite will automatically try the next available port

### Backend Issues
- **Port already in use**: Kill process on port 8000 or change port in `backend/main.py`
- **NLTK data missing**: Run `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"`
- **Module not found**: Ensure virtual environment is activated

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

Made with ❤️ using React, Three.js, and FastAPI
