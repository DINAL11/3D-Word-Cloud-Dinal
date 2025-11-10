# 3D Word Cloud Visualization

An interactive 3D word cloud application that analyzes news articles and visualizes topics using React Three Fiber and FastAPI.

## Tech Stack

### Frontend
- React 18 with TypeScript
- React Three Fiber (Three.js for React)
- @react-three/drei for 3D helpers
- Vite for build tooling
- Tailwind CSS for styling

### Backend
- Python 3.9+
- FastAPI
- BeautifulSoup4 for web scraping
- scikit-learn for NLP/topic modeling
- NLTK for text processing
- requests for HTTP calls

## Prerequisites

- Node.js 16+ and npm
- Python 3.9+
- pip (Python package manager)

## Quick Start

### One-Command Setup (Recommended)

From the project root directory, run:

```bash
# On Unix/Mac/Linux
chmod +x setup.sh
./setup.sh

# On Windows
setup.bat
```

This script will:
1. Install all frontend dependencies
2. Install all backend dependencies
3. Download required NLTK data
4. Start both servers concurrently

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

If you prefer to set up manually:

#### Backend Setup

```bash
cd backend
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


## How It Works

1. **User Input**: User enters a news article URL
2. **Article Fetching**: Backend scrapes the article content using BeautifulSoup
3. **Text Processing**: Text is cleaned, tokenized, and stop words are removed
4. **Topic Modeling**: TF-IDF vectorization extracts key terms and their importance
5. **Visualization**: Frontend renders words in 3D space with size/color based on weight
6. **Interaction**: Users can rotate, zoom, and interact with the word cloud


## Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `backend/main.py` or kill process on port 8000
- **NLTK data missing**: Run `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`
- **Module not found**: Ensure virtual environment is activated and dependencies installed

### Frontend Issues
- **Port already in use**: Vite will automatically try the next available port
- **Module not found**: Run `npm install` in the frontend directory
- **Build errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### CORS Issues
- Backend includes CORS middleware for localhost development
- For production, update allowed origins in `backend/main.py`
