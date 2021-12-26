import warnings
import sklearn
import numpy as np

class NeuralNetwork():

    def __init__(self, dimensions=[0,0,0], learningRate=0): 
        self.dimensions = dimensions
        self.learningRate = learningRate

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

    def getDist(self, obstacles, SCREEN_WIDTH):
        return (obstacles[0].getX()-180)/SCREEN_WIDTH
    
    def getHeight(self, y_pos_bg, obstacles):
        return int((y_pos_bg-obstacles[0].getY())/100>0.7)
    
    def check_state(self, state, training_inputs):
        for input in training_inputs:
            if np.array_equal(state, input):
                return True
        return False

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
        self.w2 -= self.learningRate * self.dw2
        self.b1 -= self.learningRate * self.db1
        self.w1 -= self.learningRate * self.dw1

        self.dw1 = np.zeros([self.dimensions[1], self.dimensions[0]])
        self.dw2 = np.zeros([self.dimensions[2], self.dimensions[1]])
        self.db1 = np.zeros(self.dimensions[1])
        self.db2 = np.zeros(self.dimensions[2])

    def train(self, inputs, outputs, epochs=5):
        accuracy = 0
        err_sum = 0.0
        avg_err = 0.0
        correct = 0
        size = len(inputs)
        inputs, outputs = sklearn.utils.shuffle(inputs, outputs)
        
        for i in range(3,0,-1):
            if size%i==0:
                bs=i
                break
        
        for _ in range (epochs):
            for j in range(int(size/bs)):
                for m in range(bs):
                    correct_output = outputs[j*bs+m]
                    self.forwardProp(inputs[j*bs+m])
                    self.backProp(inputs[j*bs+m], correct_output)
                    
                    if np.argmax(self.outputNeurons) == np.argmax(correct_output):
                        correct+=1

                    error = np.amax(np.absolute(self.outputLayerErrors))
                    err_sum += error
                    
                self.change()
        
        avg_err = err_sum / (epochs*size)
        accuracy = str(int((correct/(epochs*size))*100)) + '%'  
        print ("Accuracy: " + accuracy + " - Loss: " + str(round(avg_err, 10)))

    def predict(self, inputs):
        self.forwardProp(inputs)
        return np.argmax(self.outputNeurons)