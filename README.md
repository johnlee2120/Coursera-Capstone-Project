**Summary:**  

This project builds an end-to-end machine learning pipeline to predict whether the first stage of a Falcon 9 rocket will land successfully. The workflow includes data collection from the SpaceX API, web scraping, exploratory data analysis, feature engineering, model training, hyperparameter tuning, and dashboard development using Plotly Dash.

---

**Project Objective:**  

SpaceX reuses rocket boosters to reduce launch costs. Predicting landing success helps estimate launch economics. Built models to compare performance of Logistic Regression, SVM, Decision Trees, and KNN.

---

**Results:**  

Model Performance Comparison  


| Model                | CV Accuracy | Test Accuracy |
|----------------------|------------|--------------|
| Logistic Regression  | ~84.6%     | 83.3%        |
| SVM                  | ~84.8%     | 83.3%        |
| Decision Tree        | ~88.7%     | 83.3%        |
| KNN                  | ~84.8%     | 83.3%        |


---

**Insights:**  


Decision Tree performed best in cross validation.

All models achieved comparable test performance (~83%).

Primary errors were false positives (predicting landing when it failed).

---

**Images from project:**  


### Interactive Dashboard (Plotly Dash)
![Dashboard Screenshot](Images/plotly%20dash.png)

### Geospatial Analysis (Folium)
![Map Screenshot](Images/folium%20lab.png)

### Model Validation Accuracy
![Bar Chart](Images/model%20comparison%20bar%20graph.png)

---

**Workflow Overview:**  


1. Data Collection – SpaceX API

Collected launch data directly from the SpaceX API, extracting key variables such as flight number, payload mass, orbit type, booster version, launch site, and landing outcome. Converted raw JSON responses into structured Pandas dataframes for analysis.

2. Data Collection - Scraping

Scraped historical launch records from Wikipedia using requests and BeautifulSoup, handling HTTP headers and parsing HTML tables. Cleaned and structured scraped data to supplement API information.

3. Data Wrangling

Cleaned and prepared the dataset by handling missing values, creating the binary landing success label (Class), encoding categorical variables using one-hot encoding, and exporting structured datasets for modeling.

4. EDA with SQL

Loaded launch data into SQLite and performed exploratory queries using SQL to analyze launch sites, success rates, payload distributions, and orbit performance patterns.

5. EDA with Data Visualization

Used matplotlib and seaborn to visualize relationships between payload mass, flight number, orbit type, and landing success. Identified trends such as increasing success rates over time and orbit specific performance differences.

6. Folium

Built interactive maps using Folium to visualize launch site locations, success/failure markers, and proximity analysis. Calculated distances between launch sites and nearby geographic features (like coastline) to explore spatial factors affecting success.

7. Plotly Dash

Developed an interactive dashboard allowing dynamic filtering by launch site and payload range. Implemented callbacks to update pie charts (success distribution) and scatter plots (payload vs. outcome) in real time.

8. Predictive Analysis

Built and evaluated multiple classification models (Logistic Regression, SVM, Decision Tree, and KNN) using standardization, train/test splitting, and GridSearchCV hyperparameter tuning. Compared cross validation and test accuracy to determine the best performing model.
