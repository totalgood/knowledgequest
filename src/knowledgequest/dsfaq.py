# Datascience FAQ
-
q: How to use chi squared test in feature selection?
a: Personally I find it hard to know ahead of time what the right threshold for chi**2 test is. Instead I use automatic dimension reduction techniques like PCA, regularization, and hyperparameter tuning (grid search). These require less "judgement" on my part. I let the data and algorithm make the decision for me.
-
q: What's the benefits of using log loss vs accuracy? And usually where log loss is used? (do we just treat for example 5 % quantile as outliers?)
a: There are numerous cost/loss functions you can use, or you can make up your own. Almost all of them will give you the same answer to your optimization/fitting problem. But some will be better or worse at telling you how good your model is at predicting the things you care about. Sometimes you care about the standard error, sometimes you care about the log of the computer standard error, sometimes accuracy is more important to the success of your project, sometimes precision, sometimes recall, sometimes F1 or AUC. What do you think the agile approach would be to answering your question? Is there a way to use my answer to 1 to come up with an approach to question 2? Is there a way to ask your "boss" or customer which one matters most to them? What is the measure of units that most businesses measure success or lose (cost ) with? What are the best "units" for business decisions?
-
q: How to detect outliers in a data set and how to handle them?
a: Like other pipeline design challenges, I do outlier filtering in an agile way. Can you guess what that is? Spoiler alert... Outliers can be discarded automatically during hyperparameter tuning, or even within the model itself (random forest or xg-boost) 
a: Correlation is a mathematical statistic. It can be calculated on any numerical value (integer or binary or float, but not a categorical).  What do we do with all categorical features to create numerical values that work in a machine learning pipeline? Hint: correlation is equivalent to linear regression.
a: think deeply about hot an interesting is different from a float. Is 2.0 Twitter likes the same thing mathematically as 2 Twitter likes ?  30.0 vs 30 years old ? What about 5.0 stars vs 5 stars? What about toaster oven low med high vs a numerical toaster knob with 0, 1, 2 or 0.0 1.0 2.0 ? What about word frequency of 0/1 vs TF-IDF of 0.0/1.0 vs Boolean word presence value of False/True ?
a: Each situation is different. You have to think about the "physics" of something to know what what the best numerical representation is. We can go through some examples to help you learn how to think about numerical value types like binary, int, float, boolean, categorical, ordinal, and continuous things in the real world.


On Wed, Dec 26, 2018, 1:05 AM Fengying Deng <phoenixdeng2012@gmail.com> wrote:

    Hi Hobson,

    Merry Christmas! 

    Here are some questions I have and wonder if we can go over them in tmr's call:

    #1: 
    #2: 
    #3: 
    #4: how to check the correlation b/t two variables, specifically these two special case:
    ##4.1: an integer (for example how many people likes a comment on twitter) vs the age of user
    ##4.2: an integer vs a boolen, for example whether a user is an engineer or not. 
    Is pearson correlation coefficient work for both conditions? Even if one of the variable is boolen?
