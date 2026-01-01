import React from 'react'
import ReactDOM from 'react-dom/client'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
            <h1>Dashboard Connected</h1>
            <p>Backend URL: http://localhost:8000</p>
        </div>
    </React.StrictMode>,
)
