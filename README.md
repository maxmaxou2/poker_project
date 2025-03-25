# PokerProject
Poker Bot, NFSP, Neural Network, Statistical Tools, and Computer Vision for Poker

DISCLAIMER : This code was written in 2023. I am no longer that shitty at python and package organizing.

Second, thanks to this research paper about poker bot interpretability (that gave me the clever and lightweight game state representation): https://rdcu.be/ee4uS

## Description

PokerProject is a comprehensive poker bot that integrates **Neural Networks**, **NFSP (Neural Fictitious Self-Play)**, **Computer Vision**, and **Monte Carlo simulations** to create an advanced poker-playing agent. This project also includes a **GUI** to visualize the game in real-time and statistical tools to analyze poker games. The bot learns autonomously and simulates games to improve its strategy, offering a powerful and immersive AI-powered poker experience. The bot doesn't work but was on it's way. Feel free to finish this project, but I offer you a solid theoric base even though the code is a bit old and shitty (I was still learning how to code in Python)

## Table of Contents
- [Demo](#demo)
- [Computer Vision for Card Detection](#computer-vision-for-card-detection)
- [Monte Carlo Probability Calculator](#monte-carlo-probability-calculator)
- [Theory Behind the Poker Bot](#theory-behind-the-poker-bot)
- [GUI Functionality](#gui-functionality)

---

## Demo


---

## Computer Vision for Card Detection

This project uses **computer vision** to detect cards on online poker tables (PokerStars, Winamax, etc.). Since the graphical user interface (GUI) of these platforms keeps the cards in fixed positions, the detection process is optimized for screen capture rather than live camera feeds.

### Detection Process

The system employs two separate neural network classifiers:

1. **Rank Classifier** – Identifies the card's rank (Ace, King, Queen, etc.).
2. **Suit Classifier** – Determines the card's suit (Hearts, Diamonds, Clubs, Spades).

Each classifier includes an **"unknown" category**, allowing the model to return no result when it's uncertain, reducing false detections.
The neural networks are resnet-18 trained via Pytorch and are stored in ONNX format for usage in production env.

### Configurable Capture Zones

To ensure accurate detection, the GUI lets users manually define **capture zones** on the screen. These zones correspond to player card positions and are analyzed by the neural networks to extract rank and suit information efficiently.

This setup allows for a robust and adaptable card recognition system without the challenges of real-world camera-based detection.

---

## Monte Carlo Probability Calculator

The **Monte Carlo** method is used to simulate and calculate probabilities for different poker scenarios. Here's how the calculator works:

- **Simulations**: The Monte Carlo calculator runs a series of random simulations of potential poker hands. It simulates the remaining cards that could be drawn and evaluates the outcome for each possible scenario.
- **Expected Value Calculation**: The system uses the results of these simulations to estimate the expected value (EV) of various actions (e.g., fold, call, raise) given the current state of the game.
- **Decision Making**: By simulating thousands (or even millions) of possible game outcomes, the bot can make more informed decisions, weighing the likelihood of winning against the potential risks.

This Monte Carlo-based approach helps the poker bot make decisions based on probability rather than purely relying on hardcoded strategies, making its gameplay more dynamic and adaptable.

The calculator is implemented as well in JAVA using multithreading to ensure efficiency, but running the JVM is costly/long at startup so use it wisely.
(The proposed Python implementation is still 10-100 times faster than open-source libraries found online, after benchmark. Source: TrustMe.com)

---

## Theory Behind the Poker Bot

The poker bot in this project is based on several advanced **AI and reinforcement learning** techniques. Below are some key ideas behind its design:

- **Neural Networks**: The bot uses deep neural networks to analyze and interpret the game state. The network processes inputs such as the current hand, opponent behavior, and betting patterns to determine the optimal move.

- **Game State**: The game state is defined/computed following one of the smartest papers I've ever read about poker bots addressing the problem of interpretability in poker : https://rdcu.be/ee4uS.
  
- **NFSP (Neural Fictitious Self-Play)**: NFSP is a reinforcement learning technique that allows the bot to learn from self-play. By playing against itself, the bot adapts to different poker strategies and refines its own approach. It uses both **regret minimization** and **policy gradient methods** to continuously improve its play.

- **Exploration vs. Exploitation**: During training, the bot balances exploration (trying new strategies) with exploitation (using the strategies that have worked well). This enables it to learn a wide range of poker strategies while also optimizing its decision-making over time.

- **Opponent Modeling**: The bot also tries to model its opponents, identifying patterns in their play to predict their future actions. This allows it to adjust its strategy based on the behavior of other players at the table.

These techniques combine to create a highly effective poker-playing agent that can adapt, learn, and make strategic decisions based on a variety of factors.

---

## GUI Functionality

- **Statistics Display**: The GUI includes live statistics on the bot’s performance, showing metrics like win rate, average hand strength, and more.

The interface is displayed as an overlay on top of the screen and is built using **Tkinter**, a lightweight Python library for creating graphical interfaces, which provides a simple way to visualize the poker game and track the bot’s performance.

---