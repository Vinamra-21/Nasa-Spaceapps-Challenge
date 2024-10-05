'use client'
import { useEffect, useState } from 'react';

const DualMap = () => {
  const [htmlContent, setHtmlContent] = useState<string | null>(null);

  useEffect(() => {
    // Fetch the dual_map.html from the Flask server
    const fetchHtmlMap = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/map2'); // Flask URL serving the HTML
        const htmlText = await response.text();
        setHtmlContent(htmlText);  // Save the HTML content in the state
      } catch (error) {
        console.error('Error fetching the map HTML:', error);
      }
    };

    fetchHtmlMap();
  }, []);

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <iframe
        src="/dual_map_odiac.html"  // This serves the dual_map.html file from the public folder
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
    </div>
  );
};

export default DualMap;
