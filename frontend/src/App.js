import React, { useState } from 'react';
import './App.css';

function App() {
  const [movementType, setMovementType] = useState('Circle');
  const [size, setSize] = useState(100);
  const [duration, setDuration] = useState(5);
  const [steps, setSteps] = useState(100);
  const [status, setStatus] = useState('Ready');

  const handleStart = async () => {
    setStatus('Starting movement...');
    try {
      const response = await fetch('http://localhost:5000/start-movement', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movementType, size, duration, steps })
      });
      const data = await response.json();
      if (response.ok) {
        setStatus(data.status);
      } else {
        setStatus(`Error: ${data.status}`);
      }
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    }
  };

  const handleStop = async () => {
    setStatus('Stopping movement...');
    try {
      const response = await fetch('http://localhost:5000/stop-movement', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      if (response.ok) {
        setStatus(data.status);
      } else {
        setStatus(`Error: ${data.status}`);
      }
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <h1>Cursor Movement Controller</h1>
      <div className="form-group">
        <label>Movement Pattern:</label>
        <select value={movementType} onChange={e => setMovementType(e.target.value)}>
          <option value="Circle">Circle</option>
          <option value="Figure Eight">Figure Eight</option>
          <option value="Spiral">Spiral</option>
          <option value="Square">Square</option>
          <option value="Zigzag">Zigzag</option>
        </select>
      </div>
      <div className="form-group">
        <label>Size:</label>
        <input
          type="number"
          value={size}
          onChange={e => setSize(parseInt(e.target.value))}
        />
      </div>
      <div className="form-group">
        <label>Duration (sec):</label>
        <input
          type="number"
          value={duration}
          onChange={e => setDuration(parseInt(e.target.value))}
        />
      </div>
      <div className="form-group">
        <label>Smoothness (steps):</label>
        <input
          type="number"
          value={steps}
          onChange={e => setSteps(parseInt(e.target.value))}
        />
      </div>
      <div className="button-group">
        <button onClick={handleStart}>Start Movement</button>
        <button onClick={handleStop}>Stop Movement</button>
      </div>
      <div className="status">
        <p>Status: {status}</p>
      </div>
      <p className="note">Note: Ensure the Python backend is running on http://localhost:5000</p>
    </div>
  );
}

export default App;