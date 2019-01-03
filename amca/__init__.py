# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from gym.envs.registration import register

register(
    id='Backgammon-v0',
    entry_point='amca.envs:BackgammonRandomEnv',
)
register(
    id='Backgammon-v1',
    entry_point='amca.envs:BackgammonPolicyEnv',
)
register(
    id='Backgammon-v2',
    entry_point='amca.envs:BackgammonHumanEnv',
)
