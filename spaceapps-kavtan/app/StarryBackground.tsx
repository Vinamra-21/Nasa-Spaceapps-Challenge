import React, { useEffect } from 'react';
import './globals.css'; // Make sure to include the CSS for stars

const StarryBackground: React.FC = () => {
  useEffect(() => {
    const starCount = 100; // Number of stars
    const starryBackground = document.querySelector('.starry-background');

    for (let i = 0; i < starCount; i++) {
      const star = document.createElement('div');
      star.classList.add('star');
      star.style.top = Math.random() * 100 + 'vh';
      star.style.left = Math.random() * 100 + 'vw';
      star.style.animationDuration = Math.random() * 30 + 10 + 's';
      star.style.animationDelay = Math.random() * 50 + 's';
      if (starryBackground) {
        starryBackground.appendChild(star);
      }
    }
  }, []);

  return <div className="starry-background"></div>;
};

export default StarryBackground;
