import dynamic from 'next/dynamic';
import DualMap from '../components/Map';
const MapComponent = dynamic(() => import('../components/Map'), {
  ssr: false, // Disable server-side rendering for this component
});

export default function Home() {
  return (
    <div>
      <h1>Ban gya map</h1>
      <DualMap />
    </div>
  );
}
