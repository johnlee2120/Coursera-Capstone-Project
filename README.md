**Summary:**  

This project builds an end-to-end machine learning pipeline to predict whether the first stage of a Falcon 9 rocket will land successfully. The workflow includes data collection from the SpaceX API, web scraping, exploratory data analysis, feature engineering, model training, hyperparameter tuning, and dashboard development using Plotly Dash.

---

**Project Objective:**  

SpaceX reuses rocket boosters to reduce launch costs. Predicting landing success helps estimate launch economics. Built models to compare performance of Logistic Regression, SVM, Decision Trees, and KNN.

---

**Results:**  


Results Section (Very Important)

Summarize final model comparison:

Model	CV Accuracy	Test Accuracy
Logistic Regression	~84.6%	83.3%
SVM	~84.8%	83.3%
Decision Tree	~88.7%	83.3%
KNN	~84.8%	83.3%

---

**Insights:**  


Decision Tree performed best in cross-validation.

All models achieved comparable test performance (~83%).

Primary errors were false positives (predicting landing when it failed).

---

**Workflow Overview:**  


1. Data Collection – SpaceX API

Collected launch records directly from the SpaceX API. Extracted payload mass, launch site, orbit, booster version, and landing outcome.

2. Web Scraping – Wikipedia

Scraped historical Falcon 9 launch records using BeautifulSoup. Cleaned and structured raw HTML tables into a usable dataset.

3. Data Wrangling

Handled missing values, encoded categorical features, and created the binary target variable (Class).

4. Exploratory Data Analysis

Visualized relationships between:

- Flight number vs success

- Payload mass vs orbit

- Launch site vs landing outcome

- Yearly success trends

Identified increasing landing success rates over time.

5. Feature Engineering

Applied one-hot encoding to categorical variables and standardized numerical features.

6. Machine Learning Modeling

Split data into training/testing sets and trained:

- Logistic Regression

- Support Vector Machine

- Decision Tree

- K-Nearest Neighbors

Used GridSearchCV (10-fold CV) for hyperparameter tuning.

7. Model Evaluation

Compared models using:

- Test accuracy

- Confusion matrices

- Cross-validation performance

Decision Tree achieved the highest validation accuracy (~88%).

8. Interactive Dashboard

Built a Plotly Dash dashboard allowing users to:

- Filter by launch site

- Adjust payload range

- Visualize success rates interactively

