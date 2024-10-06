'use client';
import { useEffect, useState } from 'react';

const Micasa = () => {
  const [htmlUrl, setHtmlUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [inputYear, setInputYear] = useState<string>('2023');

  const fetchHtmlMap = async (year: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://127.0.0.1:5000/micasa?year=${year}`);
      if (response.ok) {
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
          // Handle JSON response (likely an error)
          const errorData = await response.json();
          setError(errorData.error || 'An unknown error occurred');
        } else {
          // Handle HTML response
          const htmlBlob = await response.blob();
          const url = URL.createObjectURL(htmlBlob);
          setHtmlUrl(url);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to fetch the map');
      }
    } catch (error) {
      console.error('Error fetching the map:', error);
      setError('An error occurred while fetching the map');
    } finally {
      setLoading(false);
    }
  };

  // Fetch the map when the inputYear changes
  useEffect(() => {
    fetchHtmlMap(inputYear);
  }, [inputYear]);

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <div>
        <label>Enter Year: </label>
        <input style={{ color: 'black' }}
          type="text"
          value={inputYear}
          onChange={(e) => setInputYear(e.target.value)}
        />
        <button onClick={() => fetchHtmlMap(inputYear)}>Load Map</button>
      </div>
      {loading ? (
        <p>Loading map...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : htmlUrl ? (
        <iframe
          src={htmlUrl}
          width="100%"
          height="100%"
          style={{ border: 'none' }}
          title="Micasa Map"
        />
      ) : null}
    </div>
  );
};

export default Micasa;
