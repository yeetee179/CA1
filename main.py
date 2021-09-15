import scipy.io
import math
import collections

mat = scipy.io.loadmat('spamData.mat')

print(mat.keys()) #'__header__', '__version__', '__globals__', 'Xtrain', 'Xtest', 'ytrain', 'ytest'

print(mat.get('__header__'))
print(mat.get('__version__'))
print(mat.get('__globals__'))
Xtrain = mat.get('Xtrain')
Xtest = mat.get('Xtest')
Ytrain = mat.get('ytrain')
Ytest = mat.get('ytest')

# Creates a empty list containing 3065 lists, each of 57 items, all set to 0
train_feature, train_sample = 57, 3065
Xtrain_bin = [[0 for x in range(train_feature)] for y in range(train_sample)]
Xtrain_log = [[0 for x in range(train_feature)] for y in range(train_sample)]

test_feature, test_sample = 57, 1536
Xtest_bin = [[0 for x in range(test_feature)] for y in range(test_sample)]
Xtest_log = [[0 for x in range(test_feature)] for y in range(test_sample)]


Ytrain_spam = 0
Ytrain_non_spam = 0
Ytest_spam = 0
Ytest_non_spam = 0

Xtrain_feature_1 = [] #number of counts of 1 for each of the features in X of the training set
Xtrain_feature_0 = [] #number of counts of 1 for each of the features in X of the training set

def initialise():
#training set
    for i in range(len(Xtrain)):
        for j in range (len(Xtrain[i])):
            #logarize
            Xtrain_log[i][j] = math.log(Xtrain[i][j]+0.1)

            #binarize
            if Xtrain[i][j] > 0:
                Xtrain_bin[i][j] = 1

#number of spam and non spam
        if Ytrain[i][0] == 1:
            global Ytrain_spam
            Ytrain_spam += 1
            for k in range (len(Xtrain[i])):
                if Xtrain[i] == 1:
                    Xtrain_feature_1[i] += 1
        else:
            global Ytrain_non_spam
            Ytrain_non_spam += 1
            for k in range (len(Xtrain[i])):
                if Xtrain[i] == 1:
                    Xtrain_feature_0[i] += 1
#test set
    for i in range(len(Xtest)):
        for j in range (len(Xtest[i])):
            #logarize
            Xtest_log[i][j] = math.log(Xtest[i][j]+0.1)

            #binarize
            if Xtest_bin[i][j] > 0:
                Xtest_bin[i][j] = 0

#number of spam and non spam
        if Ytest[i][0] == 1:
            global Ytest_spam
            Ytest_spam += 1

        else:
            global Ytest_non_spam
            Ytest_non_spam += 1


initialise()

#question 1
#lambda_ml = likelihood of spam. N1/N, where N1 is the number of spam emails
lambda_ml = Ytrain_spam/train_sample
a = 0

temp_1 = lambda_ml
temp_2 = 1 - lambda_ml
for i in range (test_sample):
    for j in range (test_feature):
        if Xtest_bin[i][j] == 1:
            temp_1 = temp_1 * ((Xtrain_feature_1 + a) / (Ytrain_spam + a + a))
            temp_2 = temp_1 * ((Xtrain_feature_0 + a) / (Ytrain_spam + a + a))
        elif Xtest_bin[i][j] == 0:
            temp_2 = temp_2 * (1 - (Xtrain_feature_0 + a) / (Ytrain_spam + a + a))



print(Ytrain_spam+Ytrain_non_spam)



# for i in range (len(Xtrain)):
#     print(1111111111111111111111111111111111)
#     print(Xtrain[i])
#     print(Xtrain_bin[i])
#     print(Xtrain_log[i])

print(type(Xtrain[1][1]))
print(Xtrain[1][1])
print(Ytrain)
# print(mat.get('Xtest'))
# print(mat.get('ytrain'))
# print(mat.get('ytest'))
