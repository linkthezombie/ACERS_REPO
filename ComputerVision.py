"""
ComputerVision.py

Interface to get card information from the robot's cameras

Created by Liam McKinney

Created 10/12/2023
Revised 10/19/2023
    -Added comments (Liam McKinney)
Revised 11/10/2023
    -Added feature to scan in Aruco marker ids and convert them to card suits and values (Nathan Smith)
Revised 11/13/2023
    -Altered the way ids are returned in getCardSpecs (Nathan Smith)
"""

from CameraCalibration import *
from naoqi import ALProxy
import motion
import RobotInfo
import atexit
import areas
from positioning import Pose
from positioning import Orientation
from positioning import Vector3D
import cv2
import cv2.aruco as aruco

# conversion rate from inches to meters
kInchesToMeters = .0254
# matrix to translate opencv coordinates to nao coordinates
CvToNao = np.array([[ 0, 0, 1],
                    [-1, 0, 0],
                    [ 0,-1, 0]])

# set up proxies to the robot, subscribe to the camera
def init():
    global camera
    global body
    camera = ALProxy("ALVideoDevice", RobotInfo.getRobotIP(), RobotInfo.getPort())
    body = ALProxy("ALMotion", RobotInfo.getRobotIP(), RobotInfo.getPort())

    #use the mouth camera at maximum resolution in RGB at the lowest fps
    bottomCamera = 1
    res1280x960 = 3
    RGBColorspace = 11
    fps = 5

    #remember the name of our subscription so we can unsubscribe later
    global name
    name = camera.subscribeCamera("ArucoVision", bottomCamera, res1280x960, RGBColorspace, fps)

# clean up any ALProxy subscriptions or other resources we may have allocated
def deinit():
    camera.unsubscribe(name)

# returns ids, marker locations (in torso space), rotation matrices (in torso space)
# The columns of the rotation matrix form an orthonormal basis of the marker's coordinate space.
# The first column points from the center of the mark to the top of the card, the second to the right,
# and the third points out of the card (i.e. the normal vector to the card)
def getVisibleCards():
    naoImg = camera.getImageRemote(name)

    #convert image data to a numpy array opencv can use
    img = np.array(bytearray(naoImg[6]), dtype="uint8").reshape(naoImg[1], naoImg[0], 3)

    #convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #detect marker locations in the image
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict,
                                                          parameters=parameters)
    
    if( ids is None ):
        return [], [], []
    
    # SUB PIXEL DETECTION
    # For each marker, refine the corner locations beyond just integer coordinates
    # stop at 100 iterations, or when the corner position changes by less than .0001
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
    for markerCorners in corners:
        cv2.cornerSubPix(gray, markerCorners, winSize = (3,3), zeroZone = (-1,-1), criteria = criteria)
    
    size_of_marker = 0.75 # side length of the marker in inches

    # get position & orientation of the detected markers in 3d space
    # rvecs & tvecs are arrays of column vectors, i.e. tvecs[i] = [ [x], [y], [z] ]
    rvecs,tvecs,_ = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameraMtx, distortionCoeffs)

    frame = motion.FRAME_TORSO
    useSensorValues = True

    # transformation mtx of camera frame in torso frame (in meters)
    T_CT = np.array( body.getTransform("CameraBottom", frame, useSensorValues) ).reshape(4,4)
    
    xs = []
    Rs = []
    # translate each opencv rvec/tvec pair into a rotation matrix and position in Nao's robot space
    for i in range(len(rvecs)):
        # rvecs[i] is a vector parallel to the axis of rotation, with norm equal to the magnitude of rotation.
        # this isn't useful, so we convert it to a rotation matrix.

        # get opencv rotation mtx of the marker in camera space, then translate to Nao coordinate order
        rmat, _ = cv2.Rodrigues( rvecs[i] )
        # Rotation matrix of the marker in camera space (CvToNao reorders coordinates and changes sign to list them in Nao order)
        R_MC = np.matmul( CvToNao, rmat )

        # reorder tvec coordinates to be consistent with Nao coordinates, then convert from inches to meters
        # position of the marker in camera space
        x_MC = np.matmul( CvToNao, tvecs[i].T ) * kInchesToMeters

        # "glue" R_MC and x_MC together to get a 4x4 transformation mtx
        # of the marker in camera space
        T_MC = np.block([[R_MC, x_MC], [np.zeros((1,3)), np.ones((1,1))]])

        # compose the two transformation matrices to get the
        # transformation mtx of the marker in torso space.
        T_MT = np.matmul( T_CT, T_MC )

        # extract rotation matrix and position vector of the marker in torso space
        # from the transformation matrix, and add them to the list
        Rs.append(T_MT[:3,:3])
        xs.append(T_MT[:3,3])
    return ids, xs, Rs

# Takes the marker ids, and determines the suit and rank of the card that id represents
def getTopCard(marker_ids, xs, Rs):
    for id in marker_ids:
        pose = Pose.Pose(Vector3D.Vector3D(xs[id]), Orientation.Orientation.fromRotationMatrix(Rs[id]))
        if areas.findPlayArea(pose) == "discard pile":
            rank = (id % 13) + 1
            suit = id // 13
            return((rank, suit))
    return None

# Takes the marker ids, and determines the suit and rank of the card that id represents
def getDrawnCard(marker_ids, xs, Rs):
    for id in marker_ids:
        pose = Pose.Pose(Vector3D.Vector3D(xs[id]), Orientation.Orientation.fromRotationMatrix(Rs[id]))
        if areas.findPlayArea(pose) == "in your face":
            rank = (id % 13) + 1
            suit = id // 13
            return((rank, suit))
    return None


# run some initialization the first time this module is imported
init()

# unsubscribe/free resources when the program exits (whether normally or from an error)
atexit.register(deinit)

# debugging loop to print the position and normal vector of aruco marker 0
if __name__ == "__main__":
    while True:
        ids, xs, Rs = getVisibleCards()

        if(ids is None):
            print("No markers visible!")
        zeroFound = False
        for i in range(len(ids)):
            if ids[i] == 0:
                print("posn: %s, norm: %s" % (xs[i], Rs[i][:,3]))
        if not zeroFound:
            print("Marker 0 not visible!")
