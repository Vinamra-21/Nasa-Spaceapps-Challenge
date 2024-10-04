// Home.tsx
'use client';
import { useState } from 'react';
import dynamic from 'next/dynamic';
import styles from './getyourown.module.css'; // Import the CSS module

// Dynamically import the Map component (with no SSR)
const MapComponent = dynamic(() => import('../components/Map'), {
  ssr: false,
});
const Map2 = dynamic(() => import('../components/Map2'), {
  ssr: false,
});

export default function Home() {
  const [selectedComponent, setSelectedComponent] = useState<number | null>(null); // Track the selected checkbox (component)
  const [searchTerm, setSearchTerm] = useState<string>(''); // Track the search input

  // Handler for when a checkbox is clicked
  const handleCheckboxChange = (index: number) => {
    setSelectedComponent(index); // Set the selected component index
  };

  // Function to handle search submission
  const handleSearchSubmit = async (event: React.FormEvent) => {
    event.preventDefault(); // Prevent default form submission
    if (searchTerm.trim() === '') return; // Do nothing if the input is empty
  };

  // Define what components to render based on the selected checkbox
  const renderComponent = () => {
    switch (selectedComponent) {
      case 1:
        return <MapComponent />;
      case 2:
        return <Map2 searchTerm={searchTerm} />; // Pass searchTerm to Map2
      case 3:
        return <div className={styles.contentBox}><h2>Component 3</h2></div>; // Placeholder for third component
      case 4:
        return <div className={styles.contentBox}><h2>Component 4</h2></div>; // Placeholder for fourth component
      case 5:
        return <div className={styles.contentBox}><h2>Component 5</h2></div>; // Placeholder for fifth component
      default:
        return <div className={styles.contentBox}><h2>Select a checkbox to render a component</h2></div>;
    }
  };

  return (
    <div className={styles.container}>
      {/* Search bar at the top */}
      <div className={styles.searchContainer}>
        <form onSubmit={handleSearchSubmit}>
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

      {/* Left panel for checkboxes */}
      <div className={styles.leftPanel}>
        <h1 className={styles.heading}>Select a Component</h1>

        {/* Checkbox list */}
        <div className={styles.checkboxContainer}>
          {['Render Map Component', 'Render Component 2', 'Render Component 3', 'Render Component 4', 'Render Component 5'].map((label, index) => (
            <label key={index} className={styles.checkboxLabel}>
              <input
                type="checkbox"
                checked={selectedComponent === index + 1}
                onChange={() => handleCheckboxChange(index + 1)}
                className={styles.checkbox}
              />
              <span className={styles.customCheckbox}></span>
              {label}
            </label>
          ))}
        </div>
      </div>

      {/* Right panel for rendered component */}
      <div className={styles.rightPanel}>
        <div className={styles.componentContainer}>
          {renderComponent()}
        </div>
      </div>
    </div>
  );
}
