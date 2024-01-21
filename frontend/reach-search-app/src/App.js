import React, { useState, useRef, useEffect } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const inputRef = useRef(null);
  const [results, setResults] = useState({ videos: [], images: [], web: [] });
  const [isSearchComplete, setIsSearchComplete] = useState(false);

  useEffect(() => {
    if (inputRef.current) {
      const minWidth = 200;
      const newWidth = Math.max(inputRef.current.scrollWidth, minWidth);
      inputRef.current.style.width = `${newWidth}px`;
    }
  }, [query]);

  const parseWebResults = (text) => {
    const linkRegex = /\[([^\]]+)\]\((https?:\/\/[^\s]+)\)/g;
    let match;
    const links = [];
    let index = 1;
    let parsedText = text;

    while ((match = linkRegex.exec(text)) !== null) {
      const [fullMatch, linkText, linkUrl] = match;
      links.push({ linkText, linkUrl });
      parsedText = parsedText.replace(fullMatch, `<a href="${linkUrl}" target="_blank" rel="noopener noreferrer">${index}</a>`);
      index++;
    }

    return { parsedText, links };
  };

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
      if (data.web) {
        const { parsedText, links } = parseWebResults(data.web.output);
        data.web.output = parsedText;
        data.web.links = links;
      }
      setResults({
        videos: data.videos ? [data.videos.output] : [],
        images: data.images ? data.images : [], // Expecting objects with pageUrl and imageUrl
        web: data.web ? data.web : {}
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
      <form onSubmit={performSearch} className="flex justify-center items-center mb-8">
        <input
          ref={inputRef}
          type="text"
          className="border-2 border-gray-300 bg-white h-10 px-5 rounded-lg text-sm focus:outline-none"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search..."
          style={{ minWidth: '200px' }}
        />
        <button
          type="submit"
          className="text-white font-bold py-2 px-4 rounded ml-2 text-lg font-libre" // Increased font size, added margin-left and font class
          style={{ backgroundColor: '#ff7300' }} // Inline style for button color
        >
          Search
        </button>
      </form>
      {isSearchComplete && (
        <div className="flex -mx-4">
          <div className="w-1/2 px-4">
            <h2 className="text-3xl font-bold mb-4 font-libre">Web</h2> {/* Increased margin-bottom and font class */}
            <div dangerouslySetInnerHTML={{ __html: results.web.output }} className="mb-8" /> {/* Increased margin-bottom */}
            <div className="grid grid-cols-2 gap-4">
              {results.web.links && results.web.links.map((link, index) => (
                <a
                  key={index}
                  href={link.linkUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="border p-2 rounded hover:bg-gray-100"
                >
                  Source {index + 1}: {link.linkText}
                </a>
              ))}
            </div>
          </div>
          <div className="w-1/2 px-4">
            <h2 className="text-3xl font-bold mb-4 font-libre">Images</h2> {/* Increased margin-bottom and font class */}
            <div className="grid grid-cols-2 gap-4">
              {results.images.map((item, index) => (
                <div key={index} className="card mb-4"> {/* Added margin-bottom to cards */}
                  <a href={item.pageUrl} target="_blank" rel="noopener noreferrer" className="no-underline hover:no-underline">
                    <div className="border rounded overflow-hidden shadow-lg">
                      <img src={item.imageUrl} alt={`Search result ${index + 1}`} className="w-full" />
                      <div className="p-4">
                        <p className="text-gray-700 text-base">
                          {item.linkText || `Image ${index + 1}`}
                        </p>
                      </div>
                    </div>
                  </a>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;