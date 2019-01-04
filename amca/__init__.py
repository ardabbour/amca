# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from gym.envs.registration import register

register(
    id='BackgammonPolicy-v0',
    entry_point='amca.envs:BackgammonPolicyEnv',
)
register(
    id='BackgammonHuman-v1',
    entry_point='amca.envs:BackgammonHumanEnv',
)

register(
    id='BackgammonPolicyContinuous-v0',
    entry_point='amca.envs:BackgammonPolicyContinuousEnv',
)

register(
    id='BackgammonHumanContinuous-v0',
    entry_point='amca.envs:BackgammonHumanContinuousEnv',
)
