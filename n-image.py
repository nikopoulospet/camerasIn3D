#!/usr/bin/python3
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
import math

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

def calc_parameters_camera2(points1n, points2n, P1, P2s):
    #P2s is the potental camera matrices for cam2 given we are at camera 1
    indx = -1

    for i, P2 in enumerate(P2s):
        #find the correct camera parameters
        d1 = structure.reconstruct_one_point(
            points1n[:,0], points2n[:,0], P1, P2)

        # Convert P2 from camera to world view
        P2_homogenous = np.linalg.inv(np.vstack([P2, [0,0,0,1]]))
        d2 = np.dot(P2_homogenous[:3, :4], d1)

        if d1[2] > 0 and d2[2] > 0:
            indx = i

    return indx

def filter_points(x,y,z):
    xnew, ynew, znew = [], [], []
    for i in range(len(x)):
        if math.sqrt((x[i]**2)+(y[i]**2)+(z[i]**2)) <= 1.0:
            xnew.append(x[i])
            ynew.append(y[i])
            znew.append(z[i])
    return xnew, ynew, znew

E = []
P = []
H = np.array([[1,0,0],[0,1,0],[0,0,1]])
X = []
Y = []
Z = []

for i in range(0,9):
    ii = i+2
    if(i > 9):
        istr = '0'+str(i)
    else:
        istr = '00'+str(i)

    if(ii > 9):
        iistr = '0'+str(ii)
    else:
        iistr = '00'+str(ii)

    path1 = 'data/viff.'+istr+'.ppm'
    path2 = 'data/viff.'+iistr+'.ppm'

    print(path1,path2)

    points1n, points2n, e = compute_essental(path1,path2)
    E.append(e)
    m1 = np.hstack((np.identity(3),np.zeros((3,1))))
    m2s = structure.compute_P_from_essential(e)
    # given we are at camera 1 calc params for camera 2
    # the following returns 4 possible camera matrices
    indx = calc_parameters_camera2(points1n, points2n, m1, m2s)
    if(indx == -1):
        print("invalid index on transform {}:{}".format(i,ii))
        continue

    m2 = np.linalg.inv(np.vstack([m2s[indx],[0,0,0,1]]))[:3,:4]
    print(m2s[indx],m2)
    pnts3D = structure.linear_triangulation(points1n,points2n,m1,m2)

    for i in range(len(pnts3D[0])):
        X.append(pnts3D[0][i])
        Y.append(pnts3D[1][i])
        Z.append(pnts3D[2][i])

X, Y, Z = filter_points(X,Y,Z)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(X,Y,Z)
plt.show()
