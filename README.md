# 2-Agent Snake Game

## Description

## Dependencies and Module installation

1. Create virtual environment (tested with python 3.8.10)


    $ python3 -m venv venv
    
    $ source venv/bin/activate

2. Install dependencies


    $ pip install -r requirements.txt

## How to Run 

The project can be run with the command **python3 *snake-game.py* --agents arg1 --episodes arg2 --debug arg3**.

After the agent run is over you need to close the visual game window to properly end the process.

#### Flags and Arguments

**--agents** corresponds to the **type of agent** that will be created to explore the environment.
The possible values **arg1** can take are:

- <span style="color:blue">random</span>: Run **1 episode** of the environment with **2 random agents**
- <span style="color:blue">fully_greedy</span>: Run **1 episode** of the environment with **2 completely greedy agents** (go straight to their respective fruit)
- <span style="color:blue">part_greedy</span>: Run **1 episode** of the environment with **2 partially greedy agents** (go to their fruit while trying to dodge the other snake and itself)
- <span style="color:blue">all</span>: Run **_arg2_ episodes** of the environment with **different teams of agents** and **compare the results** obtained in terms of **score**, **number of steps**, **score efficiency** and **cause of death/loss**

**--episodes** corresponds to the **number of episodes** of the environment that will be considered to draw results from.
This argument should only be provided if you wish to run the environment with **all** teams of agents.
Even then, this is an **optional argument** and **arg2** can take **any positive integer**, with the **default being 30**.

**--debug** is an optional flag that is activated if **arg3** is set as <span style="color:blue">true</span>.
When activated the system outputs to the terminal information about the agents' observations and actions at eacht time step.
