# 3D Word Cloud - Dinal

visualize article topics in an interactive 3d space using react three fiber and fastapi

## what you need

- python 3.9+
- node.js 16+
- thats it

## setup

clone the repo and run the setup script:

```bash
git clone <your-repo-url>
cd 3D-Word-Cloud-Dinal

# on mac/linux
chmod +x setup.sh
./setup.sh

# on windows
setup.bat
```

the script installs everything and starts both servers automatically

## if setup script doesnt work

### backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
uvicorn main:app --reload
```

### frontend
open a new terminal:
```bash
cd frontend
npm install
npm run dev
```

## using it

1. open http://localhost:5173 in your browser
2. paste an article url or click one of the sample urls
3. click analyze and wait a few seconds
4. interact with the 3d visualization - drag to rotate, scroll to zoom, hover over words

## sample urls

- https://www.bbc.com/news/technology
- https://techcrunch.com
- https://www.theguardian.com/technology

## tech stack

**backend:**
- fastapi for the api
- beautifulsoup4 for scraping articles
- scikit-learn for nlp/topic modeling
- nltk for text processing

**frontend:**
- react + typescript
- react three fiber for 3d graphics
- vite for fast development

## how it works

1. you give it an article url
2. backend scrapes the article content
3. nlp analysis extracts key topics using tf-idf
4. frontend renders the keywords as a 3d word cloud
5. word size = importance, color = relevance

## troubleshooting

**cant analyze article:**
- some sites block scrapers or are behind paywalls
- try a different url

**backend errors:**
- make sure youre in the venv
- check if nltk data downloaded properly

**frontend blank page:**
- check browser console for errors
- make sure backend is running on port 8000

**port already in use:**
- kill the process or change the port in the code

## api endpoints

- `POST /analyze` - analyze an article url
- `GET /health` - check if api is running
- `GET /docs` - interactive api documentation at http://localhost:8000/docs

## notes

- analysis takes 5-15 seconds depending on article length
- works best with articles between 500-5000 words
- returns up to 50 keywords
- only works with publicly accessible html pages

thats it, lookinf forward to hear from you!