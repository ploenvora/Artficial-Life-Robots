# Assignment 8

Use the parallel hill climber to design morphology and behavior for locomotion.

## How bodies and brains are generated

The minimum and maximum number of links and the minimum and maximum link sizes can be set in Create_Body(). For each creature generated, the number of links, numLinks, is randomized.

### Initialization
1. For each creature, the starting link is centered at the origin. The size (width, length, height) of this starting link is randomized. 

### Generating body parts
2. After the starting link is generated, links are generated until the creature has generated numLinks links. To generate a new link, we must first randomize it's size. This is the same process as how we randomized the size of the starting link. 

3. Next, we must choose which link it is going to attach itself to. Let's call this the parentLink and the new link newLink. parentLink is a randomly chosen from the list of already generated links.

4. After parentLink is chosen, we then must choose which face of the parentLink the newLink is going to attach itself to. Here, we must make sure that the face we chose doesn't already have a link attach to it. If it does, we must chose a new face. If all faces of the parentLink has a link attached, then we must go back to step 3 and choose a new parentLink.

5. After choosing a face, we must make sure that the addition of this newLink doesn't overlap with other links. If it does, go back to step 2 and generate a newLink.

6. Once we have made sure we passed step 4 and 5, we can then generate the newLink as well as the joint that connects parentLink and newLink. There are 3 types of joints we can generate: 1) a revolute joint with axis (1, 0, 0), 2) a revolute joint with axis (0, 1, 0) and 3) a revolute joint with axis (0, 0, 1). Choosing a joint type is also a randomized process.

7. We must also randomized whether this new link has a sensor or not. There is a 50/50 chance it does/doesn't.

8. Repeat steps 2 - 7 over and over again until the number of links on the creater = numLinks!

9. For each creature, the synapse weights will be randomized!

10. You then have a creature with a randomized number of links, randomized link sizes, randomized positions, randomized joint rotations, randomized sensored links and randomized synapses! Yay!

### Example diagram of body/brain generation

## How bodies and brains are mutated

For each mutation, there are 4 types of mutations it can undergo: 1) Remove a link, 2) Add a link, 3) Change a link's size, 4) Change a link's sensor senses.

1) Remove a link is simply removing a link that exists on the creature

2) Adding a link is adding a new link onto the creature

3) Changing a link's size is randomize picking a random link and changing it's width, height and length

4) Changing a link's sensors is making it sensored if previously unsensored and making it unsensored if previosly sensored!

## How to Run

Generate a random 3D creature by running search.py/main.py! :)

## Credits and References
Thanks to Karl Sims

