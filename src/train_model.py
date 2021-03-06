import os

import torch
import torch.nn as nn
import torch.optim as optim

from model_defintion.variable_rnn import VariableRNN
from utils.utils import evaluate, train


def train_rnn_model(train_loader, val_loader, num_features, num_epochs, use_cuda, path_output):
    """
    Use train and validation loader to train the variable RNN model
    Input: train_loader, val_loader
    Output: trained best model
    """
    device = torch.device("cuda" if torch.cuda.is_available() and use_cuda else "cpu")
    torch.manual_seed(1)
    if device.type == "cuda":
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    model = VariableRNN(num_features)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())

    model.to(device)
    criterion.to(device)

    best_val_acc = 0.0

    train_losses, train_accuracies = [], []
    valid_losses, valid_accuracies = [], []

    for epoch in range(num_epochs):

        train_loss, train_accuracy = train(model, device, train_loader, criterion, optimizer, epoch)
        valid_loss, valid_accuracy, valid_results = evaluate(model, device, val_loader, criterion)

        train_losses.append(train_loss)
        valid_losses.append(valid_loss)

        train_accuracies.append(train_accuracy)
        valid_accuracies.append(valid_accuracy)

        is_best = valid_accuracy > best_val_acc

        if is_best:
            best_val_acc = valid_accuracy
            torch.save(
                model,
                os.path.join(path_output, "VariableRNN.pth"),
                _use_new_zipfile_serialization=False,
            )

    best_model = torch.load(os.path.join(path_output, "VariableRNN.pth"))
    return (
        best_model,
        train_losses,
        valid_losses,
        train_accuracies,
        valid_accuracies,
        valid_results,
    )
