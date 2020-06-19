# Final exam. Recommendation system for online purchases

Katya Galaktionova, 05/07/2019

## 1. Load dataset

First, we will need to read csv file OnlineRetail.csv into Python using Pandas library. Then this dataset will be split into train and test subsets the way that 80% of data from the head is going to be train data and the rest 20% will become test set. I have checked that test set starts from new order, so no order is broken between two subsets.

## 2. Extract useful information from dataset

Our goal is to make recommendations based on what combinations of items were most popular. To do that we need to create a new object (in this case this will be series in Pandas), that will consist of lists of purchased products grouped by single purchase. Our column of interest is Description, grouped by Invoice Number. Later we will be able to send each list to Elasticsearch using for loop.

## 3. Create Elasticsearch index and put there information to analyze

In this section we define several functions to create index and schema in Elasticsearch for our analysis. Schema will be created the way that our data from previous section can be sent to Elasticsearch. Then for loop will be used to fling each single purchase into Elasticsearch as a single message. This for loop will take a while. These steps should be performed for both train and test datasets.

## 4. Perform query to get recommendations

First, we will print to the user list of all items available to purchase. For that purpose, print unique values from Description column from train subset. We are using train subset because it was used to build recommendations system and it is significantly bigger than test subset. Then we will ask user to choose one item from the list. User's input will be saved as upper-case string variable and past in query to look for highly correlated words from other messages (baskets). Query will be executed in train and test data sets to check for accuracy of the model.

## 5. Recommendation system check and visualization

For checking how good the built system gives recommendations *Red hanging heart t-light holder* item was chosen to build recommendations from train and test data subsets. Results revealed that not all recommended items from train subset were met in test subset, but most popular thing bonded with chosen item in both subsets was the same one - *White hanging heart t-light holder*. To confirm that result both items were put into search line in discover section in Kibana to see output first in train and then in test subsets. Result of these searches are shown in *kibana_train.png* and *kibana_test.png*.