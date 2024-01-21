import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState({ videos: [], images: [], web: [] });
  const [isSearchComplete, setIsSearchComplete] = useState(false);

  const performSearch = (event) => {
    event.preventDefault();
    setIsSearchComplete(false);
    fetch('http://localhost:5000/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt: query })
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      setResults({
        videos: data.videos ? [data.videos.output] : [],
        images: data.images ? [data.images.output] : [],
        web: data.web ? [data.web.output] : []
      });
      setIsSearchComplete(true);
    })
    .catch(error => {
      console.error('Error:', error);
      setIsSearchComplete(false);
    });
  };

  return (
    <div className="container mx-auto p-4">
      <form onSubmit={performSearch} className="flex justify-center items-center mb-4">
        <input
          type="text"
          className="border-2 border-gray-300 bg-white h-10 px-5 pr-16 rounded-lg text-sm focus:outline-none"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search..."
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Search
        </button>
      </form>
      {isSearchComplete && (
        <div>
          {/* Uncomment and update the following sections as needed when you have data to display */}
          {/* <h2 className="text-xl font-bold">Videos</h2>
          <ul>
            {results.videos.map((videoOutput, index) => (
              <li key={index}>{videoOutput}</li>
            ))}
          </ul> */}
          <h2 className="text-xl font-bold">Images</h2>
          <ul>
            {results.images.map((imageOutput, index) => (
              <li key={index}>{imageOutput}</li>
            ))}
          </ul>
          <h2 className="text-xl font-bold">Web</h2>
          <p>{results.web.length > 0 ? results.web[0] : "No web results"}</p>
        </div>
      )}
    </div>
  );
}

export default App;

