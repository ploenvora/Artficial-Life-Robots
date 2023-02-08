# Assignment 6

Create a program that generates a kinematic chain (a jointed, motorized, innervated, sensorized snake) with a random number of randomly shaped links with random sensor placement along the chain. Links with and without sensors should be colored green and blue, respectively.

## Method

The minimum and maximum number of links and the minimum and maximum link sizes can be set in Create_Body(). The number of links and the link sizes are then randomized. The number of sensors will be randomized with a random number generator, but will range around (mean(number of links) - 2, mean(number of links) + 2) - this is done so to avoid snakes with all sensored links or no sensored links. The weights are also randomly generated.

## How to Run

Generate a random snake bu running search.py!

