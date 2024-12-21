import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import LoadingAnimation from './components/spinner';

function App() {
  const [news, setNews] = useState(''); // User input
  const [result, setResult] = useState(null); // API response
  const [error, setError] = useState(null); // Error handling
  const [loading, setLoading] = useState(false); // Error handling

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload on form submission
    setResult(null); // Reset previous result
    setError(null); // Reset previous errors
    setLoading(true);

    try {
      const response = await axios.post('https://fake-news-detection-f27h.onrender.com/predict', {
        news,
      });
      setResult(response.data.prediction); // Update result
    } catch (err) {
      setError('Error connecting to the API. Please try again.');
    }
    finally {
      setLoading(false)
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Fake News Detection</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            value={news}
            onChange={(e) => setNews(e.target.value)}
            placeholder="Enter the news article here..."
            rows="5"
            cols="50"
            required
          />
          <br />
          <button type="submit" disabled={loading}>
            {loading ? 'Checking...' : 'Check'}
          </button>
        </form>

        {loading && <LoadingAnimation></LoadingAnimation>} {/* Spinner shown when loading */}
        {result && (
          <div className={`result ${result === 'Fake' ? 'fake' : 'real'}`}>
            <h2>Result: {result}</h2>
          </div>
        )}

        {error && <div className="error">{error}</div>}
      </header>
    </div>
  );
}

export default App;
