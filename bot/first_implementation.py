''' An example of playing randomly in RLCard
'''
import argparse
import pprint

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import set_seed

def run():
    # Make environment
    seed = 42

    env = rlcard.make(
        'no-limit-holdem',
        config={
            'seed': seed,
        }
    )

    # Seed numpy, torch, random
    set_seed(seed)

    # Set agents
    agent = RandomAgent(num_actions=env.num_actions)
    env.set_agents([agent for _ in range(env.num_players)])

    # Generate data from the environment
    trajectories, player_wins = env.run(is_training=False)
    # Print out the trajectories
    print('\nTrajectories:')
    print(trajectories)
    print('\nSample raw observation:')
    pprint.pprint(trajectories[0][0]['raw_obs'])
    print('\nSample raw legal_actions:')
    pprint.pprint(trajectories[0][0]['raw_legal_actions'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Random example in RLCard")
    parser.add_argument(
        '--env',
        type=str,
        default='leduc-holdem',
        choices=[
            'blackjack',
            'leduc-holdem',
            'limit-holdem',
            'doudizhu',
            'mahjong',
            'no-limit-holdem',
            'uno',
            'gin-rummy',
            'bridge',
        ],
    )

    args = parser.parse_args()

    #run(args)



import rlcard
from rlcard.agents import DQNAgent

# Step 1: Set a global seed for reproducibility
# Step 2: Initialize the environment
seed = 42

env = rlcard.make('no-limit-holdem', config={'num_players': 3, 'seed': seed})

print(env.actions)
# Step 3: Define the neural network architecture
agent = DQNAgent(scope='dqn',
                  action_num=env.action_num,
                  replay_memory_size=10000,
                  replay_memory_init_size=1000,
                  update_target_estimator_every=100,
                  epsilon_start=0.1,
                  epsilon_end=0.01,
                  epsilon_decay_steps=10000,
                  learning_rate=0.2,
                  discount_factor=0.9,
                  batch_size=32)

# Step 4: Train the agents
num_episodes = 10000

for episode in range(num_episodes):
    # Reset the environment for a new episode
    state = env.reset()

    while not env.is_over():
        # Choose actions for each player using the agent's policy
        action_dict = {}
        for player_id in range(env.player_num):
            if player_id in state['legal_actions']:
                action = agent.step(state)
            else:
                action = state['legal_actions'][0]  # Choose the first legal action if agent is not in the game
            action_dict[player_id] = action

        # Inside the training loop
        next_state, reward, done, _ = env.step(action_dict)


        # Collect experiences and train the agent
        for player_id in range(env.player_num):
            if player_id in state['legal_actions']:
                agent.feed(state, action_dict[player_id], reward[player_id], next_state, done[player_id])

        state = next_state

# Step 5: Save the trained model
agent.save()  # Save the trained DQN agent

# Step 6: Evaluation (You can perform evaluation after training)
# Here, you can evaluate the trained agent against other opponents or predefined strategies
# You can also load the trained agent using agent.load() and use it for evaluation
