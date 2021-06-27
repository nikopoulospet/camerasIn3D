### computing points in 3D space from two 2D images

General Process:

- compute correspondance points
- translate points into homogenous coordinates
- normalize points
- compute essential matrix from normalized points
- generate transformations between camera poses
  - pose one is [I|0]
  - pose two is computed from the essential matrix
- use normalized points and camera transforms to triagulate the corresponding 3D points
- display points in 3D scatter plot

#### starting images with computed correspondace points
![2d points](data/points2D.png)


#### final output of triangulated points in 3D space
![alt text](data/3D_plot.png)


#### The Essential matrix

###### What is an Essential matrix
The essential matrix is a 3x3 matrix that related corresponding points in stereo
images. The essential matrix assumes that cameras satisfy the pinhole camera
model. The essential matrix is the precursor to the fundamental matrix, which is
used to establish constraints between matching image points. The fundamental
matrix expands upon the essential matrix because it can be used for uncalibrated
cameras. 

###### Functional example
Lets assume that x and x' are points in img0 and img1. x and x' are normalized
homogenous points. If the following equation is satified then we can say that
x and x' correspond to the same point in 3D space.

**transpose(x') E x = 0**

###### Defining the essential matrix
Lets define y and y' as homogenous representations of the 2D image coordinates
of img0 and img1. Additionally, lets define x and x' as the proper 3D
coordinates but represented in different coordinate systems. Basically saying that x and
x' are the same point but neither are in a common frame. Assuming our cameras
are normalized, we can say that the only transformation between each coordinate
system is a translation and a rotation. We can then say that:

**x' = R (x - t)**

R is a 3x3 rotation matrix and t is a 3 vector. Given this we can define the
essential matrix as:

**E = R [t]x**

[t]x is the matrix representation of the cross product with t.

###### Solving with points


#### Method of computing pose two camera matrix from essential matrix


#### Method of triangulating points into 3D space

