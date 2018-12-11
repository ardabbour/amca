# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from gym.envs.registration import register

register(
    id='backgammon-v0',
    entry_point='amca.envs:BackgammonEnv',
)
