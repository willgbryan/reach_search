import React, { useState, useRef, useEffect } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const inputRef = useRef(null);
  const [results, setResults] = useState({ videos: [], images: [], web: [] });
  const [isSearchComplete, setIsSearchComplete] = useState(false);

  const handleFileChange = (event) => {
    if (event.target.files.length) {
      const formData = new FormData();
      for (const file of event.target.files) {
        formData.append('files', file);
      }

      fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data.message);
        // You can set state here if you want to show a message or update the UI
      })
      .catch(error => {
        console.error('Error:', error);
        // Handle errors here, such as updating the UI to show an error message
      });
    }
  };

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
        web: data.web ? data.web : {},
        pdf: data.pdf || ""
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
        <input
      type="file"
      webkitdirectory="true"
      directory="true"
      multiple
      onChange={handleFileChange}
      className=" h-10 px-5 rounded-lg text-sm focus:outline-none my-2"
      />
      </form>
      {isSearchComplete && (
      <div className="flex flex-wrap -mx-4">
        {/* Left column for Web and PDF results */}
        <div className="w-full lg:w-1/2 px-4">
          {/* Web results */}
          <div className="mb-8"> {/* Existing margin-bottom */}
            <h2 className="text-3xl font-bold mb-4 font-libre">Web</h2>
            {/* need to change how the web output is rendered */}
            <div dangerouslySetInnerHTML={{ __html: results.web.output }} />
            <div className="grid grid-cols-2 gap-4 mb-16"> {/* Increased margin-bottom */}
              {results.web.links && results.web.links.map((link, index) => (
                <a key={index} href={link.linkUrl} target="_blank" rel="noopener noreferrer" className="border p-2 rounded hover:bg-gray-100">
                  Source {index + 1}: {link.linkText}
                </a>
              ))}
            </div>
          </div>
          {/* PDF results */}
          {typeof results.pdf === 'string' && results.pdf && (
            <div>
              <h2 className="text-3xl font-bold mb-4 font-libre">PDF Search Results</h2>
              <div className="border p-2 rounded hover:bg-gray-100">
                {results.pdf}
              </div>
            </div>
          )}
        </div>
        {/* Right column for Image results */}
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