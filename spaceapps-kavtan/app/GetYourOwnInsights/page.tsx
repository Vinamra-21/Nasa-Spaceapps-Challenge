'use client';

import { useState } from 'react';
import axios from 'axios'; // For making HTTP requests
import dynamic from 'next/dynamic';
import styles from './getyourown.module.css'; // Import the CSS module
import Image from 'next/image';

// Dynamically import components without SSR
const MapComponent = dynamic(() => import('../components/Map'), { ssr: true });
const Map2 = dynamic(() => import('../components/Map2'), { ssr: false });

export default function Home() {
  // States for search and modal
  const [searchTerm, setSearchTerm] = useState<string>(''); // Track search input
  const [searchResult, setSearchResult] = useState<string | null>(null); // State to store the search result
  const [isModalOpen, setModalOpen] = useState<boolean>(false); // State for modal

  // Separate states for left and right panel components
  const [selectedLeftComponent, setSelectedLeftComponent] = useState<number | null>(null);
  const [selectedRightComponent, setSelectedRightComponent] = useState<number | null>(null);

  // Function to handle search submission
  const handleSearchSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    // console.log('searchTerm:', searchTerm);
    if (searchTerm.trim() === '') return;
    try {
        const response = await axios.post('http://127.0.0.1:5000/search', {
            place: searchTerm,
        });
        console.log('1')
        console.log(searchTerm)
        const { image_url, message } = response.data; // Destructure image_url

        if (image_url) {
            setSearchResult(image_url); // Set the image URL
            console.log(searchResult);
            setModalOpen(true); // Open modal when search result is received
        } else {
            setSearchResult('No data found.');
        }

        console.log(message);
    } catch (error) {
        console.error('Error fetching search results:', error);
        setSearchResult('An error occurred while searching.');
    }
};

  // Define what components to render based on the selected radio button in left panel
  const renderLeftComponent = () => {
    switch (selectedLeftComponent) {
      case 1:
        return <MapComponent />;
      case 2:
        return <Map2 />;
      case 3:
        return <div className={styles.contentBox}><h2>Component 3</h2></div>;
      case 4:
        return <div className={styles.contentBox}><h2>Component 4</h2></div>;
      case 5:
        return <div className={styles.contentBox}><h2>Component 5</h2></div>;
      default:
        return <div className={styles.contentBox}><h2>Select a component to render</h2></div>;
    }
  };

  // Define what components to render based on the selected radio button in right panel
  const renderRightComponent = () => {
    switch (selectedRightComponent) {
      case 1:
        return <MapComponent />;
      case 2:
        return <Map2 />;
      case 3:
        return <div className={styles.contentBox}><h2>Component 3</h2></div>;
      case 4:
        return <div className={styles.contentBox}><h2>Component 4</h2></div>;
      case 5:
        return <div className={styles.contentBox}><h2>Component 5</h2></div>;
      default:
        return <div className={styles.contentBox}><h2>Select a component to render</h2></div>;
    }
  };

  return (
    <div className={styles.container}>
      {/* Full-width search bar */}
      <div className={styles.searchContainer}>
        <form onSubmit={handleSearchSubmit} className={styles.fullWidthForm}>
          <input
            type="text"
            placeholder="Enter a place name"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className={styles.searchInput}
          />
          <button type="submit" className={styles.searchButton}>Search</button>
        </form>
      </div>

      {/* Container for panels */}
      <div className={styles.panelContainer}>
        {/* Left panel for radio buttons */}
        <div className={styles.leftPanel}>
          <h1 className={styles.heading}>Select a Component (Left)</h1>
          <div className={styles.radioContainer}>
            {['Render Map Component', 'Render Component 2', 'Render Component 3', 'Render Component 4', 'Render Component 5'].map((label, index) => (
              <label key={index} className={styles.radioLabel}>
                <input
                  type="radio"
                  checked={selectedLeftComponent === index + 1}
                  onChange={() => setSelectedLeftComponent(index + 1)}
                  className={styles.radio}
                />
                <span className={styles.customRadio}></span>
                {label}
              </label>
            ))}
          </div>
          <div className={styles.componentContainer}>
            {renderLeftComponent()}
          </div>
        </div>

        {/* Right panel for independent selection and rendering */}
        <div className={styles.rightPanel}>
          <h1 className={styles.heading}>Select a Component (Right)</h1>
          <div className={styles.radioContainer}>
            {['Render Map Component', 'Render Component 2', 'Render Component 3', 'Render Component 4', 'Render Component 5'].map((label, index) => (
              <label key={index} className={styles.radioLabel}>
                <input
                  type="radio"
                  checked={selectedRightComponent === index + 1} // Unique index for right panel
                  onChange={() => setSelectedRightComponent(index + 1)} // Unique index for right panel
                  className={styles.radio}
                />
                <span className={styles.customRadio}></span>
                {label}
              </label>
            ))}
          </div>
          <div className={styles.componentContainer}>
            {renderRightComponent()} {/* Render based on right panel selection */}
          </div>
        </div>
      </div>

      {/* Modal to display search results */}
      {isModalOpen && (
        <div className={styles.modal}>
            <div className={styles.modalContent}>
                <button className={styles.closeButton} onClick={() => setModalOpen(false)}>
                    &times;
                </button>
                {searchResult ? (
                    <Image src={searchResult} // Use the image URL directly
                    alt="CO2 Emission Graph"
                    className={styles.resultImage}
                />
                
                
                ) : (
                    <p>No search result available.</p>
                )}
            </div>
        </div>
    )}

    </div>
  );
}
