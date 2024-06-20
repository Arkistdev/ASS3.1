from transition import Transition
from collections import deque 
import random


class Memory:
    def __init__(self):
        self.transition_deque = deque() 

    def store(self, transition: Transition):
        self.transition_deque.append(transition)
        return

    def sample(self, batch_size):
        batch = random.sample(list(self.transition_deque), batch_size)
        return batch