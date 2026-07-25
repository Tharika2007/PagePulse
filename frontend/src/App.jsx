import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  const auditWebsite = async () => {
    setError("");
    setReport(null);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/audit",
        {
          url: url,
        }
      );

      setReport(response.data);
    } catch (err) {
      if (err.response) {
        setError(err.response.data.detail);
      } else {
        setError("Unable to connect to backend.");
      }
    }
  };

  return (
    <div className="container">
      <h1>Page Pulse</h1>

      <input
        type="text"
        placeholder="Enter Website URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button onClick={auditWebsite}>
        Audit
      </button>

      {error && (
        <p className="error">{error}</p>
      )}

      {report && (
        <div className="report">
          <p><strong>Status:</strong> {report.status}</p>
          <p><strong>Response Time:</strong> {report.response_time_ms} ms</p>
          <p><strong>Title:</strong> {report.title}</p>
          <p><strong>Meta Description:</strong> {report.meta_description}</p>
          <p><strong>H1 Count:</strong> {report.h1_count}</p>
          <p><strong>Missing Alt Images:</strong> {report.missing_alt_images}</p>
          <p><strong>Word Count:</strong> {report.word_count}</p>
        </div>
      )}

      <footer className="footer">
        Built for Digital Heroes Training Task •{" "}
        <a
          href="https://digitalheroesco.com"
          target="_blank"
          rel="noreferrer"
        >
          digitalheroesco.com
        </a>
      </footer>
    </div>
  );
}

export default App;