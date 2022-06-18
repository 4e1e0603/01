# -*- coding: utf-8 -*-


from ftplib import error_reply
from os import access
from typing import Callable

import numpy as np
from tqdm import tqdm



__all__ = tuple(["Network"])


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    return 1 - np.tanh(x) ** 2


def mse(y_original, y_prediction) -> float:
    return np.mean(np.power(y_original - y_prediction, 2))


def mse_derivative(y_original, y_prediction) -> float:
    return 2 * (y_original - y_prediction) / y_original.size


class Layer:

    def __init__(self, input = None, output = None) -> None:
        self._input = input
        self._output = output

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value) -> None:
        self._input = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value) -> None:
        self._output = value

    def forward_propagation(self, input) -> None:
        raise NotImplemented

    def backward_propagation(self, output_error, learning_rate) -> None:
        raise NotImplemented


class FullyConnectedLayer(Layer):
    """
    The fully connected layer.
    """

    def __init__(self, input_size, output_size) -> None:
        """
        :param input size: The number of input values (neurons).
        :param output size: The number of output values (neurons).
        """
        super().__init__(None, None)
        self._bias = np.random.rand(1, output_size) - 0.5
        self._weights = np.random.rand(input_size, output_size) - 0.5

    @property
    def bias(self): # -> np.array
        return self._bias

    @bias.setter
    def bias(self, value) -> None:
        self._bias = value

    @property
    def weights(self): # -> np.array
        return self._weights

    @weights.setter
    def weights(self, value) -> None:
        self._weights = value

    def forward_propagation(self, input) -> None:
        """
        Compute the output for the given input.

        (linear version)
        """
        self.input = input
        self.output = np.dot(self.input, self.weights) + self.bias

        return self.output

    def backward_propagation(self, output_error, learning_rate) -> None:
        """
        Compute the dE/dW dE/dB
        """
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)

        # So the dB = output_errors

        self.bias -= learning_rate * output_error
        self.weights -= learning_rate  * weights_error

        return input_error


class ActivationLayer(Layer):

    def __init__(self, activation: Callable, activation_derivative) -> None:
        super().__init__(None, None)
        self._activation = activation
        self._activation_derivative = activation_derivative

    @property
    def activation(self):
        return self._activation

    @property
    def activation_derivative(self):
        return self._activation_derivative

    def forward_propagation(self, input) -> None:
        self.input = input
        self.output = self.activation(self.input)
        return self.output

    def backward_propagation(self, output_error, learning_rate = None) -> None:
        return self.activation_derivative(self.input) * output_error


class Network:
    def __init__(self, loss, loss_der, *layers) -> None:
        """
        """
        self.loss = loss
        self.loss_der = loss_der
        self.layers = layers

    def train(self, x_train, y_train, epochs, learning_rate) -> None:
        """
        Train the network.
        """
        # The traning loop.
        for i in range(epochs): # tqdm()
            error_total = 0.0
            for j in range(len(x_train)):
                # Forward propagation.
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # Compute error (optional).
                error_total += self.loss(y_train[j], output)

                # Backward propagation.
                error = self.loss_der(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            end = "\n" if i == epochs - 1  else "\r"
            print(f"{i + 1}/{epochs}, {error_total / len(x_train)}", end=end)


    def predict(self, input) -> np.array:
        """
        Predict the values.
        """
        result = []
        for i in range(len(input)):
            output = input[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)
        return result



if __name__ == "__main__":

    print("Solving XOR problem")

    # Set the training data.
    x_train = np.array([
        [[0,0]], [[0,1]], [[1,0]], [[1,1]]
    ])

    y_train = np.array([
        [[0]], [[1]], [[1]], [[0]]
    ])

    net = Network(
        mse,
        mse_derivative,
        FullyConnectedLayer(2, 3),
        ActivationLayer(tanh, tanh_derivative),
        FullyConnectedLayer(3, 1),
        ActivationLayer(tanh, tanh_derivative)
    )

    net.train(x_train, y_train, epochs=10**3, learning_rate=0.1)

    print(
        f"output={net.predict(x_train)}"
    )

    # print("Solve the MNIST dataset")