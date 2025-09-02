# ML Model

## The Model we will be using is feature-engineering + classical ML: Use handcrafted statistics (e.g., summary stats + embeddings) and train something like Random Forest, XGBoost or Logistic Regression for classification.

## Feature engineering is the process of using domain knowledge to create new input variables, called features,  from raaw data to improve the performance of machine learning model . The right features can enable a simpler model to outperform a  more momplex one, making it a critical step in the machine learning workflow.

# Why feature engineering is important 

# Improves model accuracy: well-engineered features provide a model with mode relevant information, allowing it to better capture the underlying patterns in the data
# Reduced overfitting: By selecting only the most  important features and removing irrelevant and noisy ones, feature enginerring can create simpler more robust models 
# Handles complex data: Some raw dat types, like text or images, need to be converted into numerical features  before they can be used in models

# Common feature engineering techniques 

## Handling missing values: Inputing (or filling in) missing data suing strategies like the mean, median or  a sophisticated model
## Encoding categorical data: Converting non-numerical data (e.g., color: red, green, blue) into a  numerical format that an algorithm can understand, such as one-hot encoding 
## Creating new features: Deriving new  information from existing features, like calculating Total_Area from length and width, or extracting the day_of_week from a Timestamp.
## Feature scaling: Normalizing or standardizing numerical features so they have similar scale, which is crucial for some algorithms.

# Random Forest
## A random forest is an ensemble learning method that works by constructing a multitude of decision trees to produce a single, more accurate, and more stable prediction 

# How it is used for classification

## Bootstrapping: The algorithm creates multiple subsets of the original training data by randomly samping from it with replacement. This means some data points may appear multiple times in a single subset, while others may not appear at all.
## Random feature selection: When growing each individual decision tree, the algorithm considers only a random susbet of the total features to make the best split at each node. This ensures the trees are not too similar to one another
## Majority voting: To classify a new data point, every decision tree in the forrest casts a 'vote' for a class. The random forest's final prediction is the class that recieves the majority of votes

# XGBoost (eXtreme Gradient Boosting)
## XGBoost is a highly efficient and scalable implementation of the gradient boosting framework. Unlike Random Forest's "bagging" approach, which builds trees independently , XGBoost's "boosting" approach builds trees sequentially, where each new tree is trained to correct errors of the previous ones.

# How it is used for classification
# 1. Initial prediciton: XGBoost starts with a simple initial prediction, often the average of the target  variable.
# 2. Sequential tree building: It builds the next tree  to predict the residuals (the errors) of the previous tree. The model is continuously refined to minimize a predefined loss function 
# 3. Weighted contribution: The final prediction is a weighted sum of the predictions from all the  individual trees. XGBoost uses regularizattion techniques to prevent overfitting during this process
# 4. Final profitability: For classification, XGBoost predicts a log-odds value that is converted into final probability using a logistic funtion


# Logistic Regression
## Despite its name, Logistic Regression is a classification is a classification algorithm, not a regression algorithm. It is a simple, yet powerful , statisticalmethod used to predict a categorical outcome based one one or more independent variable

## How it's used for classification
## The  logistic fucntion: Logistic regression uses the logistic function to output the probability value that is bounded between 0 and  1, regardless of the input values.
## Linear equation: The algorithm takes a linear combination of the input features and maps this result into the sigmoid function
## Decision Boundary: A threshold is set to convert the output probability into a discrete class. For example, if the calculated porbability is greater  than 0.5, the model predicts class "1"; otherise, it predicts class "0"
## Interpretabel coefficients: The coefficients (B) in the logistic regression indicate the strength and direction of the relationship between each independent variable and the log-odds of the dependent variable.
