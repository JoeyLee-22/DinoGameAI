import time
import warnings
import numpy as np

class NeuralNetwork():

    def __init__(self, dimensions=[0,0,0], learning_rate=0): 
        self.dimensions = dimensions

        self.secondLayerNeurons = np.empty(dimensions[1])
        self.outputNeurons = np.empty(dimensions[2])

        self.w1 = np.random.rand(dimensions[1], dimensions[0]) * 2 - 1
        self.w2 = np.random.rand(dimensions[2], dimensions[1]) * 2 - 1
        self.b1 = np.zeros([dimensions[1]])
        self.b2 = np.zeros([dimensions[2]])

        self.dw1 = np.zeros([dimensions[1], dimensions[0]])
        self.dw2 = np.zeros([dimensions[2], dimensions[1]])
        self.db1 = np.zeros([dimensions[1]])
        self.db2 = np.zeros([dimensions[2]])

        self.hiddenLayerErrors = np.empty(dimensions[1])
        self.outputLayerErrors = np.empty(dimensions[2])

    def sigmoid(self, x):
        warnings.filterwarnings("ignore")
        return 1/(1+np.exp(-x))

    def sigmoidDerivative(self, x):
        return np.multiply(x,(1-x))

    def softmax(self, x):
        exps = np.exp(x - np.max(x))
        return exps / np.sum(exps)

    def forwardProp(self, inputs):
        self.secondLayerNeurons = self.sigmoid(self.w1 @ inputs + self.b1)
        self.outputNeurons = self.softmax(self.w2 @ self.secondLayerNeurons + self.b2)

    def backProp(self, inputs, correct_output):
        self.outputLayerErrors = np.subtract(self.outputNeurons, correct_output)
        self.hiddenLayerErrors = np.multiply(np.dot(self.w2.T, self.outputLayerErrors), self.sigmoidDerivative(self.secondLayerNeurons))

        self.db2 += self.outputLayerErrors
        self.dw2 += np.dot(self.outputLayerErrors.reshape(self.dimensions[2],1), self.secondLayerNeurons.reshape(1,self.dimensions[1]))
              
        self.db1 += self.hiddenLayerErrors
        self.dw1 += np.dot(self.hiddenLayerErrors.reshape(self.dimensions[1],1), inputs.reshape(1,self.dimensions[0]))

    def change(self):
        self.b2 -= self.learningRate * self.db2
        self.w2 -= self.learningRate * (self.dw2 + self.Lambda * self.w2)
        self.b1 -= self.learningRate * self.db1
        self.w1 -= self.learningRate * (self.dw1 + self.Lambda * self.w1)

        self.dw1 = np.zeros([self.dimensions[1], self.dimensions[0]])
        self.dw2 = np.zeros([self.dimensions[2], self.dimensions[1]])
        self.db1 = np.zeros(self.dimensions[1])
        self.db2 = np.zeros(self.dimensions[2])

    def train(self, trainImages, trainLabels):
        for m in range (self.bs):
            correct_output = np.zeros([self.dimensions[2]])
            correct_output[trainLabels[m]] = 1.0

            self.forwardProp(trainImages[m].flatten())
            self.backProp(trainImages[m].flatten(), correct_output)

        self.change()

    def predict(self, testImage):
        self.forwardProp(testImage)
        return np.argmax(self.outputNeurons)

if __name__ == "__main__":
    nn = NeuralNetwork(dimensions = [5, 16, 3], learning_rate = 1e-5)