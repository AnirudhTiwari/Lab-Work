'''
This module is responsible for predicting the number of domains a given multi-domain protein chain has.
The algorithm works as follows:
1. The feature set, training & test dataset is already provided, based on the training dataset the SVM is trained
2. For each of the test dataset entry, for k=2 to 4 features are calculated. 
3. For each feature set corresponding to a given k, the confidence score of the SVM is calculated
4. The k for which the confidence score is maximum is taken to be the correct value
'''


def 
