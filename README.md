# Focus on Vision: A Statistical Study of Eye

Welcome to **Focus on Vision**, a comprehensive data-driven project that investigates the factors influencing eye health and the need for vision correction in our increasingly digital world. This project, titled "Focus on Vision: A Statistical Study of Eye," explores how demographics, screen usage, environmental conditions, and genetic history contribute to vision problems. Using statistical analysis and machine learning, we predict the likelihood of needing vision correction and provide an interactive web application, **ClarityCare**, for personalized risk assessment.

With the rise of digital screen time—phones, laptops, tablets—vision issues like eye strain, blurred vision, and myopia are becoming more prevalent, especially among young people. The World Health Organization estimates over 2.2 billion people suffer from vision impairments, many linked to lifestyle factors. This project aims to uncover these connections and empower users to take proactive steps toward better eye health.

---

## Objectives

The primary goals of this study are:

- **Data Exploration**: Visualize and analyze data across domains like demographics, screen usage, environmental factors, and genetic history using interactive dashboards.
- **Hypothesis Testing**: Investigate relationships between variables (e.g., screen time and vision problems) with statistical methods.
- **Data Preprocessing**: Clean and prepare data for modeling by handling missing values, encoding features, and addressing class imbalance.
- **Feature Selection**: Identify key predictors of vision correction needs using stepwise logistic regression with L1 regularization.
- **Model Development**: Train and evaluate logistic regression and neural network models to predict vision correction probability.
- **Application Deployment**: Deliver a user-friendly Streamlit app, ClarityCare, for real-time risk assessment.

---

## Dataset

The dataset is a rich collection of variables related to eye health, gathered from diverse sources. It includes:

- **Demographics**: Age, gender, occupation, education level.
- **Screen Usage**: Daily screen time, device preferences (e.g., smartphones, laptops), dark mode usage.
- **Environmental Factors**: Lighting conditions, outdoor activity hours, air quality (via AQI mapping).
- **Genetic History**: Family vision problems (parents, relatives), age of onset.
- **Behavioral Factors**: Sleep duration, reading hours, exercise frequency.

### Preprocessing Steps
- **Column Renaming**: Standardized names for clarity.
- **Missing Values**: Imputed numerical data with medians, categorical data with modes.
- **Feature Engineering**: Created `has_or_had_glasses` from vision history and eye power data.
- **Cleaning**: Dropped irrelevant features (e.g., `air_quality` temporarily), corrected errors, removed outliers.
- **Standardization**: Ensured consistent data types and scaled numerical features.

---

## Methodology

The project follows a structured approach to analyze and model the data:

1. **Normality Testing**
   - Tools: Shapiro-Wilk, Kolmogorov-Smirnov, Anderson-Darling tests, Q-Q plots.
   - Finding: All variables were non-normal (p < 0.05), justifying non-parametric methods.

2. **Data Exploration**
   - Created dashboards to visualize:
     - Demographics (e.g., age distribution, gender split).
     - Screen usage patterns by age, gender, and occupation.
     - Symptoms (e.g., eye strain, fatigue) and their prevalence.
     - Environmental and genetic influences.

3. **Hypothesis Testing**
   - **Spearman’s Rank Correlation**: Examined monotonic relationships (e.g., strong positive correlation between left and right eye power, ρ = 0.848).
   - **Chi-Square Tests**: Confirmed significant associations (e.g., age and eye problems, p < 0.001).

4. **Data Transformation**
   - **Encoding**: Label-encoded categorical variables (e.g., occupation, lighting conditions).
   - **Scaling**: Applied Min-Max normalization to numerical features.
   - **Class Imbalance**: Used SMOTE to balance the target variable `has_or_had_glasses` (from 93.18% majority to 50-50 split).

5. **Feature Selection**
   - Method: Stepwise logistic regression with L1 (Lasso) regularization.
   - Outcome: Selected 11 key predictors (e.g., age, screen hours, reading hours).

6. **Model Building**
   - Trained logistic regression and neural network models (details below).

---
## Power BI Dashboard

Empower stakeholders and collaborators to interactively explore the data, validate model findings, and uncover deeper patterns through rich, self-service visual analytics.
1. **Overview**
  - **Page 01** - ![01](https://github.com/user-attachments/assets/d609b58a-3d96-47df-95b5-df72f8525cef)
  - **Page 02** -![02](https://github.com/user-attachments/assets/c8dfa269-eaed-4a5b-8626-3d11a408d988)
  - **Page 03** -![03](https://github.com/user-attachments/assets/e428efbf-f177-4ea4-82dc-3e14c3072374)
  - **Page 04** -![04](https://github.com/user-attachments/assets/86420d47-8c46-421d-b606-3256f30ac5db)
  - **Page 05** -![05](https://github.com/user-attachments/assets/c3700a29-e884-4699-ae13-0149cd9308f0)
  - **Page 06** -![06](https://github.com/user-attachments/assets/abb797fa-e094-4e58-bd88-4b39a950d0a0)
  - **Page 07** -![07](https://github.com/user-attachments/assets/c25c9f8c-0276-4c64-9c86-3d9b020ad38e)


2. **Dashboard Features**
   - **Demographics**: Age, gender, occupation, education distributions.  
   - **Screen Usage**: Breakdown of daily screen hours by age group, device, and purpose.  
   - **Environmental & Lifestyle**: Visualize lighting conditions, outdoor activity, sleep patterns, and AQI.  
   - **Genetic History**: Compare parental and relative vision issues with current symptoms.  
   - **Risk Factors**: Interactive slicers to see how key predictors (e.g., reading_hours, dark_usage) impact predicted risk levels.  


---
## Models

Two predictive models were developed to assess vision correction needs:

### 1. Logistic Regression
- **Purpose**: Predict the probability of needing vision correction.
- **Performance**:
  - Pseudo R²: 0.7210 (72.1% variability explained).
  - Log-Likelihood Ratio (LLR) p-value: < 0.001 (significant fit).
- **Key Predictors**:
  - Reading hours (70.1% contribution).
  - Dark usage (9.27%), age (5.93%), sleep hours (4.98%).
- **Significance**: All predictors had p-values < 0.05.

### 2. Neural Network Classifier
- **Architecture**:
  - Layers: 128-64-32 neurons with ReLU activation.
  - Regularization: Batch normalization, dropout (rate = 0.3).
  - Output: 1 neuron with sigmoid activation.
- **Training**:
  - Optimizer: Adam (learning rate = 0.0005).
  - Loss: Binary cross-entropy with label smoothing (0.1).
  - Epochs: 100 with early stopping.
- **Performance**:
  - Accuracy: 86.93%.
  - AUC: 0.6335 (good class separation).
  - Log Loss: 0.4961 (well-calibrated probabilities).

---

## Web Application: ClarityCare

**ClarityCare** is a Streamlit-based web app that makes the project accessible to users:
-**Application Walkthrough**: 
   https://github.com/user-attachments/assets/dbae20f5-5044-4451-a944-4f52f1365bf9

- **How It Works**:
  - Users answer 10 questions about their lifestyle (e.g., screen time, sleep hours).
  - Inputs are encoded, scaled, and fed into the logistic regression model.
  - Outputs a risk category (e.g., "Low Risk") with personalized tips.

- **Features**:
  - Conversational chat interface.
  - Real-time prediction with confidence scores.
  - Disclaimer: Not a substitute for medical advice.

- **Running the App**:
  1. Install dependencies.
  2. Run: `streamlit run app.py`.
  3. Follow the prompts in your browser.

---

## Results and Insights

Key findings from the analysis:

- **Screen Time**: High usage, especially among youth (18-24) and students, strongly correlates with vision symptoms.
- **Contributing Factors**: Poor lighting, limited outdoor activity, short sleep, and genetic predisposition increase risk.
- **Mitigation**: Regular eye care, better lighting, and reduced screen time can lower symptoms.

---

## Future Work

Potential enhancements include:

- **Intergenerational Prediction**: Model the risk of passing vision issues to offspring.
- **Longitudinal Studies**: Track vision progression over time with survival analysis.
- **Genomic Integration**: Add polygenic risk scores and biomarkers for richer insights.
- **Real-Time Monitoring**: Incorporate smartphone tests and wearable data into ClarityCare.
- **Clinical Validation**: Test the tool in real-world settings like clinics and schools.

---

## Installation and Usage

To run this project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Utkarshmishra2k2/Focus_on_Vision-A_Statistical_Study_of_Eye
   cd Focus_on_Vision-A_Statistical_Study_of_Eye
