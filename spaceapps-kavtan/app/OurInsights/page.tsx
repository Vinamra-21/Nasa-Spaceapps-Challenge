import Link from "next/link";
import styles from './ourinsights.module.css'; 

export default function Home() {
  return (
    <div className={styles.container}>
      <Link href="/CarbonEmission">
        <button className={styles.button}>
          Carbon Emission Model
        </button>
      </Link>
      <Link href="/MethaneEmission">
        <button className={styles.button}>
          Methane Emission Model
        </button>
      </Link>
      <Link href="/Factors">
        <button className={styles.button}>
          Factors Affecting GHG Emission
        </button>
      </Link>
      <Link href="/Effects">
        <button className={styles.button}>
          Effects of Climate Change
        </button>
      </Link>
    </div>
  );
}
