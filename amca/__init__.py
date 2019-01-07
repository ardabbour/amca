# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from gym.envs.registration import register

register(
    id='BackgammonHuman-v0',
    entry_point='amca.envs:BackgammonHumanOpponentEnv',
)
# register(
#     id='BackgammonPolicy-v0',
#     entry_point='amca.envs:BackgammonPolicyOpponentEnv',
# )
register(
    id='BackgammonRandom-v0',
    entry_point='amca.envs:BackgammonRandomOpponentEnv',
)
