from scipy import optimize
import numpy as np
from numpy import matlib


################################## CALCULATE SOFTMAX COST AND GRADIENT #################################################
def softmaxCost(theta, numClasses, inputSize, lam, data, labels):

    # reshape parameters to work with
    theta = np.reshape(theta, (numClasses, inputSize))
    numCases = data.shape[1]
    m = float(numCases)

    # Fill in groundTruth matrix, this matrix keeps track of the actual
    # labels of each element in the training set.
    groundTruth = np.zeros((numClasses, numCases))
    groundTruth[labels.astype(int), np.linspace(0, numCases-1, numCases, dtype=int)] = 1.

    # calculate cost
    expPower = np.dot(theta, data)
    expPower = expPower - np.max(expPower)  # avoid possible overflow when expoential applied
    costDen = np.sum(np.exp(expPower), 0)
    hyp = np.divide(np.exp(expPower), np.matlib.repmat(costDen, numClasses, 1))
    num = np.multiply(groundTruth, np.log(hyp))
    cost = (-1./m)*sum(sum(num)) + 0.5*lam*sum(sum(np.multiply(theta, theta)))

    # calculate gradient
    diff = groundTruth - hyp
    thetaGrad = -np.dot(diff, np.transpose(data))/m + lam*theta

    return cost, thetaGrad.flatten()


############################################ TRAIN SOFTMAX REGRESSION ##################################################

def train(numClasses, inputSize, lam, trainData, trainLabel):
    # randomly initialize theta
    theta = 0.005*np.random.randn(numClasses*inputSize, 1)
    # implement softmaxCost
    J = lambda x: softmaxCost(x, numClasses, inputSize, lam, trainData, trainLabel)

    #optimize theta values
    tmp = optimize.minimize(J, theta, method='L-BFGS-B', jac=True, options={'maxiter': 400})
    thetaOpt = tmp.x

    return thetaOpt

########################################## PREDICT LABELS FOR TEST DATA ################################################

def predict(theta, testData, numClasses, inputSize):
    # reshape
    theta = np.reshape(theta, (numClasses, inputSize))
    m = testData.shape[1]

    #calculate most likely label
    expPower = np.dot(theta, testData)
    costDen = np.sum(np.exp(expPower), 0)
    hyp = np.divide(np.exp(expPower), np.matlib.repmat(costDen, numClasses, 1))
    pred = np.argmax(hyp, axis=0)

    return pred
