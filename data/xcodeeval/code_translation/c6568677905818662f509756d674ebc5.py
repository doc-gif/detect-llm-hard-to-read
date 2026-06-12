
# coding: utf-8

# In[9]:




# In[42]:

line = input().split()

n = int(line[0])
h = int(line[1])
from math import log
array_nodes_minheigt = [[0 for x in range(36)] for y in range(36)]
array_nodes_minheigt[0][0] = 1
for nodes in range(1,36):
    for minheight in range(0,nodes+1):
        for topnode in range(1, nodes + 1):
            left = topnode-1
            right = nodes - topnode
            array_nodes_minheigt[nodes][minheight] += array_nodes_minheigt[left][0] * array_nodes_minheigt[right][0] -             (array_nodes_minheigt[left][0]-array_nodes_minheigt[left][max(minheight-1,0)])*             (array_nodes_minheigt[right][0]-array_nodes_minheigt[right][max(minheight-1,0)])


print(int(array_nodes_minheigt[n][h]))

