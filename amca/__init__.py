# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from gym.envs.registration import register

register(
    id='BackgammonHumanEnv-v0',
    entry_point='amca.envs:BackgammonHumanEnv',
)
register(
    id='BackgammonPolicyEnv-v0',
    entry_point='amca.envs:BackgammonPolicyEnv',
)
register(
    id='BackgammonRandomEnv-v0',
    entry_point='amca.envs:BackgammonRandomEnv',
)
register(
    id='BackgammonRandomContinuousEnv-v0',
    entry_point='amca.envs:BackgammonRandomContinuousEnv',
)