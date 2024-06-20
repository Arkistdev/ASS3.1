import random
import numpy as np

from memory import Memory
from policy import Policy

import torch as pt


class Agent:
    def __init__(self, epsilon, policy) -> None:
        self.memory = Memory(100_000)
        self.policy = Policy(policy)
        self.moves = [0, 1, 2, 3]

        self.epsilon = epsilon

    def select_action(self, state):
        if random.random() <= self.epsilon:
            return random.choice(self.moves)
        else:
            return self.policy.select_action(state)

    def store_transition(self, transition):
        self.memory.store(transition)

    def train(self, learning_rate):
        samples = self.memory.sample(64)
        X = []
        Y = []

        for state, state_prime, reward, action in samples:
            if state_prime[6] == 1 and state_prime[7] == 1:
                a_value = reward
            else:
                q_prime = self.policy.forward(state_prime)
                a_prime = q_prime.index(max(q_prime))
                a_value = reward + (0.99 * q_prime[a_prime])

            q_state = self.policy.forward(state)

            q_state[action] = a_value
            X.append(state)
            Y.append(q_state)

        # Forward pass
        outputs_pred = self.policy.model(pt.Tensor(np.array(X)))

        # Compute loss
        loss = self.policy.loss(outputs_pred, pt.Tensor(Y))

        # Zero the gradients
        
        self.policy.optimizer.zero_grad()

        # Backward pass
        loss.backward()

        # Update weights
        self.policy.optimizer.step()

    def decay(self):
        self.epsilon = self.epsilon * 0.996
