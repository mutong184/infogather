import os.path

import tensorflow as tf
import numpy as np


class LogisticRegressionModel:
    def __init__(self):
        self.model = None

    def binary_crossentropy(self, y_true, y_pred):
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_true, logits=y_pred))
        return loss

    def train(self, x_train, y_train, epochs=50, batch_size=10):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        self.model.compile(optimizer='adam', loss=self.binary_crossentropy)
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    def predict(self, x):
        predictions = self.model.predict(x)
        predictions = predictions.flatten()
        predictions = np.round(predictions)
        return predictions

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = tf.keras.models.load_model(path)

def train_mode(train_file,model_store):
    # 从txt文件中读取数据
    #data = np.loadtxt('D:\ljj\data\\train1.txt', delimiter="#", comments=None)
    data = np.loadtxt(train_file, delimiter="#", comments=None)

    # 提取特征和标签
    x_train = data[:, :-1]  # 所有行，除了最后一列之外的所有列
    y_train = data[:, -1]  # 所有行，最后一列

    # 创建逻辑回归模型对象
    model = LogisticRegressionModel()

    # 训练模型
    model.train(x_train, y_train)

    # 保存模型参数
    path,file = os.path.split(train_file)
    weigthfile = os.path.join(path,"weigth.txt")
    with open(weigthfile,"w",encoding="utf-8") as f:
        weights = model.model.get_weights()
        for w in weights:
            f.write(np.array2string(w))
    # 使用训练好的模型进行预测
    predictions = model.predict(x_train)

    # 计算准确度
    accuracy = np.mean(np.equal(predictions, y_train))
    print("准确度：", accuracy)

    # 保存模型
    #model.save_model('D:\ljj\data\model')
    model.save_model(model_store)

def predict(test_file,model_path):
    # 从txt文件中读取数据
    # data = np.loadtxt('D:\ljj\data\\train1.txt', delimiter="#", comments=None)
    data = np.loadtxt(test_file, delimiter="#", comments=None)

    # 提取特征和标签
    x_test = data[:, :-1]  # 所有行，除了最后一列之外的所有列
    y_test = data[:, -1]  # 所有行，最后一列

    # 创建逻辑回归模型对象
    model = LogisticRegressionModel()
    model.load_model(model_path)
    predictions = model.predict(x_test)
    # 计算准确度
    accuracy = np.mean(np.equal(predictions, y_test))
    print("准确度：", accuracy)

train_mode('D:\ljj\data\\traindata.txt',"D:\ljj\data\model")
print("train success")
predict('D:\ljj\data\\testdata.txt',"D:\ljj\data\model")

