# HCL_project

## Team members

### Vansh Vij
### Atharva Patil
### Ramkishan Suthar

### EDA and Regression 
Data cleaning and preprocessing
Univariate and bivariate analysis
Correlation and feature relationship studies
Creation of engineered features
Regression and classification model development
Model evaluation and interpretation

1. Data Quality
No missing values after removing invalid CustomerID entries
No duplicate rows
Features separated into numerical and categorical groups for analysis
2. Variable Distributions
Age, Usage Frequency, Support Calls, and Payment Delay show smooth unimodal distributions

Tenure appears uniformly distributed without strong patterns
Churn is imbalanced, with more non-churners than churners

3. Correlation Analysis
Most features have very weak correlation with Tenure
Behavioral factors such as Support Calls, Payment Delay, and Total Spend show stronger relevance to Churn
The correlation heatmap confirms limited linear relationships for regression tasks
Classification (Predicting Churn) displays clearer feature influence than regression (Predicting Tenure)

4. Feature Engineering
The following engineered variables were created to enhance modeling:
Engagement Score
Usage Frequency + Total Spend – Payment Delay – Support Calls

Risk Score
Payment Delay + Support Calls – Last Interaction

Spend Per Month
Total Spend / Contract Length

Encoded categorical variables for Subscription Type, Contract Type, and Gender

These features improved churn prediction but did not significantly improve tenure prediction due to the weak underlying relationships.

5. Graph Analysis
   Graph Explanations from EDA
      1. KDE Plot of Age
      
      What it shows:
      A Kernel Density Estimate (KDE) plot visualizing the distribution of customer ages.
      
      Interpretation:
      
      The distribution appears smooth and unimodal.
      
      Most customers fall in the middle-age range (around 30–50).
      
      Very few customers are extremely young or extremely old.
      
      Why it matters:
      Helps understand the age demographics of customers and check whether age is balanced or skewed.
      
      2. Churn Value Counts (Bar Plot)
      
      What it shows:
      A simple bar chart showing the number of churned vs non-churned customers.
      
      Interpretation:
      
      Non-churners significantly outnumber churners.
      
      The dataset is imbalanced, which affects classification performance and requires careful model evaluation.
      
      Why it matters:
      Imbalanced datasets need techniques like class weighting or resampling for fair modeling.
      
      3. Gender vs Churn (Grouped Bar Chart)
      
      What it shows:
      A bar graph comparing how many males and females churned or did not churn.
      
      Interpretation:
      
      Churn count is roughly similar between genders.
      
      No strong pattern indicates that gender is not a dominant predictor of churn.
      
      Why it matters:
      Helps check whether churn behavior differs across genders.
      
      4. Multiple KDE Plots for Numerical Columns
      
      Columns plotted include:
      
      Age
      
      Usage Frequency
      
      Support Calls
      
      Payment Delay
      
      Total Spend
      
      Last Interaction
      
      Interpretation:
      
      Most numerical features show unimodal smooth distributions.
      
      Some features like Support Calls & Payment Delay have long tails, showing varied customer behavior.
      
      None show strong visual relationship with Tenure.
      
      Why it matters:
      Helps detect skewness, outliers, and the general behavior of numeric variables.
      
      5. Correlation Heatmap
      
      What it shows:
      A heatmap showing correlation values between all numerical features and the target variables.
      
      Interpretation:
      
      Tenure has extremely weak correlations (between –0.03 and +0.07) with almost every feature.
      
      Features like Support Calls, Payment Delay, and Engagement Score show stronger correlations with Churn, not Tenure.
      
      Very few linear relationships exist overall.
      
      Why it matters:
      This explains why regression models for Tenure performed poorly (low R² score).
      
      6. KDE Plots of Numerical Columns Against Churn
      
      Example:
      
      Age vs Churn
      
      Usage Frequency vs Churn
      
      Support Calls vs Churn
      
      Interpretation:
      
      KDE curves for churned vs non-churned customers show visible separation for some features.
      
      This indicates some features behave differently for churners, improving classification models.
      
      Why it matters:
      Confirms that the dataset is more suitable for churn prediction than tenure estimation.
      
      7. Box Plots for Numerical Columns
      
      Plotted for:
      
      Age
      
      Usage Frequency
      
      Support Calls
      
      Interpretation:
      
      Helps identify outliers and spread.
      
      Support Calls has visible outliers (customers with exceptionally high call counts).
      
      Variability in Usage Frequency suggests different usage patterns across customers.
      
      Why it matters:
      Outliers can influence models; understanding spread is key for preprocessing.
      
      8. KDE Plot of Engagement Score
      
      What it shows:
      Distribution of the engineered Engagement Score.
      
      Interpretation:
      
      The score ranges widely, centered around moderate values.

Outliers on both negative and positive sides show high variability in engagement.

Why it matters:
Checks if the engineered feature has meaningful variation for prediction.

9. KDE Plot of Risk Score

What it shows:
Distribution of the engineered Risk Score.

Interpretation:

Strong right skew due to high Payment Delay + Support Calls for some customers.

Many customers have low or moderate risk.

Why it matters:
Helps in identifying high-risk behavioral patterns related to churn.

10. Subscription Type vs Churn (Bar Plot)

What it shows:
Comparison of churn rates across subscription types (Basic, Standard, Premium, etc.).

Interpretation:

Certain subscription categories may have higher churn.

Shows customer dissatisfaction differences between plans.

Why it matters:
Guides business actions such as improving weaker subscription plans.

Reason for the Low R² Score in Tenure Prediction

The regression models produced a low R² score, and this is consistent with EDA findings:

1. Weak Correlation Between Features and Tenure

The correlations between numerical features and Tenure ranged roughly between –0.03 and +0.07.
Such weak relationships limit any model’s ability to explain variance in Tenure.

2. Features Are More Predictive of Churn Than Tenure

Behavioral attributes (e.g., support calls, delays, spending patterns) influence customer dissatisfaction and churn, not how long they have already stayed.
Thus the dataset is naturally structured for classification, not regression.

3. Missing Important Factors for Tenure

Tenure typically depends on information not present in the dataset, such as:

Customer start date

Offer history

Service lifecycle stage

Retention interventions

The absence of these variables restricts model performance.

4. High Noise in Inputs

Behavioral features show high variance without a direct linear trend with Tenure, further lowering predictive accuracy.

Conclusion:
The dataset provides meaningful signals for churn classification, but insufficient information to accurately model tenure, resulting in a low R² score.

