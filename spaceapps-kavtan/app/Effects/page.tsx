import React from 'react';
import styles from './effects.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Climate Change Impacts: A Policy Brief</h1>
      <h2 className={styles.subtitle}>Executive Summary</h2>
      <p className={styles.paragraph}>
        Climate change poses significant risks to national security, economic stability, and public health. This brief outlines key impacts and their policy implications, providing a foundation for informed decision-making and strategic planning.
      </p>

      <h2 className={styles.subtitle}>1. Economic Implications</h2>
      <h3 className={styles.subsection}>1.1 GDP Impact</h3>
      <ul className={styles.list}>
        <li>Projected 10-23% reduction in global GDP by 2100 under high-emission scenarios (IPCC, 2022).</li>
        <li>Disproportionate impact on developing economies, potentially widening global inequalities.</li>
      </ul>

      <h3 className={styles.subsection}>1.2 Sectoral Vulnerabilities</h3>
      <ul className={styles.list}>
        <li>Agriculture: Potential 3-10% decrease in crop yields per decade (FAO, 2021).</li>
        <li>Infrastructure: Estimated $100 trillion in damages by 2050 without adaptation measures (World Bank, 2020).</li>
        <li>Energy: Up to 25% decrease in power generation efficiency in water-stressed regions (IEA, 2021).</li>
      </ul>

      <h3 className={styles.subsection}>1.3 Financial Market Risks</h3>
      <ul className={styles.list}>
        <li>Stranded assets in fossil fuel industries, estimated at $1-4 trillion (Carbon Tracker, 2021).</li>
        <li>Increased insurance premiums and potential market instability due to climate-related events.</li>
      </ul>

      <h2 className={styles.subtitle}>2. National Security Concerns</h2>
      <h3 className={styles.subsection}>2.1 Resource Scarcity</h3>
      <ul className={styles.list}>
        <li>Water stress affecting 52% of the world's population by 2050 (UN Water, 2021).</li>
        <li>Potential for resource-driven conflicts, particularly in water-stressed regions.</li>
      </ul>

      <h3 className={styles.subsection}>2.2 Forced Migration</h3>
      <ul className={styles.list}>
        <li>Projected 200 million climate migrants by 2050 (World Bank, 2021).</li>
        <li>Strain on urban infrastructure and potential for social unrest.</li>
      </ul>

      <h3 className={styles.subsection}>2.3 Geopolitical Instability</h3>
      <ul className={styles.list}>
        <li>Changing Arctic accessibility altering global trade routes and resource competition.</li>
        <li>Increased vulnerability of military installations to sea-level rise and extreme weather.</li>
      </ul>

      <h2 className={styles.subtitle}>3. Public Health Challenges</h2>
      <h3 className={styles.subsection}>3.1 Direct Health Impacts</h3>
      <ul className={styles.list}>
        <li>Heat-related mortality projected to increase by 50-100% in most regions by 2050 (WHO, 2021).</li>
        <li>Expansion of vector-borne diseases, potentially affecting 1 billion more people by 2080.</li>
      </ul>

      <h3 className={styles.subsection}>3.2 Food and Water Security</h3>
      <ul className={styles.list}>
        <li>540-590 million people at risk of undernourishment by 2050 due to climate change (FAO, 2020).</li>
        <li>40% of global population projected to live in severe water-stressed areas by 2050.</li>
      </ul>

      <h3 className={styles.subsection}>3.3 Air Quality</h3>
      <ul className={styles.list}>
        <li>Ground-level ozone pollution could cause 260,000 premature deaths annually by 2100 (UNEP, 2022).</li>
      </ul>

      <h2 className={styles.subtitle}>4. Environmental and Biodiversity Impacts</h2>
      <h3 className={styles.subsection}>4.1 Ecosystem Disruption</h3>
      <ul className={styles.list}>
        <li>20-30% of species at increased risk of extinction with 1.5°C warming (IPBES, 2021).</li>
        <li>Potential collapse of key ecosystems (e.g., coral reefs) with cascading economic impacts.</li>
      </ul>

      <h3 className={styles.subsection}>4.2 Sea Level Rise</h3>
      <ul className={styles.list}>
        <li>Projected 0.6-1.1m rise by 2100 under high-emission scenarios (IPCC, 2021).</li>
        <li>$14 trillion in annual coastal damage costs by 2100 without adaptation (Nature, 2020).</li>
      </ul>

      <h2 className={styles.subtitle}>5. Policy Recommendations</h2>
      <h3 className={styles.subsection}>5.1 Mitigation Strategies</h3>
      <ul className={styles.list}>
        <li>Accelerate transition to renewable energy, aiming for 70-85% renewables in electricity generation by 2050.</li>
        <li>Implement carbon pricing mechanisms, targeting $50-100/tCO2e by 2030.</li>
        <li>Enhance natural carbon sinks through reforestation and improved land management.</li>
      </ul>

      <h3 className={styles.subsection}>5.2 Adaptation Measures</h3>
      <ul className={styles.list}>
        <li>Develop national adaptation plans focusing on vulnerable sectors and regions.</li>
        <li>Invest in climate-resilient infrastructure, particularly in urban and coastal areas.</li>
        <li>Strengthen early warning systems and disaster preparedness protocols.</li>
      </ul>

      <h3 className={styles.subsection}>5.3 International Cooperation</h3>
      <ul className={styles.list}>
        <li>Enhance climate finance commitments, aiming to meet and exceed the $100 billion annual target.</li>
        <li>Strengthen international frameworks for climate migrants and resource-sharing agreements.</li>
        <li>Support technology transfer and capacity building in developing nations.</li>
      </ul>

      <h3 className={styles.subsection}>5.4 Research and Innovation</h3>
      <ul className={styles.list}>
        <li>Increase R&D funding for climate solutions, targeting 1% of GDP by 2030.</li>
        <li>Promote public-private partnerships in clean technology development.</li>
        <li>Establish national climate risk assessment frameworks to inform policy decisions.</li>
      </ul>

      <h2 className={styles.subtitle}>Conclusion</h2>
      <p className={styles.paragraph}>
        The impacts of climate change are far-reaching and interconnected, posing significant challenges to governance, economic stability, and social welfare. Immediate, coordinated action across all levels of government is essential to mitigate risks and build resilience. This brief underscores the urgency of implementing comprehensive climate policies that address both mitigation and adaptation, ensuring a sustainable and secure future for our nation and the global community.
      </p>

      <div className={styles.footer}>
        <p>&copy; 2024 Climate Change Policy Brief</p>
      </div>
    </div>
  );
}
