'use client';
import { useEffect, useState } from 'react';

const Wetlands = () => {
  const [htmlUrl, setHtmlUrl] = useState<string | null>(null); // To store the full URL to the HTML file
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const [error, setError] = useState<string | null>(null); // Error message state
  const [inputYear, setInputYear] = useState<string>('2016'); // Default year

  // Function to fetch the HTML map
  const fetchHtmlMap = async (year: string) => {
    setLoading(true); // Start loading
    setError(null); // Reset error state

    try {
      // Validate year input
      if (!/^\d{4}$/.test(year)) {
        setError('Please enter a valid year (e.g., 2020)');
        setLoading(false);
        return;
      }

      const response = await fetch(`http://127.0.0.1:5000/wetlands?date=${year}`); // Correct query param to 'date'
      if (response.ok) {
        const htmlBlob = await response.blob(); // Receive the HTML file as a blob
        const url = URL.createObjectURL(htmlBlob); // Create a URL object to use in iframe
        setHtmlUrl(url); // Set the iframe source to the blob URL
      } else {
        setError('Failed to fetch the map HTML');
      }
    } catch (error) {
      console.error('Error fetching the map HTML:', error);
      setError('Error fetching the map HTML. Please try again.');
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
        <p>{error}</p> // Display error message
      ) : htmlUrl ? (
        <iframe
          src={htmlUrl}  // Set the iframe src to the blob URL
          width="100%"
          height="100%"
          style={{
            border: 'none',
          }}
          title="Wetlands"
        />
      ) : null}
    </div>
  );
};

export default Wetlands;
