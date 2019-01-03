# import gym
from gym import spaces
import numpy as np

lower_bound = np.array([1, ]*2 + [0, ]*52)
upper_bound = np.array(
    [6, ]*2 + [16, ]*4 + [item for sublist in [[3, 16], ]*24 for item in sublist])
space = spaces.Box(low=lower_bound, high=upper_bound,
                   dtype=np.float32)

print(space.sample())

# import numpy as np
# mylist = [[16, 16],  # bourne off checkers for white/black
#           [16, 16],  # hit checkers for white/black
#           [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16],
#           [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16],
#           [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16],
#           [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16]]


# mylist1 = np.array([0, ]*52)
# mylist2 = np.array([16, ]*4 + [item for sublist in [[3, 16],]*24 for item in sublist])
# print(len(mylist2))

# print(mylist1.shape)
# print(mylist2.shape)

# print(mylist2)
# mylist = np.array(mylist)
# print(mylist1 + mylist2)
# print(len(np.array(mylist).flatten()))
