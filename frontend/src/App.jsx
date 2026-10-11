import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';
const disclaimer = 'Academic demonstration only. Not intended for medical diagnosis or treatment. Results must not be used as a substitute for professional medical testing.';

function BoxOverlay({ analysis, imageSize }) {
  const pads = analysis?.strip_detection?.pads || analysis?.detected_pads || [];
  const quality = analysis?.image_metadata?.quality || analysis?.strip_detection?.quality;
  if (!pads.length || !imageSize.width || !quality?.width) return null;
  return (
    <div className="overlay">
      {pads.map((pad) => (
        <div
          key={`${pad.parameter}-${pad.order}`}
          className="pad-box"
          style={{
            left: `${(pad.x / quality.width) * 100}%`,
            top: `${(pad.y / quality.height) * 100}%`,
            width: `${(pad.width / quality.width) * 100}%`,
            height: `${(pad.height / quality.height) * 100}%`
          }}
          title={pad.parameter}
        />
      ))}
    </div>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 });

  const rows = useMemo(() => analysis?.measurements || [], [analysis]);

  async function loadHistory() {
    try {
      const response = await fetch(`${API_BASE}/api/results`);
      const data = await response.json();
      setHistory(data.results || []);
    } catch {
      setHistory([]);
    }
  }

  useEffect(() => { loadHistory(); }, []);

  function onFileChange(event) {
    const selected = event.target.files?.[0];
    setFile(selected || null);
    setAnalysis(null);
    setError('');
    setImageSize({ width: 0, height: 0 });
    setPreview(selected ? URL.createObjectURL(selected) : '');
  }

  async function analyze() {
    if (!file) {
      setError('Choose a PNG or JPEG strip image first.');
      return;
    }
    setLoading(true);
    setError('');
    const body = new FormData();
    body.append('image', file);
    try {
      const response = await fetch(`${API_BASE}/api/analyze`, { method: 'POST', body });
      const data = await response.json();
      if (!response.ok) throw new Error(data.details?.detail || data.error || 'Analysis failed.');
      setAnalysis(data);
      await loadHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <header className="topbar">
        <div>
          <h1>Urine Strip Colorimetric Analyzer</h1>
          <p>Measured RGB, HSV, and CIE Lab values are compared with replaceable demo reference colors.</p>
        </div>
        <div className="badge">Microservices Demo</div>
      </header>

      <section className="disclaimer">{disclaimer}</section>

      <section className="workspace">
        <div className="panel upload-panel">
          <h2>Upload Strip Image</h2>
          <input type="file" accept="image/png,image/jpeg" onChange={onFileChange} />
          <button onClick={analyze} disabled={loading || !file}>{loading ? 'Processing...' : 'Analyze Image'}</button>
          {error && <p className="error">{error}</p>}
          {analysis?.ml_warning && <p className="warning">{analysis.ml_warning}</p>}
          <div className="preview-wrap">
            {preview ? (
              <>
                <img src={preview} alt="Uploaded strip preview" onLoad={(event) => setImageSize({ width: event.currentTarget.clientWidth, height: event.currentTarget.clientHeight })} />
                <BoxOverlay analysis={analysis} imageSize={imageSize} />
              </>
            ) : <div className="placeholder">Image preview</div>}
          </div>
        </div>

        <div className="panel">
          <h2>Strip Detection</h2>
          <dl className="facts">
            <div><dt>Status</dt><dd>{analysis ? 'Detected' : 'Waiting'}</dd></div>
            <div><dt>Quality</dt><dd>{analysis?.image_metadata?.quality?.quality || '-'}</dd></div>
            <div><dt>Pad Count</dt><dd>{analysis?.detected_pads?.length || '-'}</dd></div>
            <div><dt>Layout</dt><dd>{analysis?.image_metadata?.layout || '-'}</dd></div>
          </dl>
        </div>
      </section>

      <section className="panel">
        <h2>Colorimetric Measurements</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Parameter</th>
                <th>Color</th>
                <th>RGB</th>
                <th>HSV</th>
                <th>Lab</th>
                <th>Estimated Result</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => {
                const final = analysis.final_results?.find((item) => item.parameter === row.parameter);
                return (
                  <tr key={row.parameter}>
                    <td>{row.parameter.replace('_', ' ')}</td>
                    <td><span className="swatch" style={{ backgroundColor: row.hex }} /> {row.hex}</td>
                    <td>{row.rgb.r}, {row.rgb.g}, {row.rgb.b}</td>
                    <td>{row.hsv.h}, {row.hsv.s}, {row.hsv.v}</td>
                    <td>{row.lab.l}, {row.lab.a}, {row.lab.b}</td>
                    <td>{final?.estimated_result || row.reference_match}</td>
                    <td>{final ? `${Math.round(final.confidence * 100)}%` : '-'}</td>
                  </tr>
                );
              })}
              {!rows.length && <tr><td colSpan="7" className="empty">Upload a demo strip image to view measurements.</td></tr>}
            </tbody>
          </table>
        </div>
      </section>

      <section className="panel">
        <h2>Previous Analyses</h2>
        <div className="history">
          {history.map((item) => (
            <article key={item.id}>
              <strong>{item.image_metadata?.filename || item.id}</strong>
              <span>{item.created_at}</span>
              <span>{item.final_results?.length || 0} results</span>
            </article>
          ))}
          {!history.length && <p className="empty">No saved analyses yet.</p>}
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
