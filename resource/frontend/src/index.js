import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

document.addEventListener("DOMContentLoaded", function(event) {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById('root')
  );  
})