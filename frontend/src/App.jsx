import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  return (
    <div>
      <h1>React + Flask App</h1>
      <p>Backend says: {message}</p>
    </div>
  );
}

export default App;