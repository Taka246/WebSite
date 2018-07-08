import pickle
import numpy as np
from PIL import Image
from sklearn import datasets
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam


def read():
    """予測モデルを読み込む"""
    with open('mnist.pickle', 'rb') as file:
        clf = pickle.load(file)
    return clf

def build_multilayer_perceptron():
    model = Sequential()

    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    return model

def create_and_save():
    """予測モデルを作成し、保存する"""
    # サンプル画像データのロード
    mnist = datasets.fetch_mldata('MNIST original', data_home='image/')
    X = X.astype('float32')
    X = mnist.data / 255
    y = mnist.target

    # 訓練用データとテスト用データに分ける
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=70000, test_size=0
    )

    # 多層ニューラルネットワークモデルを構築
    model = build_multilayer_perceptron()
    # モデルをコンパイル
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])

    # Early-stopping
    early_stopping = EarlyStopping(patience=0, verbose=1)

    # モデルの訓練
    clf = model.fit(X_train, y_train,
                        verbose=1,
                        validation_split=0.1,
                        callbacks=[early_stopping])


    # 予測モデルの保存
    with open('mnist', 'wb') as file:
        pickle.dump(clf, file)
    return clf


# pickleで保存したデータがなければ、新しく作る
try:
    clf = read()
except FileNotFoundError:
    clf = create_and_save()


def predict(img_array):
    """手書き文字を判別した結果を返す"""
    result = clf.predict(img_array)
    return str(int(result[0]))


if __name__ == '__main__':
    # 0.png ~ 9.pngを実際に試す
    for i in range(0, 10):
        file_name = '{}.png'.format(i)
        img = Image.open(file_name)
        img = np.asarray(img) / 255
        img_array = img.reshape(1, 784)
        result = predict(img_array)
        print(result)
