"use client";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import Link from "next/link";
import { Suspense, useEffect, useState } from "react";

// Earth model component
function EarthModel() {
  const { scene } = useGLTF("/glb/earth_model.glb"); // Update the path to your GLB model
  return <primitive object={scene} scale={1.5} />; // Set initial scale
}

export default function Home() {
  const [scale, setScale] = useState(1.5); // Initial scale for the Earth model

  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      // Scale down the Earth model as you scroll down
      setScale(Math.max(0.5, 1.5 - scrollY / 200)); // Adjust values for the effect
    };

    window.addEventListener("scroll", handleScroll);
    
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] bg-gray-900 text-white">
      <header className="text-center mb-8">
        <h1 className="text-6xl sm:text-8xl font-extrabold tracking-wide">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
            GHG
          </span>
          <span> by Team Kavtan</span>
        </h1>
      </header>

      <main className="relative flex flex-col items-center justify-center">
        {/* Responsive Canvas with Earth Model */}
        <div className="earth-container relative w-full" style={{ height: '300px' }}>
          <Canvas className="absolute bottom-0 left-0 right-0">
            <Suspense fallback={null}>
              <OrbitControls enableZoom={true} />
              <EarthModel scale={scale} /> {/* Use scale state */}
            </Suspense>
          </Canvas>
        </div>

        {/* Buttons Section */}
        <div className="flex flex-col sm:flex-row gap-8 items-center justify-center mt-8">
          <Link href="/OurInsights">
            <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 shadow-lg transition-transform transform hover:scale-105">
              Our Insights
            </button>
          </Link>

          <Link href="/GetYourOwnInsights">
            <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 shadow-lg transition-transform transform hover:scale-105">
              Your Insights
            </button>
          </Link>
        </div>
      </main>

      <footer className="flex gap-6 flex-wrap items-center justify-center text-md mt-8">
        <span>Team Kavtan</span>
      </footer>
    </div>
  );
}

// Preload the GLB model
useGLTF.preload("/glb/earth_model.glb");
