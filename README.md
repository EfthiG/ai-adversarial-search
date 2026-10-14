# Adversarial Search in Pacman

A Python university coursework project exploring **multi-agent decision-making** in the UC Berkeley CS188 Pacman environment. It implements reflex-based behavior and adversarial search strategies for Pacman navigating a maze with ghosts.

## Implemented agents and evaluation

| Question | Component | Description |
| --- | --- | --- |
| Q1 | `ReflexAgent` | Scores immediate successor states to select an action based on the current situation. |
| Q2 | `MinimaxAgent` | Searches a game tree with Pacman as the maximizing player and ghosts as minimizing players. |
| Q3 | `AlphaBetaAgent` | Uses alpha-beta pruning to avoid exploring branches that cannot change the minimax decision. |
| Q4 | `ExpectimaxAgent` | Models ghost moves as uniformly random and chooses actions using expected utility. |
| Q5 | `betterEvaluationFunction` | Evaluates game states using the game score and spatial information such as food and ghost distances. |

The main implementation is in **`multiAgents.py`**. The project supports multiple ghosts and configurable search depth through the provided game framework.

## Repository structure

```text
ai-adversarial-search/
├── multiAgents.py           # Coursework agents and evaluation functions
├── pacman.py                # Pacman game runner (educational framework)
├── game.py                  # Game-state and game mechanics (framework)
├── ghostAgents.py           # Ghost behavior (framework)
├── util.py                  # Supporting utilities (framework)
├── autograder.py            # Project test runner
├── layouts/                 # Pacman maze layouts
├── test_cases/              # Test suites q1–q5 and additional cases
│   ├── q1/
│   ├── q2/
│   ├── q3/
│   ├── q4/
│   └── q5/
└── ...                      # Other framework and grading support files
```

## Requirements

- Python 3
- The complete files from the submitted `multiagent` directory
- A graphical environment for visual gameplay (or use `-q` for a text-only run)

The project uses the educational Pacman framework supplied with the assignment.

## Run the agents

From the repository root:

```bash
# Reflex agent
python pacman.py -p ReflexAgent -l testClassic

# Minimax agent
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=2

# Alpha-beta pruning
python pacman.py -p AlphaBetaAgent -l smallClassic -a depth=2

# Expectimax agent
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=2

# Minimax with the improved evaluation function
python pacman.py -p MinimaxAgent -l smallClassic -a evalFn=better,depth=2
```

Search depth and layout can be changed to compare agent behavior. To run without graphics, add `-q` where supported by the Pacman runner.

## Automated tests

The submitted project includes the Berkeley-style autograder and test cases for questions Q1–Q5:

```bash
# Run all graded questions
python autograder.py

# Run one question
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
```

## Concepts demonstrated

- Reflex agents and state evaluation
- Multi-agent game trees
- Minimax decision-making
- Alpha-beta pruning
- Expectimax under stochastic opponent behavior
- Depth-limited search and heuristic evaluation

## Attribution

This project is based on the **UC Berkeley CS188 Pacman Projects** educational framework. The coursework contributions are concentrated in the designated implementation sections of `multiAgents.py`.

- [UC Berkeley CS188 — Project 2: Multi-Agent Search (Fall 2024)](https://inst.eecs.berkeley.edu/~cs188/fa24/projects/proj2/)
