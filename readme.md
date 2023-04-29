# Optimized USC Path Finding

This is my variation on an A-star algorithm I call Q-star which first finds a good (but not necessarily optimal path) between two points and then uses that path to futility prune out future paths in order to efficiently search the entire tree and eventually find the best path quickly.

## Pruning Techniques

- ### Transpositional Pruning
    If we reach a node we've been at before and we reached it in the same amount or more steps, prune the subtree

- ### Futility Pruning
    If the length of our current path + the length of a straight line to the destination is greater than the length of the best path found, prune the subtree


## Examples

*The optimal route from Parkside to TCC after a completed search:*

![](https://media.discordapp.net/attachments/1101412775344996392/1101455297492557915/image.png)

*An incomplete search from Parkside to EVK:*

![](https://media.discordapp.net/attachments/1101412775344996392/1101426257532559401/image.png)