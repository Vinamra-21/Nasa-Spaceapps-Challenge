# GHG Emissions Analysis Platform - NASA Space Apps Challenge 2024
## Team Kavtan

![Team Kavtan Logo](spaceapps-kavtan/public/logo2.png)

## Project Overview

This project is our submission for the NASA Space Apps Challenge 2024, focusing on greenhouse gas (GHG) emissions analysis and prediction. Our platform provides comprehensive insights into how land use patterns and population dynamics affect carbon dioxide (CO₂) and methane (CH₄) emissions, leveraging machine learning models trained on NASA satellite data and global environmental datasets.

### Mission Statement
To provide data-driven insights and predictions for greenhouse gas emissions based on land use patterns and demographic factors, enabling informed policy decisions for climate change mitigation.

## Project Architecture

The project consists of three main components:

1. **Frontend Application** (`spaceapps-kavtan/`) - Interactive Next.js web application with 3D Earth visualization
2. **Machine Learning Pipeline** (`machine learning/`) - Data processing, model training, and analysis scripts
3. **Backend Services** (`Server/`) - Flask APIs for model predictions and data analysis

## Key Features

### Interactive Web Application
- **3D Earth Visualization**: Rotating Earth model with interactive controls
- **Emissions Analysis Dashboard**: Real-time predictions and sensitivity analysis
- **Data Insights**: Comprehensive reports on land use impact on emissions
- **User-Friendly Interface**: Modern, responsive design with interactive maps

### Machine Learning Models
- **CO₂ Emissions Prediction**: Random Forest model trained on land use and population data
- **Methane Emissions Analysis**: Specialized model for CH₄ predictions
- **Sensitivity Analysis**: Understanding the impact of different factors on emissions
- **Data Processing Pipeline**: Automated data cleaning and normalization

### Data Sources
- NASA satellite data (ODIAC, MiCASA)
- EDGAR emissions database
- World Bank population data
- Global land use datasets

## Quick Start

### Prerequisites
- Node.js (v18 or higher)
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vinamra-21/Nasa-Spaceapps-Challenge.git
   cd Nasa-Spaceapps-Challenge
   ```

2. **Set up the Frontend**
   ```bash
   cd spaceapps-kavtan
   npm install
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

3. **Set up the Backend**
   ```bash
   cd ../Server/App2
   pip install flask pandas joblib google-generativeai flask-cors python-dotenv
   python app.py
   ```
   The API will be available at `http://localhost:5001`

4. **Environment Variables**
   Create a `.env` file in `Server/App2/` with:
   ```
   API_KEY=your_google_ai_api_key
   ```

### Usage

1. **Access the Web Application**: Navigate to `http://localhost:3000`
2. **Explore Insights**: Click "Our Insights" to view pre-analyzed data
3. **Get Custom Predictions**: Click "Your Insights" to input custom land use data
4. **View Analysis**: Get detailed sensitivity analysis and policy recommendations

## Project Structure

```
Nasa-Spaceapps-Challenge/
├── spaceapps-kavtan/              # Next.js Frontend Application
│   ├── app/                       # App router pages and components
│   │   ├── page.tsx              # Main landing page with 3D Earth
│   │   ├── OurInsights/          # Pre-analyzed insights dashboard
│   │   ├── GetYourOwnInsights/   # Custom prediction interface
│   │   ├── carbonemission/       # CO₂ emission analysis
│   │   ├── methaneemission/      # CH₄ emission analysis
│   │   └── components/           # Reusable React components
│   ├── public/                   # Static assets (models, images)
│   └── package.json              # Dependencies and scripts
│
├── machine learning/             # ML Pipeline and Data Processing
│   ├── *.py                     # Various data processing scripts
│   ├── *.csv                    # Processed datasets
│   ├── *.joblib                 # Trained ML models
│   └── *.xlsx                   # Raw data files
│
├── Server/                      # Backend Services
│   ├── App1/                    # Visualization service
│   ├── App2/                    # Main prediction API
│   │   └── app.py              # Flask application
│   └── App3/                    # Additional services
│
└── README.md                    # This file
```

## Technical Details

### Machine Learning Models

#### CO₂ Emissions Model
- **Algorithm**: Random Forest Regression
- **Features**: Crop land, grazing land, forest land, fishing ground, built-up land, population
- **Target**: Net carbon emissions (g CO₂/m²/yr)
- **Normalization**: Z-score standardization for all features

#### Methane Emissions Model
- **Algorithm**: Random Forest Regression
- **Features**: Land use categories and population density
- **Target**: Methane emissions (tonnes/year)
- **Validation**: Cross-validation with R² > 0.93

### Frontend Technologies
- **Next.js 14**: React framework with App Router
- **Three.js**: 3D graphics and Earth visualization
- **React Three Fiber**: React renderer for Three.js
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe JavaScript

### Backend Technologies
- **Flask**: Python web framework
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms
- **Joblib**: Model serialization
- **Google AI**: Generative AI for insights

## Data Pipeline

1. **Data Collection**: NASA satellite data, emissions databases, population data
2. **Preprocessing**: Data cleaning, normalization, country code matching
3. **Feature Engineering**: Land use categorization, population density calculation
4. **Model Training**: Random Forest with hyperparameter optimization
5. **Validation**: Cross-validation and sensitivity analysis
6. **Deployment**: Model serialization and API integration

## Key Insights

Our analysis reveals:
- **Forest land** has the strongest negative correlation with emissions (carbon sink effect)
- **Built-up land** and **population density** are primary emission drivers
- **Agricultural practices** significantly impact regional emission patterns
- **Policy interventions** in land use can achieve 15-30% emission reductions

## Development

### Running Tests
```bash
# Frontend tests
cd spaceapps-kavtan
npm test

# Backend tests
cd Server/App2
python -m pytest
```

### Building for Production
```bash
# Frontend build
cd spaceapps-kavtan
npm run build

# Backend deployment
cd Server/App2
gunicorn -w 4 app:app
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Data Acknowledgments

- **NASA**: ODIAC and MiCASA datasets
- **EDGAR**: Emissions Database for Global Atmospheric Research
- **World Bank**: Population and development indicators
- **Global Land Cover**: FAO and ESA datasets

## Team Kavtan

- **Data Scientists**: ML model development and validation
- **Full-Stack Developers**: Web application and API development
- **Environmental Analysts**: Domain expertise and policy insights
- **UI/UX Designers**: User experience and visualization design

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **GitHub Repository**: https://github.com/Vinamra-21/Nasa-Spaceapps-Challenge
- **Live Demo**: [Coming Soon]
- **NASA Space Apps Challenge**: https://spaceappschallenge.org/

## Acknowledgments

Special thanks to NASA Space Apps Challenge organizers, our mentors, and the open-source community for making this project possible.

---

**Built with care by Team Kavtan for NASA Space Apps Challenge 2024** 
