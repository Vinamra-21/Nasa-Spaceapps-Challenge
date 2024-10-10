'use client';

import { useState } from 'react';
import axios from 'axios';
import dynamic from 'next/dynamic';
import styles from './getyourown.module.css';
import Image from 'next/image';

const CO2 = dynamic(() => import('../components/CO2'), { ssr: true });
const Micasa = dynamic(() => import('../components/Micasa'), { ssr: false });
const Odiac = dynamic(() => import('../components/Odiac'), { ssr: true });
const Wetlands = dynamic(() => import('../components/Wetlands'), { ssr: false });

export default function Home() {
  const [leftSearchTerm, setLeftSearchTerm] = useState<string>(''); 
  const [leftSearchResult, setLeftSearchResult] = useState<string | null>(null);
  const [isLeftModalOpen, setLeftModalOpen] = useState<boolean>(false);

  const [rightSearchTerm, setRightSearchTerm] = useState<string>(''); 
  const [rightSearchResult, setRightSearchResult] = useState<string | null>(null);
  const [isRightModalOpen, setRightModalOpen] = useState<boolean>(false);

  const [selectedLeftComponent, setSelectedLeftComponent] = useState<number | null>(null);
  const [selectedRightComponent, setSelectedRightComponent] = useState<number | null>(null);

  const handleLeftSearchSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (leftSearchTerm.trim() === '') {
      setLeftSearchResult('Please enter a place name.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/search', {
        place: leftSearchTerm,
      });
      const { image_url, message } = response.data;
      if (image_url) {
        setLeftSearchResult(image_url);
        setLeftModalOpen(true); 
      } else {
        setLeftSearchResult('No data found.');
      }
      console.log(message);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setLeftSearchResult('An error occurred while searching.');
    }
  };

  const handleRightSearchSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (rightSearchTerm.trim() === '') {
      setRightSearchResult('Please enter a place name.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/search', {
        place: rightSearchTerm,
      });
      const { image_url, message } = response.data;
      if (image_url) {
        setRightSearchResult(image_url);
        setRightModalOpen(true);
      } else {
        setRightSearchResult('No data found.');
      }
      console.log(message);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setRightSearchResult('An error occurred while searching.');
    }
  };

  const renderLeftComponent = () => {
    switch (selectedLeftComponent) {
      case 1:
        return <CO2 searchTerm={leftSearchTerm} />;
      case 2:
        return <Micasa searchTerm={leftSearchTerm} />;
      case 3:
        return <Odiac searchTerm={leftSearchTerm} />;
      case 4:
        return <Wetlands searchTerm={leftSearchTerm} />;
      default:
        return <div className={styles.contentBox}><h2>Select a component to render</h2></div>;
    }
  };

  const renderRightComponent = () => {
    switch (selectedRightComponent) {
      case 1:
        return <CO2 searchTerm={rightSearchTerm} />;
      case 2:
        return <Micasa searchTerm={rightSearchTerm} />;
      case 3:
        return <Odiac searchTerm={rightSearchTerm} />;
      case 4:
        return <Wetlands searchTerm={rightSearchTerm} />;
      default:
        return <div className={styles.contentBox}><h2>Select a component to render</h2></div>;
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.panelContainer}>
        <div className={styles.leftPanel}>
          <h1 className={styles.heading}>Left Panel Search</h1>
          <form onSubmit={handleLeftSearchSubmit} className={styles.fullWidthForm}>
            <input
              type="text"
              placeholder="Enter a place name"
              value={leftSearchTerm}
              onChange={(e) => setLeftSearchTerm(e.target.value)}
              className={styles.searchInput}
            />
            <button type="submit" className={styles.searchButton}>Search</button>
          </form>

          <div className={styles.radioContainer}>
            {['CO2', 'Micasa', 'Odiac', 'Wetlands'].map((label, index) => (
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

        <div className={styles.rightPanel}>
          <h1 className={styles.heading}>Right Panel Search</h1>
          <form onSubmit={handleRightSearchSubmit} className={styles.fullWidthForm}>
            <input
              type="text"
              placeholder="Enter a place name"
              value={rightSearchTerm}
              onChange={(e) => setRightSearchTerm(e.target.value)}
              className={styles.searchInput}
            />
            <button type="submit" className={styles.searchButton}>Search</button>
          </form>

          <div className={styles.radioContainer}>
            {['CO2', 'Micasa', 'Odiac', 'Wetlands'].map((label, index) => (
              <label key={index} className={styles.radioLabel}>
                <input
                  type="radio"
                  checked={selectedRightComponent === index + 1}
                  onChange={() => setSelectedRightComponent(index + 1)}
                  className={styles.radio}
                />
                <span className={styles.customRadio}></span>
                {label}
              </label>
            ))}
          </div>
          <div className={styles.componentContainer}>
            {renderRightComponent()} 
          </div>
        </div>
      </div>

      {isLeftModalOpen && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <button className={styles.closeButton} onClick={() => setLeftModalOpen(false)}>
              &times;
            </button>
            {leftSearchResult ? (
              <Image
                src="/mapnew.png"
                width={500}
                height={500}
                alt="Left Search Result"
                className={styles.resultImage}
              />
            ) : (
              <p>No search result available.</p>
            )}
          </div>
        </div>
      )}

      {isRightModalOpen && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <button className={styles.closeButton} onClick={() => setRightModalOpen(false)}>
              &times;
            </button>
            {rightSearchResult ? (
              <Image
                src={rightSearchResult}
                width={300}
                height={300}
                alt="Right Search Result"
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
