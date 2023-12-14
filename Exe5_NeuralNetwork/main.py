import warnings
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.datasets import imdb
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix

"""
Author
    Sebastian Mackiewicz - PJAIT student

Build program that based on given datasets will train Neural Networks for classification

Before running program install
pip install warnings
pip install pandas
pip install tensorflow
pip install numpy
pip install matplotlib.pyplot
pip install seaborn

Make sure you have installed python at least in version 3.10
"""

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning, module='tensorflow')
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def exe1():
    """Description of the exe1 function
         Train Neural Networks with Heart Disease dataset and returns process of learning/training.
    """

    data = pd.read_csv('heart.csv')

    data_labels = data.pop('target')
    data_features = data.values

    data_model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(data_features.shape[1],)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    data_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    data_model.fit(data_features, data_labels, epochs=10, batch_size=32)

def exe2():
    """Description of the exe2 function
         Train Neural Networks with cifar10 dataset and returns process of learning/training.
    """

    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test))

    predictions = model.predict(x_test)

    class_names = [
        'airplane', 'automobile', 'bird', 'cat', 'deer',
        'dog', 'frog', 'horse', 'ship', 'truck'
    ]

    for i in range(len(predictions)):
        predicted_label = np.argmax(predictions[i])
        true_label = np.argmax(y_test[i])

        if class_names[true_label] in ['bird', 'cat', 'deer', 'dog', 'frog', 'horse']:
            print(f"True label: {class_names[true_label]}, Predicted label: {class_names[predicted_label]}")

def exe3():
    """Description of the exe3 function
        Train Neural Networks with fashion_mnist dataset and returns process of learning/training.
    """

    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    y_train = tf.keras.utils.to_categorical(y_train, 10)
    y_test = tf.keras.utils.to_categorical(y_test, 10)

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test))

    predictions = model.predict(x_test)

    class_names = [
        'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
        'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
    ]

    for i in range(len(predictions)):
        predicted_label = np.argmax(predictions[i])
        true_label = np.argmax(y_test[i])

        if class_names[true_label] in ['T-shirt/top', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker']:
            print(f"True label: {class_names[true_label]}, Predicted label: {class_names[predicted_label]}")


def exe4():
    """Description of the exe4 function
        Train Neural Networks with imdb reviews dataset and returns process of learning/training and plot with confusion matrix.
    """

    max_words = 10000
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_words)

    maxlen = 100
    x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = tf.keras.preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(max_words, 32, input_length=maxlen),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test))

    loss, accuracy = model.evaluate(x_test, y_test)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    y_pred_probs = model.predict(x_test)
    y_pred = (y_pred_probs > 0.5).astype(int)

    conf_matrix = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

exe1()
exe2()
exe3()
exe4()
