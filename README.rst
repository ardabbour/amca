Amca
====

**Status: Under construction.**

Amca is an RL-based `Backgammon`_ agent.

Dependencies
------------

+---------------------+-------------------+
| Dependency          | Version Tested On |
+=====================+===================+
| `Ubuntu`_           |             16.04 |
+---------------------+-------------------+
| `Python`_           |             3.6.8 |
+---------------------+-------------------+
| `numpy`_            |            1.15.4 |
+---------------------+-------------------+
| `gym`_              |            0.10.9 |
+---------------------+-------------------+
| `Stable Baselines`_ |            2.4.0a |
+---------------------+-------------------+


About
-----

This project aims to design `Backgammon`_ as a reinforcement learning problem, 
and gauge the performance of common deep reinforcement learning algorithms. This
is done by training and gauging the performance of three popular and powerful RL
algorithms:

- `Deep Q Network (Mnih et. al)`_
- `Proximal Policy Optimization (Schulman et. al)`_
- `Soft Actor-Critic (Haarnoja et. al)`_

The testing is done with the default parameters and implementations provided by
the `Stable Baselines`_ library.

Usage
-----

There are two main scripts given:

- **play.py**: to launch a game against a trained agent. For example, ``python play.py ppo amca/agents/amca.pkl`` will launch the agent called ``amca.pkl`` that was trained using the PPO algorithm.

- **train.py**: to train an agent (with default hyperparameters) to play. For example, ``python train.py -n terminator -a sac -t 10000000`` will train an agent called ``terminator.pkl`` using the SAC algorithm for 10000000 timesteps.


License
-------

`GNU General Public License v3.0`_

.. _Ubuntu: https://www.ubuntu.com/
.. _Python: https://www.python.org/
.. _numpy: https://www.numpy.org/
.. _gym: https://gym.openai.com/
.. _Stable Baselines: https://stable-baselines.readthedocs.io/
.. _Backgammon: https://en.wikipedia.org/wiki/Backgammon/
.. _Deep Q Network (Mnih et. al): https://arxiv.org/abs/1312.5602/
.. _Proximal Policy Optimization (Schulman et. al): https://arxiv.org/abs/1707.06347/
.. _Soft Actor-Critic (Haarnoja et. al): https://arxiv.org/abs/1812.05905/
.. _GNU General Public License v3.0: /LICENSE
