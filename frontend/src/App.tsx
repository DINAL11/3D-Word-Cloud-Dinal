import { useState } from 'react';
import WordCloud3D from './components/WordCloud3D';
import './App.css';

interface WordData {
  word: string;
  weight: number;
  frequency: number;
}

interface AnalysisResult {
  words: WordData[];
  article_title: string;
  word_count: number;
  url: string;
}

// Sample article URLs for convenience
const SAMPLE_URLS = [
  'https://www.bbc.com/news/technology',
  'https://www.theguardian.com/technology',
  'https://techcrunch.com/',
  'https://www.reuters.com/technology/',
];

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze article');
      }

      const data: AnalysisResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setUrl('');
    setResult(null);
    setError(null);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !loading) {
      handleAnalyze();
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">3D Word Cloud</h1>
          <p className="subtitle">
            Visualize article topics in an interactive 3D space
          </p>
        </header>

        {!result ? (
          <div className="input-section">
            <div className="input-group">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter article URL..."
                className="url-input"
                disabled={loading}
              />
              <button
                onClick={handleAnalyze}
                disabled={loading || !url.trim()}
                className="analyze-button"
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  'Analyze'
                )}
              </button>
            </div>

            {error && (
              <div className="error-message">
                <svg
                  className="error-icon"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                {error}
              </div>
            )}

            <div className="sample-urls">
              <p className="sample-title">Try these sample articles:</p>
              <div className="url-buttons">
                {SAMPLE_URLS.map((sampleUrl, index) => (
                  <button
                    key={index}
                    onClick={() => setUrl(sampleUrl)}
                    className="sample-button"
                    disabled={loading}
                  >
                    {new URL(sampleUrl).hostname.replace('www.', '')}
                  </button>
                ))}
              </div>
            </div>

            <div className="info-box">
              <h3>How it works:</h3>
              <ol>
                <li>Enter a news article URL or select a sample</li>
                <li>Click "Analyze" to extract and process the content</li>
                <li>Explore the 3D visualization of key topics and terms</li>
                <li>Interact with the word cloud (rotate, zoom, hover)</li>
              </ol>
            </div>
          </div>
        ) : (
          <div className="result-section">
            <div className="result-header">
              <div className="result-info">
                <h2 className="result-title">{result.article_title}</h2>
                <p className="result-stats">
                  {result.words.length} keywords from {result.word_count} words
                </p>
              </div>
              <button onClick={handleReset} className="reset-button">
                ← New Analysis
              </button>
            </div>

            <div className="canvas-container">
              <WordCloud3D words={result.words} />
            </div>

            <div className="instructions">
              <p>
                🖱️ <strong>Rotate:</strong> Left-click and drag
                {' | '}
                🔍 <strong>Zoom:</strong> Scroll wheel
                {' | '}
                👆 <strong>Hover:</strong> See word details
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;