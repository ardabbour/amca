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
- `Sarsa (Rummery and Niranjan)`_

The testing is done with the default parameters and implementations provided by
the `Stable Baselines`_ library.

Usage
-----

- **play.py**: to launch a game against a deep RL trained model. For example, ``python play.py ppo amca/models/amca.pkl`` will launch the model called ``amca.pkl`` that was trained using the PPO algorithm.
- **train.py**: to train an deep RL model (with default hyperparameters) to play. For example, ``python train.py -n terminator.pkl -a sac -t 1000000`` will train an agent called ``terminator.pkl`` using the SAC algorithm for 1000000 steps.
- **sarsa_play.py**: to launch a game against a SARSA trained model. ``python sarsa_play.py r2d2.pkl`` will launch the model called ``r2d2.pkl`` that was trained using the SARSA algorithm.
- **sarsa_train.py**: to train a model using SARSA. For example, ``python sarsa_train.py jarvis.pkl -g 10000`` will train an agent called ``jarvis.pkl`` using the SARSA algorithm for 10000 games.


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
.. _`Sarsa (Rummery and Niranjan)`: ftp://mi.eng.cam.ac.uk/pub/reports/auto-pdf/rummery_tr166.pdf
.. _GNU General Public License v3.0: /LICENSE
