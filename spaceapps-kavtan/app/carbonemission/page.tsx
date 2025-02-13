"use client";
import styles from "./carbonEmission.module.css";
import { useState, ChangeEvent, FormEvent } from "react";

export default function Home() {
  const [inputs, setInputs] = useState({
    cropLand: 0,
    grazingLand: 0,
    forestLand: 0,
    fishingGround: 0,
    builtupLand: 0,
    population: 0,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: Number(value),
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputs),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.h1}>Carbon Emissions Predictor</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="number"
          name="cropLand"
          placeholder="Crop Land Area"
          onChange={handleChange}
          required
          className={styles.input}
        />
        <input
          type="number"
          name="grazingLand"
          placeholder="Grazing Land Area"
          onChange={handleChange}
          required
          className={styles.input}
        />
        <input
          type="number"
          name="forestLand"
          placeholder="Forest Land Area"
          onChange={handleChange}
          required
          className={styles.input}
        />
        <input
          type="number"
          name="fishingGround"
          placeholder="Fishing Ground Area"
          onChange={handleChange}
          required
          className={styles.input}
        />
        <input
          type="number"
          name="builtupLand"
          placeholder="Built-up Land Area"
          onChange={handleChange}
          required
          className={styles.input}
        />
        <input
          type="number"
          name="population"
          placeholder="Population"
          onChange={handleChange}
          required
          className={styles.input}
        />
        <button type="submit" disabled={loading} className={styles.button}>
          {loading ? "Loading..." : "Predict Emissions"}
        </button>
      </form>

      {result && (
        <div className={styles.result}>
          <h2 className={styles.h2}>Sensitivity Analysis Results:</h2>
          <pre className={styles.pre}>
            {Object.entries(result).map(([key, val]) => (
              <div key={key}>
                <strong>{key}:</strong> {val}
              </div>
            ))}
          </pre>
        </div>
      )}
    </div>
  );
}
