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
'''
takes the path of two images and computes corresponding points between them
returns corresponding points in each frame and intrinsic camera matrix
'''
def img_correspondances(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    pts1, pts2 = features.find_correspondence_points(img1, img2)
    points1 = processor.cart2hom(pts1)
    points2 = processor.cart2hom(pts2)

    height, width, ch = img1.shape
    intrinsic = np.array([  # for dino
        [2360, 0, width / 2],
        [0, 2360, height / 2],
        [0, 0, 1]])

    return points1, points2, intrinsic



def compute_essental(path1, path2):
    points1, points2, intrinsic = img_correspondances(path1, path2)

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
    return points1n, points2n, E




E = []
P = []
H = np.array([[1,0,0],[0,1,0],[0,0,1]])
X = []
Y = []
Z = []

for i in range(1,5):
    ii = i+1
    if(ii >= 4):
        ii = 1

    path1 = 'data/viff.00'+str(i)+'.ppm'
    path2 = 'data/viff.00'+str(ii)+'.ppm'

    print(path1,path2)

    points1n, points2n, e = compute_essental(path1,path2)
    E.append(e)
    P.append(structure.compute_P_from_essential(e))

    m1 = np.hstack((np.identity(3),np.zeros((3,1))))
    pnts3D = structure.linear_triangulation(points1n,points2n,m1,P[i-1][1])
    pnts3D = processor.hom2cart(pnts3D)

    print(pnts3D.shape)

    for i in range(len(pnts3D[0])):
        X.append(pnts3D[0][i])
        Y.append(pnts3D[1][i])
        Z.append(pnts3D[2][i])


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(X,Y,Z)
plt.show()
