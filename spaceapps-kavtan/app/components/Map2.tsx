// Map2.tsx
'use client';
import { useEffect, useState } from 'react';

interface Map2Props {
  searchTerm: string; // Receive the search term as a prop
}

const Map2: React.FC<Map2Props> = ({ searchTerm }) => {
  const [image, setImage] = useState<string | null>(null); // State to store the plot image

  useEffect(() => {
    const fetchPlot = async () => {
      if (searchTerm.trim() === '') return; // Do nothing if the input is empty

      try {
        const response = await fetch('http://localhost:5000/search', { // Adjust the URL to your Flask backend
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ place: searchTerm }), // Send the place name
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        if (data.image) {
          setImage(data.image); // Set the image received from the backend
        }
      } catch (error) {
        console.error('Error fetching plot:', error);
      }
    };

    fetchPlot(); // Call the fetch function when the component mounts or searchTerm changes
  }, [searchTerm]);

  return (
    <div >
      {image ? (
        <img src={`data:image/png;base64,${image}`} alt="CO2 Emission Graph" className={styles.plotImage} />
      ) : (
        <div >Loading plot...</div>
      )}
    </div>
  );
};

export default Map2;
