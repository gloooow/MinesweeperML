import torch
import random
import numpy as np
from collections import deque
from main import Minesweeper
from model import Linear_QNet, QTrainer
from helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(1, 256, 5)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        # TODO: create model, trainer
    
    def get_state(self, game):
        state = [
            game.matrix[game.cursorPosition_x][game.cursorPosition_y]['first'] == 'cell.png',
        ]
        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if(len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        self.model.train()

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 4)
            final_move[move] = 1
        else:
            # get prediction from NN
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Minesweeper()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.move_cursor(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)
        game.main()

        if done:
            print('done')
            game.reset_game()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
