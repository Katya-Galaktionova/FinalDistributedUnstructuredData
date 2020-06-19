import pandas as pd
import requests

## read the data
data = pd.read_csv('OnlineRetail.csv', encoding = 'ISO-8859-1')

## form test and train sets
train = data.head(int(len(data)*0.8))
test = data.tail(-int(len(data)*0.8))

## Create new object series from train dataframe which consists list of 
## descriptions grouped by InvoiceNumber
train_series = train.groupby('InvoiceNo')['Description'].apply(lambda x: x.tolist())

## Starting working with Elasticsearch
## Get indices
def get_es_indices():
    r = requests.get("http://elasticsearch:9200/_cat/indices?format=json")
    if r.status_code != 200:
        print("Error listing indices")
        return None
    else:
        indices_full = r.json()  # contains full metadata as a dict
        indices = []  # let's extract the names separately
        for i in indices_full:
            indices.append(i['index'])
        return indices, indices_full

indices, indices_full = get_es_indices()
print(indices)

def create_es_index(index, index_config):
    r = requests.put("http://elasticsearch:9200/{}".format(index),
                     json=index_config)
    if r.status_code != 200:
        print("Error creating index")
    else:
        print("Index created")


def delete_es_index(index):
    r = requests.delete("http://elasticsearch:9200/{}".format(index))
    if r.status_code != 200:
        print("Error deleting index")
    else:
        print("Index deleted")


indices, indices_full = get_es_indices()
if 'recommendations_train' in indices:
    delete_es_index('recommendations_train')


index_config = {
    "mappings": {
        "recommendation": {
            "properties": {
                "Basket": {"type": "string", "index": "not_analyzed"}
            }
        }
    }
}

create_es_index('recommendations_train', index_config)
print(indices)


def fling_message(index, doctype, msg):
    r = requests.post("http://elasticsearch:9200/{}/{}".format(index, doctype),
                      json=msg)
    if r.status_code != 201:
        print("Error sending message")
    else:
        print("message sent")


## loop through train_series and send descriptions of each invoice as a single message
## This might take a while
msg = {}
for i in range(0, len(train_series)):
    msg['Basket'] = train_series[i]
    fling_message('recommendations_train', 'recommendation', msg)


## check in test data set if it works.
## create series from test dataframe and send messages to elasticsearch the same way we did above

test_series = test.groupby('InvoiceNo')['Description'].apply(lambda x: x.tolist())

indices, indices_full = get_es_indices()
if 'recommendations_test' in indices:
    delete_es_index('recommendations_test')

create_es_index('recommendations_test', index_config)
print(indices)

for i in range(0, len(test_series)):
    msg['Basket'] = test_series[i]
    fling_message('recommendations_test', 'recommendation', msg)




## Give user list of items and ask to choose one
print(train.Description.unique())
user_choice = str(input('''Please choose item from the above list: ''')).upper()

## put user_choice into querry and search for recommendations

def execute_es_query(index, query):
    r = requests.get("http://elasticsearch:9200/{}/_search".format(index),
                     json=query)
    if r.status_code != 200:
        print("Error executing query")
        return None
    else:
        return r.json()


query = {
    "size": 0,
    "query": {
        "bool": {
            "filter": [
                {"term": {"Basket": user_choice}},
            ]
        }
    },
    "aggs": {
        "highly_correlated_words": {
            "significant_terms": {
                "field": "Basket",
                "exclude": user_choice,
                "min_doc_count": 20,
            }
        }
    }
}

print("Recommendations from train set: ")
res = execute_es_query('recommendations_train', query)
print (res)

print("Recommendation from test set: ")
res2 = execute_es_query('recommendations_test', query)
print(res2)

print('We are done! Thanks for great class Spencer!')
