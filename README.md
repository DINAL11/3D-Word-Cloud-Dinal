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

### One-Command Setup (Recommended) - Local Development

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

## Deployment

### Frontend Deployment (Vercel)

1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Click "Add New..." → "Project"
4. Import your GitHub repository
5. Configure build settings:
   - **Framework Preset**: Vite
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `npm install`
6. Add environment variables if needed (VITE_API_URL pointing to your Render backend)
7. Deploy

Vercel will automatically deploy on every push to main. Frontend URL will be provided after deployment.

### Backend Deployment (Render)

1. Push your code to GitHub
2. Go to [Render](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: 3D-Word-Cloud-Backend
   - **Root Directory**: `Backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Set environment variables:
   - Add `PYTHON_VERSION = 3.9` (or your Python version)
7. Deploy

After deployment, note your Render backend URL (e.g., `https://3d-word-cloud-backend.onrender.com`) and update your frontend `.env` file with:
```
VITE_API_URL=https://your-render-backend-url
```

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
- **TypeScript errors on build**: Ensure all Three.js refs use correct types (Mesh for meshes, Group for groups)

### Deployment Issues
- **NLTK data not downloading on Render**: Ensure the build command includes NLTK downloads: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"`
- **CORS errors in production**: Update `backend/main.py` to include your Vercel frontend domain in allowed origins
- **Cold starts on Render**: Free tier has 15-minute inactivity spindown. Upgrade for production use

### CORS Configuration for Production

In `backend/main.py`, update the CORS middleware:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vercel-domain.vercel.app",  # Your Vercel frontend URL
        "http://localhost:5173",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Recent Fixes

- **Fixed TypeScript compilation error** in `src/components/WordCloud3D.tsx`: Changed ref type from `THREE.Mesh` to `THREE.Group` for proper group element typing
- **Added deployment configuration** for Vercel (frontend) and Render (backend)
