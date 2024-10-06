"use client";

import Image from "next/image";
import styles from "./analysis.module.css"; // Assuming you're using a CSS module for styling

export default function AnalysisPage() {
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Analysis of CO2 and Methane Emission Prediction Models</h1>

      <section className={styles.section}>
        <h2 className={styles.subheading}>Introduction</h2>
        <p className={styles.paragraph}>
          Recent studies on greenhouse gas emissions have revealed distinct patterns in the factors
          influencing CO2 and methane emissions. This document analyzes the feature importance
          graphs for both gases, highlighting key differences and their implications for climate
          change mitigation strategies.
        </p>
      </section>

      <section className={styles.section}>
        <h2 className={styles.subheading}>Key Observations</h2>

        <h3 className={styles.observation}>1. Land Use: Crucial for Both, but with Different Emphases</h3>
        <p className={styles.paragraph}>
          CO2 emissions are significantly influenced by forest land, while methane emissions are primarily
          affected by crop land. This difference stems from the unique properties and sources of each gas:
        </p>
        <ul className={styles.list}>
          <li>
            <strong>Forest Land and CO2:</strong> Forests act as carbon sinks, absorbing CO2 from the
            atmosphere. Deforestation not only releases stored carbon but also reduces the Earth's capacity to
            absorb CO2. The high importance of forest land in CO2 predictions underscores the critical role
            of forest conservation in climate change mitigation.
          </li>
          <li>
            <strong>Crop Land and Methane:</strong> Agricultural activities, particularly rice cultivation
            and livestock farming, are major sources of methane. Crop lands often involve practices like
            flooding (in rice paddies) and the use of fertilizers, which create anaerobic conditions favorable
            for methane-producing bacteria. The dominance of crop land in methane predictions highlights the
            need for sustainable agricultural practices to reduce emissions.
          </li>
        </ul>
        <Image
          src="/image/carbon.jpg"
          alt="CO2 Feature Importance Graph"
          width={600}
          height={400}
          className={styles.image}
        />

        <h3 className={styles.observation}>2. Population: Strong Influence on CO2, Not a Top Factor for Methane</h3>
        <p className={styles.paragraph}>
          Population emerges as the most significant predictor for CO2 emissions but doesn't appear among
          the top factors for methane. This disparity can be explained by:
        </p>
        <ul className={styles.list}>
          <li>
            <strong>CO2 and Human Activities:</strong> Population growth directly correlates with increased
            energy consumption, industrial production, and transportation – all major sources of CO2 emissions.
            More people generally means more fossil fuel consumption for electricity, heating, and transportation.
          </li>
          <li>
            <strong>Methane and Specific Practices:</strong> Methane emissions are more closely tied to
            specific industrial and agricultural practices rather than general population levels. While
            population growth may indirectly increase demand for methane-producing activities, the relationship
            is not as direct as with CO2.
          </li>
        </ul>

        <h3 className={styles.observation}>3. Methane Emissions: Influenced by Specific Industrial and Agricultural Practices</h3>
        <p className={styles.paragraph}>
          The methane prediction model shows high importance for factors like metal industry, manure management,
          and civil aviation. This specificity reflects the nature of methane sources:
        </p>
        <ul className={styles.list}>
          <li>
            <strong>Industrial Processes:</strong> Certain industries, particularly those involving fossil fuel
            extraction and processing, are significant methane emitters. The metal industry, for instance,
            often involves coking coal, which releases methane.
          </li>
          <li>
            <strong>Agricultural Practices:</strong> Manure management in livestock farming is a major source
            of methane. The anaerobic decomposition of organic matter in manure produces significant amounts of
            this potent greenhouse gas.
          </li>
          <li>
            <strong>Specialized Sectors:</strong> The inclusion of civil aviation suggests that certain
            transportation sectors may have distinct methane emission profiles, possibly related to fuel types
            or combustion processes.
          </li>
        </ul>
        <Image
          src="/image/methane.jpg"
          alt="Methane Feature Importance Graph"
          width={600}
          height={400}
          className={styles.image}
        />

        <h3 className={styles.observation}>4. CO2 Prediction: Reliance on Broader Land Use Categories</h3>
        <p className={styles.paragraph}>
          The CO2 model features broader categories like forest land, crop land, and built-up land. This generalization
          reflects the pervasive nature of CO2 emissions:
        </p>
        <ul className={styles.list}>
          <li>
            <strong>Diverse Sources:</strong> CO2 is produced by a wide range of human activities, from energy
            production to transportation and industrial processes. Broader land use categories serve as proxies
            for these diverse emission sources.
          </li>
          <li>
            <strong>Long-term Carbon Cycle:</strong> The inclusion of various land types acknowledges the role of
            natural carbon sinks and sources in the global carbon cycle, which is crucial for understanding long-term
            CO2 trends.
          </li>
        </ul>
      </section>

      <section className={styles.section}>
        <h2 className={styles.subheading}>Conclusion</h2>
        <p className={styles.paragraph}>
          The distinct feature importance profiles for CO2 and methane emissions underscore the complexity of greenhouse gas
          dynamics. Effective climate change mitigation strategies must account for these differences, targeting specific
          practices for methane reduction while addressing broader systemic issues for CO2 mitigation. This nuanced understanding
          is crucial for developing comprehensive and effective policies to combat climate change.
        </p>
      </section>
    </div>
  );
}
