
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def starplugs():
#  pip install mlxtend pandas openpyxl
#  pip install pandas scikit-learn openpyxl matplotlib
  print("**********************************************************")
  print("Welcome to use starplugs *: a star data analytics solution")
  print("Starplugs is your star solution for seamless data analysis. With Starplugs, you can easily 'plug' in different functions tailored for various data analysis needs—empowering you to unlock insights faster and more efficiently. Whether you're handling large datasets or running complex analyses, Starplugs is here to simplify your workflow and enhance your results.")
  print()
  print("Get ready to power up your data journey with Starplugs!")
  print("**********************************************************")
  print()
  print("Contacts:")
  print()
  print("Dr Anna Sung - email: a.sung@chester.ac.uk")
  print("Prof Kelvin Leong - email: k.leong@chester.ac.uk")
  print()
  print("subpackages: arule01, arule, cluster, dtree, test")
  # print()
  # print()
  print("**********************************************************")

#SUBPACKAGE: arule01---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: association tree will be created for data input as 0 1 format
#***********************************************************************************************************
def arule01():
  import pandas as pd
  from mlxtend.frequent_patterns import apriori, association_rules
  from google.colab import files

  # Allow the user to upload the file
  uploaded = files.upload()

  # Assume only one file is uploaded, get the file name
  file_name = list(uploaded.keys())[0]

  # Load the dataset from the uploaded file
  df = pd.read_excel(file_name)

  # Display the dataset
  print("Dataset:")
  print(df)

  # Remove 'Transaction' column if it exists
  if 'Transaction' in df.columns:
      df = df.drop(columns=['Transaction'])

  # Prompt the user to input the minimum support value
  while True:
      try:
          min_support = float(input("Please enter the minimum support value (less than 1):\n "))
          if min_support <= 0 or min_support >= 1:
              raise ValueError("The value must be between 0 and 1 (exclusive).")
          break
      except ValueError as e:
          print(e)

  # Perform Apriori algorithm to find frequent itemsets
  frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

  # Display the frequent itemsets
  print("\nFrequent Itemsets:")
  print(frequent_itemsets)

  # Generate the association rules
  rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

  # Display the association rules
  print("\nAssociation Rules:")
  print(rules)

#SUBPACKAGE: arule---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: association tree will be created for data input as text (e.g. milk, chips, cake)
#***********************************************************************************************************
def arule():
  import pandas as pd
  from mlxtend.frequent_patterns import apriori, association_rules
  from google.colab import files

  # Allow the user to upload the file
  uploaded = files.upload()

  # Assume only one file is uploaded, get the file name
  file_name = list(uploaded.keys())[0]

  # Load the dataset from the uploaded file
  df = pd.read_excel(file_name)

  # Display the dataset
  print("Original Dataset:")
  print(df)

  # Split the items into lists and create a one-hot encoded DataFrame
  df['Items'] = df['Items'].str.split(', ')

  # One-hot encode the items
  df_onehot = df['Items'].str.join('|').str.get_dummies()

  # Display the one-hot encoded DataFrame
  print("\nOne-Hot Encoded Dataset:")
  print(df_onehot)

  # Prompt the user to input the minimum support value
  while True:
      try:
          min_support = float(input("Please enter the minimum support value (less than 1):\n "))
          if min_support <= 0 or min_support >= 1:
              raise ValueError("The value must be between 0 and 1 (exclusive).")
          break
      except ValueError as e:
          print(e)

  # Perform Apriori algorithm to find frequent itemsets
  frequent_itemsets = apriori(df_onehot, min_support=min_support, use_colnames=True)

  # Display the frequent itemsets
  print("\nFrequent Itemsets:")
  print(frequent_itemsets)

  # Generate the association rules
  rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

  # Display the association rules
  print("\nAssociation Rules:")
  print(rules)

#SUBPACKAGE: cluster---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct clustering analysis
#***********************************************************************************************************
def cluster():
  # Import necessary libraries
  import pandas as pd
  from sklearn.cluster import KMeans
  from sklearn.preprocessing import StandardScaler, OneHotEncoder
  from sklearn.compose import ColumnTransformer
  from sklearn.pipeline import Pipeline
  import matplotlib.pyplot as plt
  from google.colab import files

  # Step 1: Upload the Excel file
  print("Please upload your Excel file:")
  uploaded = files.upload()

  # Step 2: Load the Excel file into a Pandas DataFrame
  df = pd.read_excel(list(uploaded.keys())[0])

  # Display the first few rows of the dataset
  print("\nHere is a preview of your dataset:")
  print(df.head())

  # Step 3: Allow users to choose the number of clusters
  print("\nHow many clusters would you like to create?")
  num_clusters = int(input("> "))  # User input on the next line

  # Step 4: Allow users to select columns for clustering
  print("\nAvailable columns in the dataset:")
  print(df.columns)
  print("\nEnter the column names to use for clustering (separated by commas):")
  columns = input("> ").split(',')  # User input on the next line

  # Step 5: Prepare the selected data for clustering
  selected_data = df[columns]

  # Step 6: Identify categorical and continuous columns
  categorical_cols = selected_data.select_dtypes(include=['object', 'category']).columns
  continuous_cols = selected_data.select_dtypes(include=['float64', 'int64']).columns

  # Step 7: Create a preprocessing pipeline
  # Scale continuous data and one-hot encode categorical data
  preprocessor = ColumnTransformer(
      transformers=[
          ('num', StandardScaler(), continuous_cols),
          ('cat', OneHotEncoder(), categorical_cols)
      ])

  # Step 8: Create a pipeline to preprocess the data and apply KMeans
  pipeline = Pipeline(steps=[
      ('preprocessor', preprocessor),
      ('kmeans', KMeans(n_clusters=num_clusters))
  ])

  # Fit the pipeline to the data
  pipeline.fit(selected_data)

  # Get the cluster labels
  cluster_labels = pipeline.named_steps['kmeans'].labels_

  # Step 9: Add the cluster labels to the original DataFrame
  df['Cluster'] = cluster_labels

  # Display the DataFrame with the cluster labels
  print("\nHere is your dataset with the assigned cluster labels:")
  print(df.head())

  # Step 10: Visualize the Clusters (optional: if you selected two numeric columns)
  if len(continuous_cols) == 2:
      plt.scatter(df[continuous_cols[0]], df[continuous_cols[1]], c=df['Cluster'], cmap='viridis')
      plt.xlabel(continuous_cols[0])
      plt.ylabel(continuous_cols[1])
      plt.title(f'K-Means Clustering with {num_clusters} clusters')
      plt.show()

  # Step 11: Save the DataFrame with the cluster labels into a new Excel file
  output_file = "clustered_data.xlsx"
  df.to_excel(output_file, index=False)

  # Step 12: Allow the user to download the new Excel file
  print(f"\nThe file '{output_file}' has been created and is ready for download.")
  files.download(output_file)


#SUBPACKAGE: dtree---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct clustering analysis for data input as text type
#***********************************************************************************************************
def dtree():
  import pandas as pd
  from sklearn.model_selection import train_test_split
  from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
  from sklearn import tree
  from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
  from sklearn.preprocessing import LabelEncoder, OneHotEncoder
  import matplotlib.pyplot as plt
  from google.colab import files

  # Upload the Excel file
  uploaded = files.upload()

  # Load the uploaded Excel file into a pandas DataFrame
  file_name = list(uploaded.keys())[0]
  data = pd.read_excel(file_name)

  # Display the first few rows of the dataset
  print("Dataset Preview:")
  print(data.head())

  # Ask user to input feature columns and target column
  print("\nFeature (X) and Target (y) Selection:")
  print("***********************************************************************")
  print("***********************************************************************")
  print("Features (X) are the independent variables used to predict the target.")
  print("Target (y) is the dependent variable that we are trying to predict. It can be continuous or categorical.")
  print("***********************************************************************")
  print("***********************************************************************")

  # Display column names to help user choose
  print("\nAvailable columns in the dataset:")
  print(data.columns)

  # Ask user for input on which columns to use as features (X)
  features = input("\nEnter the column names for features (X) separated by commas: \n").split(',')
  # Strip extra spaces and display the user-selected features
  features = [feature.strip() for feature in features]
  print(f"\nYou selected features: {features}")

  # Ask user to input target column
  target = input("\nEnter the column name for the target (y): \n")
  target = target.strip()  # Strip any extra spaces
  print(f"\nYou selected target: {target}")

  # Split data into features (X) and target (y)
  X = data[features]
  y = data[target]

  # Explanation of test size
  print("\nTest Size Selection:")
  print("The test size is the proportion of the dataset that will be used for testing the model. The rest will be used for training. A typical test size is between 20% and 30% of the data.")

  # Ask user to input the test size
  test_size = float(input("\nEnter the test size as a fraction (e.g., 0.3 for 30% test size): \n"))
  print(f"\nYou selected a test size of: {test_size}")

  # Handle categorical features in X (if any)
  categorical_features = X.select_dtypes(include=['object', 'category']).columns
  if len(categorical_features) > 0:
      X = pd.get_dummies(X, columns=categorical_features)
      print(f"\nCategorical features found and one-hot encoded: {list(categorical_features)}")

  # Detect if the target is categorical or continuous
  if pd.api.types.is_numeric_dtype(y):
      # Continuous target -> Regression
      print("\nThe target is continuous. Performing regression analysis.")
      model = DecisionTreeRegressor(random_state=42)
      is_classification = False
  else:
      # Categorical target -> Classification
      print("\nThe target is categorical. Performing classification analysis.")
      le = LabelEncoder()
      y = le.fit_transform(y)  # Encode target labels as numbers for classification
      model = DecisionTreeClassifier(random_state=42)
      is_classification = True

  # Split the dataset into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

  # Train the model
  model.fit(X_train, y_train)

  # Predict on the test set
  y_pred = model.predict(X_test)

  # Evaluate the model based on the type of task (classification or regression)
  if is_classification:
      accuracy = accuracy_score(y_test, y_pred)
      print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
  else:
      mse = mean_squared_error(y_test, y_pred)
      r2 = r2_score(y_test, y_pred)
      print(f"\nModel Evaluation Metrics:")
      print(f"Mean Squared Error: {mse}")
      print(f"R-squared: {r2}")

  # Plot the Decision Tree
  plt.figure(figsize=(12, 8))
  tree.plot_tree(model, feature_names=X.columns, filled=True)
  plt.show()

  # Provide description of the Decision Tree
  n_nodes = model.tree_.node_count
  max_depth = model.tree_.max_depth
  print(f"\nThe decision tree has {n_nodes} nodes and a maximum depth of {max_depth}.")

  # Short conclusion based on model evaluation
  if is_classification:
      if accuracy > 0.8:
          print("\nConclusion: The model has a high accuracy, indicating that it performs well on this dataset.")
      elif accuracy > 0.6:
          print("\nConclusion: The model has moderate accuracy. It performs decently, but there is room for improvement.")
      else:
          print("\nConclusion: The model has low accuracy, and its predictions may not be reliable. Consider tuning the model or providing more data.")
  else:
      if r2 > 0.8:
          print("\nConclusion: The model explains most of the variance in the data and performs well.")
      elif r2 > 0.6:
          print("\nConclusion: The model explains a decent amount of variance, but there is room for improvement.")
      else:
          print("\nConclusion: The model does not explain much of the variance, and its predictions may not be very accurate. Consider tuning the model or providing more data.")


#SUBPACKAGE: test---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct varoious statistic tests
#***********************************************************************************************************
def test():
  import pandas as pd
  import numpy as np
  from scipy import stats
  import seaborn as sns
  import matplotlib.pyplot as plt
  from google.colab import files
  import io

  # Step 1: Upload the Excel file
  uploaded = files.upload()

  # Step 2: Load the Excel file into a DataFrame
  df = pd.read_excel(io.BytesIO(uploaded[list(uploaded.keys())[0]]))

  # Step 3: Display the uploaded data
  print("Here is the uploaded data:")
  print(df.head())

  # Step 4: Explain the statistical tests
  print("\nPlease choose a statistical test to perform:")
  print("1. Chi-Square Test: Used to examine the association between two categorical variables.")
  print("2. T-test: Used to compare the means of two groups (independent or paired).")
  print("3. ANOVA: Used to compare the means of three or more groups.")
  print("4. Z-test: Used to compare the means of two groups, typically when the sample size is large or the population variance is known.")

  # Step 5: User chooses the statistical test
  choice = input("\nEnter the number corresponding to your choice (1, 2, 3, or 4):\n")

  # Step 6: User enters the significance level
  alpha = float(input("\nEnter the significance level (e.g., 0.05 for 5% significance):\n"))

  # Step 7: Perform the chosen test and display the results
  if choice == '1':
      # Chi-Square Test
      crosstab = pd.crosstab(df['Group'], df['Measure'])
      chi2, p, dof, expected = stats.chi2_contingency(crosstab)

      print(f"\nChi-Square Test Results:")
      print(f"Chi-Square Statistic: {chi2:.4f}")
      print(f"Degrees of Freedom: {dof}")
      print(f"p-value: {p:.4f}")
      
      if p < alpha:
          print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant association between the Group and Measure variables. This means that the distribution of the Measure variable is different across the different Groups, and the likelihood of this difference being due to chance is low.")
      else:
          print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant association between the Group and Measure variables. This suggests that any observed differences in the distribution of the Measure variable across the Groups could likely be due to chance.")

      print("Note: Chi-Square Test is most appropriate when you have two categorical variables and you want to see if the categories are independent of each other.")
      
      # Plot the results
      sns.countplot(x='Group', hue='Measure', data=df)
      plt.title('Chi-Square Test: Group vs Measure')
      plt.show()

  elif choice == '2':
      # T-test (independent samples)
      groups = df['Group'].unique()
      
      if len(groups) != 2:
          print("Error: T-test requires exactly two groups.")
      else:
          group1 = df[df['Group'] == groups[0]]['Measure']
          group2 = df[df['Group'] == groups[1]]['Measure']
          
          t_stat, p = stats.ttest_ind(group1, group2)
          
          print(f"\nT-test Results:")
          print(f"T-statistic: {t_stat:.4f}")
          print(f"p-value: {p:.4f}")
          
          if p < alpha:
              print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in the means of {groups[0]} and {groups[1]}. This suggests that the observed difference in means is unlikely to have occurred by chance.")
          else:
              print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in the means of {groups[0]} and {groups[1]}. This implies that any observed difference in means could likely be due to chance.")

          print("Note: The T-test assumes that the data in each group is normally distributed and that the variances in the two groups are equal.")
          
          # Plot the results
          sns.boxplot(x='Group', y='Measure', data=df)
          plt.title('T-test: Group vs Measure')
          plt.show()

  elif choice == '3':
      # ANOVA
      f_stat, p = stats.f_oneway(*(df[df['Group'] == group]['Measure'] for group in df['Group'].unique()))

      print(f"\nANOVA Results:")
      print(f"F-statistic: {f_stat:.4f}")
      print(f"p-value: {p:.4f}")
      
      if p < alpha:
          print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in means across the groups. This suggests that at least one group mean is significantly different from the others.")
      else:
          print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in means across the groups. This suggests that any observed differences in means are likely due to chance.")

      print("Note: ANOVA assumes that the data in each group is normally distributed and that the variances across the groups are equal. If you find a significant result, post-hoc tests can be conducted to determine which specific groups differ from each other.")
      
      # Plot the results
      sns.boxplot(x='Group', y='Measure', data=df)
      plt.title('ANOVA: Group vs Measure')
      plt.show()

  elif choice == '4':
      # Z-test
      groups = df['Group'].unique()
      
      if len(groups) != 2:
          print("Error: Z-test requires exactly two groups.")
      else:
          group1 = df[df['Group'] == groups[0]]['Measure']
          group2 = df[df['Group'] == groups[1]]['Measure']
          
          mean1 = np.mean(group1)
          mean2 = np.mean(group2)
          std1 = np.std(group1, ddof=1)
          std2 = np.std(group2, ddof=1)
          n1 = len(group1)
          n2 = len(group2)
          
          # Calculate the Z-statistic
          z_stat = (mean1 - mean2) / np.sqrt((std1**2/n1) + (std2**2/n2))
          p = stats.norm.sf(abs(z_stat)) * 2  # two-tailed p-value
          
          print(f"\nZ-test Results:")
          print(f"Z-statistic: {z_stat:.4f}")
          print(f"p-value: {p:.4f}")
          
          if p < alpha:
              print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in the means of {groups[0]} and {groups[1]}. This suggests that the observed difference in means is unlikely to have occurred by chance.")
          else:
              print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in the means of {groups[0]} and {groups[1]}. This implies that any observed difference in means could likely be due to chance.")

          print("Note: The Z-test is generally used when the sample size is large or when the population variance is known. It assumes that the data in each group is normally distributed.")
          
          # Plot the results
          sns.boxplot(x='Group', y='Measure', data=df)
          plt.title('Z-test: Group vs Measure')
          plt.show()

  else:
      print("Invalid choice. Please restart and select a valid option.")
