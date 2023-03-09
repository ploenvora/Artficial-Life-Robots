# Final Project ʕ •ᴥ•ʔゝ☆ Science Option ʕ •ᴥ•ʔゝ☆

Generate a hypothesis and test it.

Expectations: Identify and investigate an interesting detail of evolution, morphology or behavioral control. Formulate a hypothesis and design a control experiment that isolates and interrogates this detail.

## Defining my hypothesis
<img width="800" alt="Screen Shot 2023-03-09 at 00 48 12" src="https://user-images.githubusercontent.com/63747047/223942773-0e9c558a-6339-489d-974f-2918a048e210.png">
<img width="800" alt="Screen Shot 2023-03-09 at 00 48 26" src="https://user-images.githubusercontent.com/63747047/223942807-c59549b0-6c31-49cf-92a6-595cec2cac28.png">

### Hypothesis: **Robots with hierarchical links, where the size of the parent link is consistently greater than that of the child link, have the ability to traverse greater distances compared to robots with links of cubic dimensions.**

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
The gif below shows a potential body/brain generation. It must be noted that although the link sizes here are integers (as links are constructed with cubes in the gif), the simulation link sizes can take on non-integer sizes. Blue links represent unsensored links and green represents sensored links. 

![ezgif com-crop](https://user-images.githubusercontent.com/63747047/221438685-99344543-7dd7-46a0-b1f7-5f54ff613c65.gif)

## How bodies and brains are mutated

For each mutation, there are 5 types of mutations it can undergo: 1) Remove a link, 2) Add a link, 3) Change a link's size, 4) Change a link's sensor senses and 5) Change a joint's axis.

1) Remove a link is simply removing a link that exists on the creature

![ezgif com-crop (4)](https://user-images.githubusercontent.com/63747047/221439442-70deb513-868c-4ca4-9c31-fe0311abed4e.gif)

2) Adding a link is adding a new link onto the creature

![ezgif com-crop (3)](https://user-images.githubusercontent.com/63747047/221439451-e03b7280-af7c-43c3-aea9-4a76d0d35f79.gif)

3) Changing a link's size is randomize picking a random link and changing it's width, height and length

![ezgif com-crop (2)](https://user-images.githubusercontent.com/63747047/221439462-78418948-07bc-4684-9937-7702b934087f.gif)

4) Changing a link's sensors is making it sensored if previously unsensored and making it unsensored if previously sensored!

![ezgif com-crop (1)](https://user-images.githubusercontent.com/63747047/221439457-5c933384-a028-42ef-9b93-3a404e7d6f25.gif)

5) Changing a joint's axis. There are 3 types of joint axis as mentioned above. Changing this just means changing the current axis to 1 out of the 2 other types of joint axis avaiable. It's difficult to create a diagram to show this but essentially, if its rotating in the x plane, it would be changed to rotate in the y or z plane, and so on.

## How to Run

Generate a random 3D creature by running search.py/main.py! :)

## Experiment
5 simulations were generated with a population of 50 and 100 mutational genenerations. For each simulation, for each generation, we computed the creature with the best fitness up until that generation. The fitness function here is the distance the robot can move in the -x direction, the robot that moved the most in the -x direction had the best fitness. The 5 simulations started from a different random seed (1,2,3,4,5) to ensure replicability. 

For this experiment, I started with numLinks between 5 - 20, linkSize between 0.3 - 1 and a motorRange of 0.35.

### Results

The results of the best fitness at each generation for each simulation (Seed 1 - 5) is show below:

<img width="651" alt="Screen Shot 2023-02-27 at 15 54 25" src="https://user-images.githubusercontent.com/63747047/221695172-d9ba5a15-604c-4450-9036-ec624ae6d681.png">

## Citation
Inspiration for this project from Ludobots MOOC and Karl Sims! :)

