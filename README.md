### computing points in 3D space from two 2D images

General Process:

- compute correspondance points
- translate points into homogenous coordinates
- normalize points
- compute essental matrix from normalized points
- generate transformations between camera poses
  - pose one is [I|0]
  - pose two is computed from the essental matrix
- use normalized points and camera transforms to triagulate the corresponding 3D points
- display points in 3D scatter plot

#### starting images with computed correspondace points
![2d points](data/points2D.png)


#### final output of triangulated points in 3D space
![alt text](data/3D_plot.png)


#### The Essental matrix

###### What is an Essental matrix
The essental matrix is a 3x3 matrix that related corresponding points in stereo
images. The essental matrix assumes that cameras satisfy the pinhole camera
model. The essental matrix is the precursor to the fundamental matrix, which is
used to establish constraints between matching image points. The fundamental
matrix expands upon the essental matrix because it can be used for uncalibrated
cameras. 

###### Functional example
Lets assume that x and x' are points in img0 and img1. x and x' are normalized
homogenous points. If the following equation is satified then we can say that
x and x' correspond to the same point in 3D space.

** transpose(x') E x = 0 **

###### Defining the Essental matrix


#### Method of computing pose two camera matrix from Essental matrix


#### Method of triangulating points into 3D space

