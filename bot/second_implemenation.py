import os

import torch

import rlcard
from rlcard.agents import RandomAgent, NFSPAgent
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    reorganize,
    Logger,
    plot_curve,
)

def train():

    args = {'seed': 42,
            'env': "no-limit-holdem",
            'num_players': 2,
            'log_dir': "./log",
            'num_episodes': 10000,
            'algorithm':'nfsp',
            'evaluate_every': 500,
            'num_eval_games' : 100,
            'learn_type_change_ratio':0.01
        }

    # Check whether gpu is available
    device = get_device()
        
    # Seed numpy, torch, random
    set_seed(args['seed'])

    # Make the environment with seed
    env = rlcard.make(
        args['env'],
        config={
            'seed': args['seed'],
            'num_players': args['num_players']
        }
    )

    # Initialize the agent and use random agents as opponents
    agent = NFSPAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        hidden_layers_sizes=[1024]*5,
        q_mlp_layers=[512]*5,
        device=device,
    )
    agents = [agent]
    for _ in range(1, env.num_players):
        agents.append(RandomAgent(num_actions=env.num_actions))

    step_value = args['num_episodes']*args['learn_type_change_ratio']
    env.set_agents(agents)
    print(torch.cuda.is_available())
    # Start training
    with Logger(args['log_dir']) as logger:
        for episode in range(args['num_episodes']):

            agent.sample_episode_policy()

            # Alternate between self-play and supervised learning phases
            """if (episode//step_value)%2==0:
                # Self-play phase
                env.set_agents([agent for _ in range(env.num_players)])
                trajectories, payoffs = env.run(is_training=True)
                
            else:
                # Supervised learning phase
                env.set_agents(agents)"""
            trajectories, payoffs = env.run(is_training=True)
                
            trajectories = reorganize(trajectories, payoffs)
            for ts in trajectories[0]:
                agent.feed(ts)

            # Evaluate the performance. Play with random agents.
            if episode % args['evaluate_every'] == 0:
                logger.log_performance(
                    episode,
                    tournament(
                        env,
                        args['num_eval_games'],
                    )[0]
                )

        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, args['algorithm'])

    # Save model
    save_path = os.path.join(args['log_dir'], 'model.pth')
    torch.save(agent, save_path)
    print('Model saved in', save_path)

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = 'true'
    train()