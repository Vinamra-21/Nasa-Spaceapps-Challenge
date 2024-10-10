'use client';
import { useEffect, useState } from 'react';

const CO2 = ({ searchTerm }: { searchTerm: string })  => {
  const [htmlUrl, setHtmlUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<boolean>(false);
  const [inputYear, setInputYear] = useState<string>('2016'); 


  const fetchHtmlMap = async (year: string) => {
    setLoading(true);
    setError(false);

    try {
      const response = await fetch(`http://127.0.0.1:5000/co2?year=${year}`); 
      if (response.ok) {
        const htmlBlob = await response.blob();
        const url = URL.createObjectURL(htmlBlob);
        setHtmlUrl(url);
      } else {
        setError(true);
      }
    } catch (error) {
      console.error('Error fetching the map HTML:', error);
      setError(true);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    fetchHtmlMap(searchTerm); 
  }, [inputYear]);

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <div>
        <label>Enter Year: </label>
        <input
          style={{ color: 'black' }}
          type="text"
          value={inputYear}
          onChange={(e) => setInputYear(e.target.value)}
        />
        <button onClick={() => fetchHtmlMap(inputYear)}>Load Map</button>
      </div>
      {loading ? (
        <p>Loading map...</p>
      ) : error ? (
        <p>Failed to load map. Please try again later.</p>
      ) : htmlUrl ? (
        <iframe
          src={htmlUrl}
          width="100%"
          height="100%"
          style={{ border: 'none' }}
          title="CO2"
        />
      ) : null}
    </div>
  );
};

export default CO2;
