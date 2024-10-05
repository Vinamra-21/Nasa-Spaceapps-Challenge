'use client'
import { useEffect, useState } from 'react';

const DualMap = () => {
  const [htmlPath, setHtmlPath] = useState<string | null>(null); // To store the path to the HTML file
  const [loading, setLoading] = useState<boolean>(true); // Loading state

  useEffect(() => {
    // Fetch the HTML path from the Flask server
    const fetchHtmlMap = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/micasa'); // Flask endpoint to generate and return the HTML file path
        if (response.ok) {
          const data = await response.json(); // Assuming Flask sends a JSON response
          setHtmlPath(data.file_path); // Update with the path to the generated HTML
          setLoading(false); // HTML is ready, stop loading
        } else {
          console.error('Failed to fetch the map HTML');
        }
      } catch (error) {
        console.error('Error fetching the map HTML:', error);
        setLoading(false); // Stop loading even if there is an error
      }
    };

    fetchHtmlMap();
  }, []);

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      {loading ? (
        <p>Loading map...</p> // Display a loading message while fetching
      ) : htmlPath ? (
        <iframe
          src={`http://127.0.0.1:5000${htmlPath}`}  // Dynamically set the iframe src to the returned HTML file path
          width="80%"
          height="80%"
          style={{ 
            width: '100%', 
            height: '90%', 
            border: 'none', 
            display: 'block',
            paddingTop: '10%',
          }}
          title="Dual Map"
        />
      ) : (
        <p>Failed to load map. Please try again later.</p> // Handle the case when the HTML path is null
      )}
    </div>
  );
};

export default DualMap;
