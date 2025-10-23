# Robot Localization - Particle Filter
**Authors:** Dhvan Shah and Bhargavi Deshpande

## Project Goal:
The goal of this project was for a Neato placed at an unknown point on a known map to determine its location within said map using a particle filtering algorithm. We want to minimize the robot’s uncertainty in location and converge on an accurate point within the map.

## Problem Solving and Implementation:
We used a particle filtering algorithm for robot localization to have the robot converge at its location within the known map. The particle filtering algorithm begins by distributing particles at random (x, y, theta) points across the known map. A gaussian (normal) distribution was used to create the initial spread of particles around an initialized (x, y, theta) position, set by us. 

The algorithm then takes the LiDAR scan of the real robot at an unknown point in the map and determines the distance the robot is from its closest obstacle (the minimum LiDAR distance value). Each particle also has a hypothetical LiDAR scan that collects the particle’s minimum distance from an object. After those values are compared, the closer the particle’s distance value is to the robot’s distance value, the 
higher that particle was weighted: Weight = 1.0|Error|, where Error is the difference in minimum lidar distance. Finally we normalized this particle cloud so that the weights all add up to 1.

We then re-sampled our particles. To resample, we picked 75% of our particle population to sample from, and then randomly picked particles from that population, but accounting for the weight. So a higher weighted particle was more likely to be picked. We used a uniform random distribution to send out 25% of the particle population to avoid falsely converging on an incorrect point. We added some random linear noise to all particles after resampling to help us converge on the right point.

As neato’s position in the bag file updates, the process repeats itself and the particles continue to resample and converge with the robot’s real position.

## Key Design Decision 
One design decision we had to make was determining if we wanted to send out random particles away from the initial particle cloud. Since the bag files we were given started the robot at the origin of the map, our particle filter converged quickly, since the initial position was set to be 0, 0 on the map. When we were doing analysis of our filter, we realized that it probably wouldn’t converge if the initial position was far from the estimated initial position. This led to our design decision to send out uniformly random particles every timestep.

In this step, we also had to decide the percentage of particles that we were distributing randomly. We started off with 50% of the particle cloud being randomly distributed particles, and quickly turned that percentage down to 25%. We found that this was a nice balance between converging on the real position of the robot and verifying that we are not converging on an incorrect position.

## Challenges

The biggest challenge we had was while working with rviz. When running the bag file and the MAC map in rviz, the neato visual was not appearing on screen. Our particles would populate within the MAC map and when we echoed the /odom topic to verify that the bag file was playing and the Neato was moving. This made it difficult to understand the accuracy of our pose estimate since we couldn’t visually see where the Neato was in reference to the map.

Initially, the map to odom transform wasn’t being published by the launch cycle, which was why the odom data wasn’t appearing on the map frame. This was a symptom of some small launch file bugs, where the map server wasn’t always running leading to some visualization issues. We solved this by adjusting the launch file to publish an empty map server if one doesn’t exist, which solved our problems and we were able to confirm that our particle cloud is working.

## Future Project Improvements
If we had more time we would want to determine a method to incorporate more than one ray of LiDAR scan to compare. Instead of looking at the minimum distance to  the closest object, it would be much more accurate to compare a spread of distances or features from a LiDAR scan for each particle and the robot. Thus, we would be able to differentiate whether the object directly in front of a particle was the same object that was in front of the robot or if they were just similar distances away. However, this would have made our code much more complex and it didn’t seem achievable for the scope of this project. 

## Interesting Robotics Lessons
One thing we learned was how different it is to start a robotic programming project from starter code rather than from scratch. While it is really helpful to have a basis of code that we know works and can be a great starting point for us, if we don’t take the time to fully understand all the functions and properties that have already been created we risk creating contradictory or significantly less efficient functions and processes. Additionally, working off a starter code made us switch our mindset from “how do we make a particle function that works?” to “how do we make this code work”, which we thought was an interesting shift.
