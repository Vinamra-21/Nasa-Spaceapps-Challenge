'use client';
import { useEffect, useState } from 'react';

const DualMap = () => {
  const [htmlUrl, setHtmlUrl] = useState<string | null>(null); // To store the full URL to the HTML file
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const [error, setError] = useState<boolean>(false); // Error state
  const [inputYear, setInputYear] = useState<string>('2016'); // Default year

  // Function to fetch the HTML map
  const fetchHtmlMap = async (year: string) => {
    setLoading(true); // Start loading
    setError(false); // Reset error state

    try {
      const response = await fetch(`http://127.0.0.1:5000/co2?year=${year}`); // Add year as a query parameter
      if (response.ok) {
        const htmlBlob = await response.blob(); // Receive the HTML file as a blob
        const url = URL.createObjectURL(htmlBlob); // Create a URL object to use in iframe
        setHtmlUrl(url); // Set the iframe source to the blob URL
      } else {
        console.error('Failed to fetch the map HTML');
        setError(true); // Set error state
      }
    } catch (error) {
      console.error('Error fetching the map HTML:', error);
      setError(true); // Set error state
    } finally {
      setLoading(false); // Stop loading
    }
  };

  // Fetch map whenever the year changes
  useEffect(() => {
    fetchHtmlMap(inputYear); // Fetch map with the current input year
  }, [inputYear]);

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <div>
        <label>Enter Year: </label>
        <input
          type="text"
          value={inputYear}
          onChange={(e) => setInputYear(e.target.value)} // Update year based on input
        />
        <button onClick={() => fetchHtmlMap(inputYear)}>Load Map</button> {/* Manually trigger map load */}
      </div>
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
