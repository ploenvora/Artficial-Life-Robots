# Final Project ʕ •ᴥ•ʔゝ☆ Science Option ʕ •ᴥ•ʔゝ☆

Generate a hypothesis and test it.

Expectations: Identify and investigate an interesting detail of evolution, morphology or behavioral control. Formulate a hypothesis and design a control experiment that isolates and interrogates this detail.

## Defining my hypothesis
<img width="800" alt="Screen Shot 2023-03-09 at 01 29 07" src="https://user-images.githubusercontent.com/63747047/223951710-61052903-c208-4ee6-a891-c81941695255.png">
<img width="800" alt="Screen Shot 2023-03-09 at 21 39 02" src="https://user-images.githubusercontent.com/63747047/224217512-07e3cdf2-9fdc-4df5-9380-d0b37bd6d493.png">

### Hypothesis: 
Robots with hierarchical links, where the size of the parent link is consistently greater than that of the child link, have the ability to traverse greater distances compared to robots with links of cubic dimensions.

## Creating my variations

### Groups
Control Group (A) will have robots with cubic links. Experiment Group (B) will have robots with hierarchical links, where the size of the parent link is consistently greater than that of the child link.

## Group A: How bodies and brains are generated - Control (Cubic Links)

The minimum and maximum number of links and the minimum and maximum link sizes can be set in Create_Body(). For each creature generated, the number of links, numLinks, is randomized.

### Initialization
1. For each creature, the starting link is centered at the origin. The size (width, length, height) of this starting link is (1, 1, 1). All links generated for this robot will have the size of (1, 1, 1). After the starting link is generated, links will be generated until the creature has generated numLinks links.

### Generating body parts

2. Generate a new link! Since this is the control experiment, the link will have size (1, 1, 1).

3. Next, we must choose which link it is going to attach itself to. Let's call this the parentLink and the new link newLink. parentLink is randomly chosen from the list of already generated links.

4. After parentLink is chosen, we then must choose which face of the parentLink the newLink is going to attach itself to. Here, we must make sure that the face we chose doesn't already have a link attach to it. If it does, we must chose a new face. If all faces of the parentLink has a link attached, then we must go back to step 3 and choose a new parentLink.

5. After choosing a face, we must make sure that the addition of this newLink doesn't overlap with other links. If it does, go back to step 2 and generate a newLink.

6. Once we have made sure we passed step 4 and 5, we can then generate the newLink as well as the joint that connects parentLink and newLink. There are 3 types of joints we can generate: 1) a revolute joint with axis (1, 0, 0), 2) a revolute joint with axis (0, 1, 0) and 3) a revolute joint with axis (0, 0, 1). Choosing a joint type is also a randomized process.

7. We must also randomized whether this new link has a sensor or not. There is a 50/50 chance it does/doesn't.

8. Repeat steps 2 - 7 over and over again until the number of links on the creater = numLinks!

9. For each creature, the synapse weights will be randomized!

10. You then have a creature with a randomized number of links, randomized positions, randomized joint rotations, randomized sensored links and randomized synapses! Yay!

## Group B: How bodies and brains are generated - Experiment (Hierarchical Links)

The minimum and maximum number of links and the minimum and maximum link sizes can be set in Create_Body(). For each creature generated, the number of links, numLinks, is randomized.

### Initialization
1. For each creature, the starting link is centered at the origin. The size (width, length, height) of this starting link is randomized between 0.3 - 1.

### Generating body parts
2. After the starting link is generated, links will be generated until the creature has generated numLinks links. Before generating a new link, we must choose which link it is going to attach itself to. Let's call this the parentLink and the new link newLink. parentLink is a randomly chosen from the list of already generated links.

3. Next, we must first randomize the newLink's size. This is the same process as how we randomized the size of the starting link, however, there is a constraint. A new link generated must have a smaller size than its parent link.

4. After we have generated a new link, we then must choose which face of the parentLink the newLink is going to attach itself to. Here, we must make sure that the face we chose doesn't already have a link attach to it. If it does, we must chose a new face. If all faces of the parentLink has a link attached, then we must go back to step 3 and choose a new parentLink.

5. After choosing a face, we must make sure that the addition of this newLink doesn't overlap with other links. If it does, go back to step 2 and generate a newLink.

6. Once we have made sure we passed step 4 and 5, we can then generate the newLink as well as the joint that connects parentLink and newLink. There are 3 types of joints we can generate: 1) a revolute joint with axis (1, 0, 0), 2) a revolute joint with axis (0, 1, 0) and 3) a revolute joint with axis (0, 0, 1). Choosing a joint type is also a randomized process.

7. We must also randomized whether this new link has a sensor or not. There is a 50/50 chance it does/doesn't.

8. Repeat steps 2 - 7 over and over again until the number of links on the creater = numLinks!

9. For each creature, the synapse weights will be randomized!

10. You then have a creature with a randomized number of links, randomized link sizes, randomized positions, randomized joint rotations, randomized sensored links and randomized synapses! Yay!

## Body and Brain Generation Diagram
<img width="800" alt="Screen Shot 2023-03-09 at 16 10 45" src="https://user-images.githubusercontent.com/63747047/224172100-c86d05bf-bf3f-42c0-94a7-e1731ff2fd07.png">

## Sample Size
I will create 25,000 simulations for each group. Each group will have 5 runs. Each run starts with a population size of 10 and evolve for 100 generations

## Mutation over generations
Each child differs from it's parent due to mutation, there are 5 types of mutations it can undergo: 1) Remove a link, 2) Add a link, 3) Change a link's size (This is not applicable for the control group), 4) Change a link's sensor senses and 5) Change a joint's axis.

1) Remove a link is simply removing a link that exists on the creature

![ezgif com-crop (4)](https://user-images.githubusercontent.com/63747047/221439442-70deb513-868c-4ca4-9c31-fe0311abed4e.gif)

2) Adding a link is adding a new link onto the creature

![ezgif com-crop (3)](https://user-images.githubusercontent.com/63747047/221439451-e03b7280-af7c-43c3-aea9-4a76d0d35f79.gif)

3) Changing a link's size is randomize picking a random link and changing it's width, height and length

![ezgif com-crop (2)](https://user-images.githubusercontent.com/63747047/221439462-78418948-07bc-4684-9937-7702b934087f.gif)

4) Changing a link's sensors is making it sensored if previously unsensored and making it unsensored if previously sensored!

![ezgif com-crop (1)](https://user-images.githubusercontent.com/63747047/221439457-5c933384-a028-42ef-9b93-3a404e7d6f25.gif)

5) Changing a joint's axis. There are 3 types of joint axis as mentioned above. Changing this just means changing the current axis to 1 out of the 2 other types of joint axis avaiable. It's difficult to create a diagram to show this but essentially, if its rotating in the x plane, it would be changed to rotate in the y or z plane, and so on.

### How mutations for Group A and B differ
For group A, all links are sized (1, 1, 1) while for group B, all links are randomized between 0.3 - 1 with the exception that parent links must always be bigger than the child link. In terms of mutation, both groups will mutate in the same manner as we are using the same random seed for each group's 5 runs. The only difference is that when robots in Group A undergo the Change_Size mutation, nothing happens! :) 

## Selection
The selection process of best fitness robots is illustrated in the "Defining my hypothesis" section's diagram above. It essentially follows the parallel hill climber algorithm from the Ludobots MOOC. 

## Testing Metric (Fitness Function)
The fitness function, which acts as an A/B testing metric, here is the distance the robot can move in the -x direction, the robot that moved the most in the -x direction had the best fitness.

## Experimental Method (also can be used for running during grading)
For the control group, change sizeMin and sizeMax in constants.py to 1. Then, uncomment the first line of the Change_Size function in solution.py - this should uncomment out the "return" This ensures that our random seed for both groups generate the same robot with only one thing changed - size.

For the experiment group, change sizeMin and sizeMax in the constants.py to 0.3 and 1, respectively. If the first line of the Change_Size function in solution.py is uncomment, comment this out.

Generate 5 runs with 100 generations and 10 starting parent with your group of choice (control v.s. experiment) by running search.py/main.py! :)
The number of generations and population size can be changed in constants.py.

## Results

## Discussion and Conclusion




