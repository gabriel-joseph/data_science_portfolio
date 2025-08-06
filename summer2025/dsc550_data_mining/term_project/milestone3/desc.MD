Now that you have created your idea, located data, and have started your graphical analysis, you will move on to the data preparation process of your project. After completing Milestone 2, your data should be ready for the model building/evaluation phase.
Here is a list of steps to consider performing in Milestone 2:
Drop any features that are not useful for your model building and explain why they are not useful.
Perform any data extraction/selection steps.
Transform features if necessary.
Engineer new useful features.
Deal with missing data (do not just drop rows or columns without justifying this).
Create dummy variables if necessary.
Explain your process at each step. You can use any methods/tools you think are most appropriate. Do what makes the most sense for your data/problem. This will vary greatly among different projects. Be careful to avoid data snooping in these steps.
It is important to note that these milestones are meant to keep you on track for the final project submission. At any point, you can pivot or modify your project as needed based on what you discover. These milestones are not final versions; they are drafts of the many steps you need to complete along the way.
As a reminder, Teams is a great place to discuss your project with your peers. Feel free to solicit feedback/input (without creating a group project!) and collaborate on your projects with your peers.
Each milestone will build on top of each other, so make sure you do not fall behind. Submit Milestones 1 & 2 together. I recommend building your project milestones in a Jupyter Notebook, building upon one another. However, make sure it is clear where Milestone 1 ends and Milestone 2 begins.


# Dummy variables (also called one-hot encoding) are used to convert categorical variables 
# into a numerical format. For each category in a feature, a new column is created with a 
# value of 1 if the observation belongs to that category, and 0 otherwise. This allows 
# categorical data to be used in machine learning models.

import pandas as pd

df = pd.DataFrame({'Color': ['Red', 'Green', 'Blue']})
# Convert the 'Color' column to dummy variables
df_dummies = pd.get_dummies(df, columns=['Color'])

# Result:
#    Color_Blue  Color_Green  Color_Red
# 0           0            0          1
# 1           0            1          0
# 2           1            0          0
