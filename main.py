#!/usr/bin/python3
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2

from camera import Camera
import structure
import processor
import features

# Download images from http://www.robots.ox.ac.uk/~vgg/data/mview/
matplotlib.use("TkAgg")

def dino():
    # Dino
    img1 = cv2.imread('data/viff.003.ppm')
    img2 = cv2.imread('data/viff.001.ppm')
    pts1, pts2 = features.find_correspondence_points(img1, img2)
    points1 = processor.cart2hom(pts1)
    points2 = processor.cart2hom(pts2)

    fig, ax = plt.subplots(1, 2)
    ax[0].autoscale_view('tight')
    ax[0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    ax[0].plot(points1[0], points1[1], 'r.')
    ax[1].autoscale_view('tight')
    ax[1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    ax[1].plot(points2[0], points2[1], 'r.')
    plt.show()
    print(matplotlib.backends.backend)

    height, width, ch = img1.shape
    intrinsic = np.array([  # for dino
        [2360, 0, width / 2],
        [0, 2360, height / 2],
        [0, 0, 1]])

    return points1, points2, intrinsic


points1, points2, intrinsic = dino()
# Calculate essential matrix with 2d points.
# Result will be up to a scale
# First, normalize points
points1n = np.dot(np.linalg.inv(intrinsic), points1)
points2n = np.dot(np.linalg.inv(intrinsic), points2)

#TODO
# calculate essential matrix
E = structure.compute_essential_normalized(points1n,points2n)

#print essential matrix
print(E)

#display of the cameras in 3D space
m1= np.hstack((np.identity(3),np.zeros((3,1))))
m2 = structure.compute_P_from_essential(E)
pnts3D = structure.linear_triangulation(points1n,points2n,m1,m2[1])
pnts3D = processor.hom2cart(pnts3D)
x = pnts3D[0]
y = pnts3D[1]
z = pnts3D[2]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x,y,z)
plt.show()
