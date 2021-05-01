import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
# from lightgbm import LGBMClassifier
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_predict, train_test_split
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class VariableRNN(nn.Module):
    def __init__(self, dim_input):
        super(VariableRNN, self).__init__()
        # You may use the input argument 'dim_input', which is basically the number of features
        self.fc32 = nn.Linear(dim_input, 32)
        self.gru = nn.GRU(
            input_size=32, hidden_size=16, num_layers=2, dropout=0.15, batch_first=True,
        )
        self.fc2 = nn.Linear(16, 2)

    def forward(self, input_tuple):
        # build architecture
        x, lengths = input_tuple
        import pdb
        # pdb.set_trace()
        
        # pass x through the first layer
        x = F.relu(self.fc32(x))
        # create packed sequence as input to the lstm
        packed_x = pack_padded_sequence(x, lengths, batch_first=True)
        # pass padded pack sequence through the lstm layer
        packed_x, _ = self.gru(packed_x)
        # unpack the padded sequence from lstm output
        x, _ = pad_packed_sequence(packed_x, batch_first=True)
        # pass through the second layer
        x = self.fc2(x[:, -1, :])

        return x


# def logreg(X, y):

#     k = 5
#     kf = KFold(n_splits=k, random_state=None)
#     lrm = LogisticRegression(solver="liblinear")

#     roc_score = []

#     for train_index, test_index in kf.split(X):

#         X_train, X_test = X.todense()[train_index, :], X.todense()[test_index, :]
#         # [:10, :10]
#         y_train, y_test = np.array(y)[train_index], np.array(y)[test_index]

#         lrm.fit(X_train, y_train)
#         pred_values = lrm.predict(X_test)

#         roc = metrics.roc_auc_score(pred_values, y_test)
#         roc_score.append(roc)

#     avg_roc_score = sum(roc_score) / k

#     print("Accuracy of each fold - {}".format(roc_score))
#     print("Avg accuracy : {}".format(avg_roc_score))


# def lightgbm(X, y):

#     k = 5
#     kf = KFold(n_splits=k, random_state=None)
#     lgbm = LGBMClassifier()

#     roc_score = []

#     for train_index, test_index in kf.split(X):
#         X_train, X_test = X.todense()[train_index, :], X.todense()[test_index, :]
#         # [:10, :10]
#         y_train, y_test = np.array(y)[train_index], np.array(y)[test_index]

#         lgbm.fit(X_train, y_train)
#         pred_values = lgbm.predict(X_test)

#         roc = metrics.roc_auc_score(pred_values, y_test)
#         roc_score.append(roc)

#     avg_roc_score = sum(roc_score) / k
#     print("Accuracy of each fold - {}".format(roc_score))
#     print("Avg accuracy : {}".format(avg_roc_score))
#     # print(metrics.roc_auc_score(y_test, y_pred))
