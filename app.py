from flask import Flask, render_template, request, jsonify
import models.model as model
import string
import pandas as pd
from sentence_transformers import SentenceTransformer
import random
from prettytable import from_csv
import csv

data = {}

# answer_data=pd.read_csv("answers.csv")
# Read the CSV data into a prettytable object
# with open('answers.csv', 'r') as f:
#     table = from_csv(f, delimiter=',')
# Load the CSV file into a list of dictionaries
with open('answers.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if 'cluster' in row:
            cluster = row['cluster']
            if cluster not in data:
                data[cluster] = []
            data[cluster].append(row['answer'])

answer_data = data
#print(answer_data)

nn, cluster_data = model.train_lr_model()
val = 0

app = Flask(__name__)

# index route
@app.route('/')
def index():
    return render_template('index.html')

# test api
# @app.route('/test-ui')
# def test_ui():
#     return render_template('test-index.html')


# dummy api to test UI
# @app.route('/api/v1.0/get-dummy-answer/<question>')
# def get_dummy_answer(question):
#     ans = '# To be edited #'
#     return render_template('dummy-api.html', question=question, ans=ans)


# get_cluster API get the cluster label for the given question
@app.route('/api/v1.0/get-cluster/<question>', methods=['GET'])
def get_cluster(question):
    question = question.lower()
    translator = str.maketrans('','',string.punctuation)
    question = question.translate(translator)
    question = " ".join(question.split())
    embedder = SentenceTransformer('distilbert-base-nli-mean-tokens')
    question = embedder.encode(question)
    question2d = question.reshape(1, 768)

    cluster_arr = nn.predict(question2d)
    #cluster = cluster_arr[0].astype('U')
    max_res=max(cluster_arr)
    max_val=max(max_res)
    global val
    val=0
    for i in range(0,len(max_res)):
        if max_res[i]==max_val:
            val=i
            break
    
    # choose the random question
    # cluster1=val
    # if cluster1==58:
    #     cluster1=cluster1-1
    # else:
    #     cluster1=cluster1+1
    # cluster_data = cluster_data[cluster_data.cluster==cluster1]
    # cluster_question=cluster_data['Questions'].values
    # random_index = random.randint(0, len(cluster_question)-1)

    # Select the random question
    # random_question = cluster_question[random_index]

    # #Select the answer
    # res_answer_data = answer_data[answer_data.cluster == val]
    # answer = res_answer_data['answer'].iloc[0]
    # table = from_csv(answer, delimiter=',')
    # # Set the format options to preserve whitespace and indentation
    # table.format = True
    # # Generate the HTML table
    # html_table = table.get_html_string()

    answer = answer_data[str(val)]
    answer = answer[0]
    
    return jsonify({'answer': '<pre>' + answer + '</pre>'})


# API to get suggested questions based on the last question asked
@app.route('/api/v1.0/get-suggested-ques/')
def get_questions():
    global val
    if val == 58:
        # for last cluster the cluster number has to be reset
        cluster_num = val - 1
    else:
        cluster_num = val + 1
    
    result = cluster_data[cluster_data.cluster == cluster_num]
    resultQs = result['Questions'].values
    
    return list(resultQs)

# driver function
if __name__ == '__main__':
    app.run(debug=True)
