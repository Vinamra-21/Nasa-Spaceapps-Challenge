"use client";

import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, useGLTF, Stars } from "@react-three/drei";
import Link from "next/link";
import { Suspense, useEffect, useState, useRef } from "react";
import StarryBackground from "./StarryBackground";
import "./globals.css";

function EarthModel({ scale }) {
  const earthRef = useRef();
  const { scene } = useGLTF("/glb/earth_model.glb");

  useFrame((_, delta) => {
    if (earthRef.current) {
      earthRef.current.rotation.y += delta * 0.05;
    }
  });

  return (
    <primitive
      ref={earthRef}
      object={scene}
      scale={scale * 0.5}
      position={[0, 0, 0]}
    />
  );
}

function CameraAdjuster() {
  const { camera } = useThree();

  useEffect(() => {
    camera.position.set(0, 0, -400);
    camera.fov = 30;
    camera.updateProjectionMatrix();
  }, [camera]);

  return null;
}

export default function Home() {
  const [scale, setScale] = useState(0.5);

  useEffect(() => {
    const handleScroll = () => {
      setScale(Math.max(0.5, 1 - window.scrollY / 1000));
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <div className="relative">
      <StarryBackground />
      <div className="flex flex-col items-center justify-center min-h-screen p-8 gap-16 sm:p-20 text-white">
        {/* Header */}
        <header className="text-center">
          <img src="/logo2.png" alt="Team Kavtan Logo" className="h-12" />
          <h1 className="text-6xl sm:text-8xl font-extrabold tracking-wide">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
              GHG
            </span>
            <span> by Team Kavtan</span>
          </h1>
        </header>

        {/* Main Section */}
        <main className="relative flex flex-col items-center justify-center w-full">
          <div className="earth-container w-full sm:h-[80vh]">
            <Canvas>
              <Suspense fallback={null}>
                <CameraAdjuster />
                <ambientLight intensity={5.5} />
                <pointLight position={[10, 10, 100]} intensity={5.5} />
                <OrbitControls enableZoom={true} />
                <EarthModel scale={scale} />
                <Stars
                  radius={200}
                  depth={100}
                  count={8000}
                  factor={7}
                  fade
                  speed={0.5}
                />
              </Suspense>
            </Canvas>
          </div>

          {/* Buttons */}
          <div className="flex flex-col sm:flex-row gap-8 items-center justify-center mt-8">
            <Link href="/OurInsights">
              <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 shadow-lg transform hover:scale-105 transition-transform">
                Our Insights
              </button>
            </Link>
            <Link href="/GetYourOwnInsights">
              <button className="text-white font-bold py-4 px-8 rounded-lg text-xl bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 shadow-lg transform hover:scale-105 transition-transform">
                Your Insights
              </button>
            </Link>
          </div>
        </main>

        {/* Footer */}
        <footer className="flex gap-6 flex-wrap items-center justify-center text-md mt-8 p-4">
          <span>Team Kavtan</span>
          <img
            src="/logo2.png"
            alt="Team Kavtan Logo"
            className="h-10 w-auto"
          />
          <nav>
            <ul className="flex gap-4">
              <li>
                <a
                  href="https://github.com/Vinamra-21/Nasa-Spaceapps-Challenge"
                  className="text-blue-500">
                  GitHub
                </a>
              </li>
            </ul>
          </nav>
        </footer>
      </div>
    </div>
  );
}

// Preload the GLB model
useGLTF.preload("/glb/earth_model.glb");
