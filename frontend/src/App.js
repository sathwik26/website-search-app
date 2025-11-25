// frontend/src/App.js
import React, { useState } from "react";
import "./App.css";
import { searchWebsite } from "./api";

function App() {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [openIndex, setOpenIndex] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!url || !query) {
      setError("Please enter both website URL and search query.");
      return;
    }
    setError("");
    setLoading(true);
    setResults([]);

    try {
      const data = await searchWebsite(url, query);
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data.results || []);
      }
    } catch (err) {
      setError("Backend connection error.");
    } finally {
      setLoading(false);
    }
  };

  const toggleHtml = (idx) => {
    setOpenIndex(openIndex === idx ? null : idx);
  };

  return (
    <div className="app-wrapper">
      <h1 className="title">Website Content Search</h1>

      <div className="form">
        <input
          type="text"
          placeholder="Search URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <input
          type="text"
          placeholder="Search query (e.g. AI)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && <p>⏳ Searching...</p>}
      {error && <p className="error">{error}</p>}

      {results.length > 0 && (
        <div className="results">
          <h2>Search Results</h2>
          {results.map((r, idx) => (
            <div className="result-card" key={idx}>
              <div className="card-header">
                <div>
                  <h3>{r.title}</h3>
                  <p className="path">Path: {r.path}</p>
                </div>
                <div className="score-badge">{r.score}% match</div>
              </div>

              <button className="view-btn" onClick={() => toggleHtml(idx)}>
                {openIndex === idx ? "Hide HTML ▲" : "View HTML ▼"}
              </button>

              {openIndex === idx && (
                <pre className="html-block">
                  {r.html}
                </pre>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
