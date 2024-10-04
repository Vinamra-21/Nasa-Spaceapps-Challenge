import dynamic from 'next/dynamic';
const MapComponent = dynamic(() => import('../components/Map'), {
  ssr: false, // Disable server-side rendering for this component
});

export default function Home() {
  return (
    <div>
      <h1>Interactive Map with Leaflet.js</h1>
      <MapComponent />
    </div>
  );
}
