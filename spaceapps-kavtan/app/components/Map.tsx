'use client';
import { useEffect, useState } from 'react';

const DualMap = () => {
  const [htmlUrl, setHtmlUrl] = useState<string | null>(null); // To store the full URL to the HTML file
  const [loading, setLoading] = useState<boolean>(true); // Loading state
  const [error, setError] = useState<boolean>(false); // Error state

  useEffect(() => {
    const fetchHtmlMap = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/co2'); // Flask endpoint serving the HTML file
        if (response.ok) {
          const htmlBlob = await response.blob(); // Receive the HTML file as a blob
          const url = URL.createObjectURL(htmlBlob); // Create a URL object to use in iframe
          setHtmlUrl(url); // Set the iframe source to the blob URL
          setLoading(false); // HTML is ready, stop loading
        } else {
          console.error('Failed to fetch the map HTML');
          setError(true); // Set error state
          setLoading(false); // Stop loading
        }
      } catch (error) {
        console.error('Error fetching the map HTML:', error);
        setError(true); // Set error state
        setLoading(false); // Stop loading even if there is an error
      }
    };

    fetchHtmlMap();
  }, []);

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      {loading ? (
        <p>Loading map...</p> // Display a loading message while fetching
      ) : error ? (
        <p>Failed to load map. Please try again later.</p> // Handle errors
      ) : htmlUrl ? (
        <iframe
          src={htmlUrl}  // Set the iframe src to the blob URL
          width="100%"
          height="100%"
          style={{
            border: 'none',
          }}
          title="Dual Map"
        />
      ) : null}
    </div>
  );
};

export default DualMap;
