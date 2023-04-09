# required imports
import pandas as pd
import string
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import tensorflow as tf

#Clearing sentences
def train_lr_model():
    data = pd.read_csv("questions.csv")
    cluster_data=data

    clean_data = []
    for i in range(0, data.shape[0]):
        line = data['Questions'].iloc[i]
        line = line.lower()
        translator = str.maketrans('', '', string.punctuation)
        line = line.translate(translator)
        line = " ".join(line.split())
        clean_data.append(line)

#Transforming sentences into matrix:

    embedder = SentenceTransformer('distilbert-base-nli-mean-tokens')
    clean_data_embeddings = embedder.encode(clean_data)


    df = pd.DataFrame(clean_data_embeddings)

    df['cluster']=data['cluster']

    df = df.sample(frac=1, random_state=42)   
    X = df.drop('cluster', axis=1)
    Y = df['cluster']

    # Split the dataset into training and testing sets
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    # Split data into training and testing sets
    train_data, test_data, train_labels, test_labels = train_test_split(X,Y, test_size=0.1, random_state=56)

    # Train a Linear Regression model
    # lr = LogisticRegression(max_iter=1200,random_state=0)
    # lr.fit(train_data, train_labels)

    #Train the Neural Network model
    model_nn=tf.keras.models.Sequential([
        tf.keras.layers.Dense(units=128, activation='relu', input_shape=(768,)),
        tf.keras.layers.Dense(units=128, activation='relu'),
        tf.keras.layers.Dense(units=128, activation='relu'),
        tf.keras.layers.Dense(units=128, activation='relu'),

        tf.keras.layers.Dense(units=59, activation='softmax'),
    ])

    #Compile the model with multi-class cross-entropy loss
    model_nn.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

    # #Train the model
    model_nn.fit(train_data, tf.keras.utils.to_categorical(train_labels),epochs=50,batch_size=40)

    # Predict target values on the test set
    y_pred = model_nn.predict(test_data)
    
    # return model object
    # return model_nn, cluster_data
    return model_nn, cluster_data
