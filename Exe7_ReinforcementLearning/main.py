import gym
import numpy as np
import warnings

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers.legacy import Adam

from rl.agents import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

"""
Author
    Sebastian Mackiewicz - PJAIT student

Use Reinforcement Learning to build bot that will play games. In this scenario bot will be playing Acrobot on 
https://gymnasium.farama.org/environments/classic_control/acrobot/

Before running program install
pip install numpy
pip install pygame
pip install tensorflow
pip install keras-rl2
pip install gym

Make sure you have installed python at least in version 3.9
"""

warnings.filterwarnings("ignore", category=DeprecationWarning)

env = gym.make("Acrobot-v1")

states = env.observation_space.shape[0]
actions = env.action_space.n

model = Sequential()
model.add(Flatten(input_shape=(1, states)))
model.add(Dense(32, activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dense(actions, activation="linear"))

policy = EpsGreedyQPolicy(eps=0.1)

dqn_agent = DQNAgent(
    model=model,
    memory=SequentialMemory(limit=50000, window_length=1),
    policy=policy,
    nb_actions=actions,
    nb_steps_warmup=1000,
    target_model_update=0.001
)

dqn_agent.compile(optimizer=Adam(learning_rate=0.001), metrics=["mae"])
dqn_agent.fit(env, nb_steps=100000, visualize=True, verbose=1)

results = dqn_agent.test(env, nb_episodes=10, visualize=True)

print(np.mean(results.history["episode_reward"]))

env.close()

