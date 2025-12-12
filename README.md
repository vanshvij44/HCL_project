# Machine Learning regression analysis used for predictive analysis

## Team members

### Vansh Vij
### Atharva Patil
### Ramkishan Suthar

## Regression analysis using feature engineered features:(main.py)
 The biggest challenge we encountered using the given features predicting the tenure for which the customer will stay with the company was that the tenure target variable was showing very less correlation with the feature variables which indicates that the tenure of a customer was largely independent of the feature variables and mostly random. The R2 score for this analysis was around 0.0027
 To solve this, we engineered some other features which are related to other features but can increase the correlation with the target variable. We analyses 2 approaches
 - The engineered features which depended on the target variable itself, this lead to R2 score of 1 which meant perfect prediction but this was obviously due to data leakage and the model was "cheating".
 - The engineered features which did'nt depend on target variable and this gave us a R2 score of 0.0042,
 a slight increase.
 - The eda and the training part was similar to that of EDA.ipynb


## Classification analysis

We also tried to predict whether the customer would churn or not using ANN classification analysis. The data preprocessing was done based on the ideation file. The neural network parameters summary is as follows:
model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ layer1 (Dense)                  │ (None, 64)             │           832 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ layer2 (Dense)                  │ (None, 32)             │         2,080 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ layer3 (Dense)                  │ (None, 1)              │            33 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 2,945 (11.50 KB)
 Trainable params: 2,945 (11.50 KB)
 Non-trainable params: 0 (0.00 B)
 
 Then the model was hosted on streamlit.
![alt text](image-2.png)

