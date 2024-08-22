import React from 'react';
import './LandingPage.css';

function LandingPage() {
  return (
    <div className="landing-container">
      <div className="content">
        <h1>Universal Ricin Detection Model</h1>
        <p>If you want to test whether a food product contains ricin or not, choose if you’d like to manually put in the data or upload a csv file.</p>
        <div className="buttons">
          <button className="btn">MANUALLY ENTER</button>
          <button className="btn">UPLOAD FILE</button>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
