'use client';
import { useEffect, useState } from 'react';

const Wetlands = ({ searchTerm }: { searchTerm: string })  => {
  const [htmlUrl, setHtmlUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [inputYear, setInputYear] = useState<string>('2016'); 


  const fetchHtmlMap = async (year: string) => {
    setLoading(true); 
    setError(null); 

    try {
      if (!/^\d{4}$/.test(year)) {
        setError('Please enter a valid year (e.g., 2020)');
        setLoading(false);
        return;
      }

      const response = await fetch(`http://127.0.0.1:5000/wetlands?date=${year}`); 
      if (response.ok) {
        const htmlBlob = await response.blob(); 
        const url = URL.createObjectURL(htmlBlob); 
        setHtmlUrl(url); 
      } else {
        setError('Failed to fetch the map HTML');
      }
    } catch (error) {
      console.error('Error fetching the map HTML:', error);
      setError('Error fetching the map HTML. Please try again.');
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
          type="text"
          value={inputYear}
          onChange={(e) => setInputYear(e.target.value)}
        />
        <button onClick={() => fetchHtmlMap(inputYear)}>Load Map</button> 
      </div>
      {loading ? (
        <p>Loading map...</p> 
      ) : error ? (
        <p>{error}</p> 
      ) : htmlUrl ? (
        <iframe
          src={htmlUrl}  
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
