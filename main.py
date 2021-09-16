import scipy.io
import math
import matplotlib.pyplot as plt
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
train_feature_count, train_sample_count = 57, 3065
Xtrain_bin = [[0 for x in range(train_feature_count)] for y in range(train_sample_count)]
Xtrain_log = [[0 for x in range(train_feature_count)] for y in range(train_sample_count)]

test_feature_count, test_sample_count = 57, 1536
Xtest_bin = [[0 for x in range(test_feature_count)] for y in range(test_sample_count)]
Xtest_log = [[0 for x in range(test_feature_count)] for y in range(test_sample_count)]


Ytrain_spam = 0
Ytrain_non_spam = 0
Ytest_spam = 0
Ytest_non_spam = 0

Xtrain_feature_1 = [0 for x in range(train_feature_count)] #number of counts of 1 for each of the features in X of the training set
Xtrain_feature_0 = [0 for x in range(train_feature_count)] #number of counts of 1 for each of the features in X of the training set

def initialise():
#training set
    for i in range(train_sample_count):
        for j in range (train_feature_count):
            #logarize
            Xtrain_log[i][j] = math.log(Xtrain[i][j]+0.1)

            #binarize
            if Xtrain[i][j] > 0:
                Xtrain_bin[i][j] = 1

#number of spam and non spam
        if Ytrain[i][0] == 1:
            global Ytrain_spam
            Ytrain_spam += 1
            for k in range (train_feature_count):
                if Xtrain_bin[i][k] == 1:
                    Xtrain_feature_1[k] += 1
        else:
            global Ytrain_non_spam
            Ytrain_non_spam += 1
            for k in range (len(Xtrain_bin[i])):
                if Xtrain_bin[i][k] == 1:
                    Xtrain_feature_0[k] += 1
#test set
    for i in range(len(Xtest)):
        for j in range (len(Xtest[i])):
            #logarize
            Xtest_log[i][j] = math.log(Xtest[i][j]+0.1)

            #binarize
            if Xtest[i][j] > 0:
                Xtest_bin[i][j] = 1

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
lambda_ml = Ytrain_spam/train_sample_count
a = 0
success = 0

#for testing on test samples
error_rate_testing = []
while a <= 100:
    for i in range (test_sample_count):
        temp_1 = lambda_ml  # y=1
        temp_2 = 1 - lambda_ml  # y=0
        for j in range (test_feature_count):
            if Xtest_bin[i][j] == 1:
                temp_1 = temp_1 * ((Xtrain_feature_1[j] + a) / (Ytrain_spam + a + a))
                temp_2 = temp_2 * ((Xtrain_feature_0[j] + a) / (Ytrain_non_spam + a + a))
            else:
                temp_1 = temp_1 * (1 - (Xtrain_feature_1[j] + a) / (Ytrain_spam + a + a))
                temp_2 = temp_2 * (1 - (Xtrain_feature_0[j] + a) / (Ytrain_non_spam + a + a))

        if temp_1 > temp_2:
            if Ytest[i][0] == 1:
                success += 1
        else:
            if Ytest[i][0] == 0:
                success += 1

    error_rate_testing.append(1-success/test_sample_count)
    success = 0
    a += 0.5
print(error_rate_testing)


#for testing on test samples
lambda_ml = Ytrain_spam/train_sample_count
a = 0
a_list = []
error_rate_training = []
while a <= 100:
    a_list.append(a)
    for i in range (train_sample_count):
        temp_1 = lambda_ml  # y=1
        temp_2 = 1 - lambda_ml  # y=0
        for j in range (train_feature_count):
            if Xtrain_bin[i][j] == 1:
                temp_1 = temp_1 * ((Xtrain_feature_1[j] + a) / (Ytrain_spam + a + a))
                temp_2 = temp_2 * ((Xtrain_feature_0[j] + a) / (Ytrain_non_spam + a + a))
            else:
                temp_1 = temp_1 * (1 - (Xtrain_feature_1[j] + a) / (Ytrain_spam + a + a))
                temp_2 = temp_2 * (1 - (Xtrain_feature_0[j] + a) / (Ytrain_non_spam + a + a))

        if temp_1 > temp_2:
            if Ytrain[i][0] == 1:
                success += 1
        else:
            if Ytrain[i][0] == 0:
                success += 1

    error_rate_training.append(1-success/train_sample_count)
    success = 0
    a += 0.5

print(error_rate_training)

plt.plot(a_list, error_rate_testing)

# naming the x axis
plt.xlabel('a value')
# naming the y axis
plt.ylabel('test sample error rate')

# giving a title to my graph
plt.title('Test Sample')

# function to show the plot
plt.show()



plt.plot(a_list, error_rate_training)

# naming the x axis
plt.xlabel('a value')
# naming the y axis
plt.ylabel('training sample error rate')

# giving a title to my graph
plt.title('Training Sample')

# function to show the plot
plt.show()
