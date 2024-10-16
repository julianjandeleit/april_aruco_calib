import os
import numpy as np
import cv2
import json 
import pathlib
# from https://medium.com/@nflorent7/a-comprehensive-guide-to-camera-calibration-using-charuco-boards-and-opencv-for-perspective-9a0fa71ada5f

# ------------------------------
# ENTER YOUR REQUIREMENTS HERE:
ARUCO_DICT = cv2.aruco.DICT_4X4_50
SQUARES_VERTICALLY = 5
SQUARES_HORIZONTALLY = 7
#SQUARE_LENGTH = 0.03  # in meters
#MARKER_LENGTH = 0.015  # in meters
SQUARE_LENGTH = 0.055 # in meters
MARKER_LENGTH = 0.04  # in meters
# ...
#PATH_TO_YOUR_IMAGES = 'testdata/charuco_calib_set_1/'
PATH_TO_YOUR_IMAGES = 'testdata/charuco_calib_gopro_max_100/'
#ecl_list = ["GOPR0026.JPG"]
ecl_list  = ["GS__0010_90.JPG", "GS__0014_90.JPG"]
print(f"{ARUCO_DICT=}")
# ------------------------------
def get_calibration_parameters(img_dir, exclude_list=["GOPR0026.JPG"]):
    # Define the aruco dictionary, charuco board and detector
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)
    
    # Load images from directory
    image_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(".JPG")]
    image_files = [imf for imf in image_files if pathlib.Path(imf).name not in exclude_list]
    #print(image_files)
    print(f"excluding {exclude_list}")

    all_charuco_ids = []
    all_charuco_corners = []

    # Loop over images and extraction of corners
    for image_file in image_files:
        print(image_file)
        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgSize = image.shape
        image_copy = image.copy()
        marker_corners, marker_ids, rejectedCandidates = detector.detectMarkers(image)
        
        if marker_ids is not None and len(marker_ids) > 0: # If at least one marker is detected
            # cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
            ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
            #print(ret, charucoCorners, charucoIds, marker_ids)
            if charucoIds is not None and len(charucoCorners) > 3:
                all_charuco_corners.append(charucoCorners)
                all_charuco_ids.append(charucoIds)
            else:
                print("ids not determined")
        else:
            print("no markers found")
    if len(all_charuco_corners) == 0:
        print("no corners detected at all")
        return None
    # Calibrate camera with extracted information
    result, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board, imgSize, None, None)
    return mtx, dist

SENSOR = 'gopro_2'
LENS = 'gopro_2'
OUTPUT_JSON = 'calibration.json'

ret = get_calibration_parameters(img_dir=PATH_TO_YOUR_IMAGES, exclude_list=ecl_list)
if ret is None:
    print("no calibration could be estimated")
    exit(1)
mtx, dist = ret
data = {"sensor": SENSOR, "lens": LENS, "mtx": mtx.tolist(), "dist": dist.tolist()}

with open(OUTPUT_JSON, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f'Data has been saved to {OUTPUT_JSON}')

json_file_path = './calibration.json'

# with open(json_file_path, 'r') as file: # Read the JSON file
#     json_data = json.load(file)

# mtx = np.array(json_data['mtx'])
# dst = np.array(json_data['dist'])

# image_path = [os.path.join(PATH_TO_YOUR_IMAGES, f) for f in os.listdir(PATH_TO_YOUR_IMAGES) if f.endswith(".JPG")][0] # NOTE select image to calculate size
# image = cv2.imread(image_path)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# h,  w = image.shape[:2]
# newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dst, (w,h), 1, (w,h))
# image = cv2.undistort(image, mtx, dst, None, newcameramtx)

# all_charuco_ids = []
# all_charuco_corners = []

# dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
# board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
# params = cv2.aruco.DetectorParameters()
# detector = cv2.aruco.ArucoDetector(dictionary, params)

# marker_corners, marker_ids, rejectedCandidates = detector.detectMarkers(image)
# if marker_ids is not None and len(marker_ids) > 0: # If at least one marker is detected
#     # cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
#     ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
#     if charucoCorners is not None and charucoIds is not None and len(charucoCorners) > 3:
#         all_charuco_corners.append(charucoCorners)
#         all_charuco_ids.append(charucoIds)

#     retval, rvec, tvec = cv2.aruco.estimatePoseCharucoBoard(np.array(all_charuco_corners)[0], np.array(all_charuco_ids)[0], board, np.array(mtx), np.array(dst), np.empty(1), np.empty(1))

#     Zx, Zy, Zz = tvec[0][0], tvec[1][0], tvec[2][0]
#     fx, fy = mtx[0][0], mtx[1][1]

#     print(f'Zz = {Zz}\nfx = {fx}')
# else:
#     print("no marker for pose estimation detected")
#     exit(1)


# # size in meters
# def perspective_function(x, Z, f): 
#     return x*Z/f

# nb_pixels = 192
# print(perspective_function(nb_pixels, Zz, fx))