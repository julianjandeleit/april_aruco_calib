import os
import numpy as np
import cv2
import json 

# ------------------------------
# ENTER YOUR REQUIREMENTS HERE:
ARUCO_DICT = cv2.aruco.DICT_4X4_50
SQUARES_VERTICALLY = 5
SQUARES_HORIZONTALLY = 7
SQUARE_LENGTH = 0.03  # in meters
MARKER_LENGTH = 0.015  # in meters
# ...
PATH_TO_YOUR_IMAGES = 'testdata/charuco_calib_set_1/'
print(f"{ARUCO_DICT=}")
# ------------------------------

json_file_path = './calibration.json'

with open(json_file_path, 'r') as file: # Read the JSON file
    json_data = json.load(file)

mtx = np.array(json_data['mtx'])
dst = np.array(json_data['dist'])

dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, params)

def estimate_pose(image, mtx, dst, detector):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h,  w = image.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dst, (w,h), 1, (w,h))
    image = cv2.undistort(image, mtx, dst, None, newcameramtx)

    all_charuco_ids = []
    all_charuco_corners = []


    marker_corners, marker_ids, rejectedCandidates = detector.detectMarkers(image)
    if marker_ids is not None and len(marker_ids) > 0: # If at least one marker is detected
        # cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
        ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
        if charucoCorners is not None and charucoIds is not None and len(charucoCorners) > 3:
            all_charuco_corners.append(charucoCorners)
            all_charuco_ids.append(charucoIds)

        retval, rvec, tvec = cv2.aruco.estimatePoseCharucoBoard(np.array(all_charuco_corners)[0], np.array(all_charuco_ids)[0], board, np.array(mtx), np.array(dst), np.empty(1), np.empty(1))

        Zx, Zy, Zz = tvec[0][0], tvec[1][0], tvec[2][0]
        fx, fy = mtx[0][0], mtx[1][1]

        #print(f'Zz = {Zz}\nfx = {fx}')
        return rvec, tvec, charucoCorners, charucoIds

    else:
        print("no marker for pose estimation detected")
        return None
    

image_paths = [os.path.join(PATH_TO_YOUR_IMAGES, f) for f in os.listdir(PATH_TO_YOUR_IMAGES) if f.endswith(".JPG")]
image_paths = sorted(image_paths)
#print(image_paths)
rvecs = []
tvecs = []
for image_path in image_paths:
    print(image_path)
    image = cv2.imread(image_path)
    res = estimate_pose(image, mtx, dst, detector)
    if res is None:
        continue
    rvec, tvec, charucoCorners, charucoIds = res
    rvecs.append(rvec)
    tvecs.append(tvec)
    #print(charucoCorners)

import matplotlib.pyplot as plt
def show_charuco_corners(image, charucoCorners):
    # Convert the image to RGB for displaying with matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Plot the image with marked Charuco corners
    plt.figure(figsize=(10, 8))
    plt.imshow(image_rgb)
    
    if charucoCorners is not None:
        # Plot each corner
        for corner in charucoCorners:
            plt.plot(corner[0][0], corner[0][1], 'go', markersize=5)  # Green circles
    
    plt.title("Detected Charuco Corners")
    plt.axis('off')
    plt.show()
#print("showing result")
#show_charuco_corners(image, charucoCorners)

def plot_cameras_and_board(camera_rvecs, camera_tvecs, board):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Iterate through each camera pose (rvec, tvec)
    for idx, (rvec, tvec) in enumerate(zip(camera_rvecs, camera_tvecs)):
        # Convert rotation vector to rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(rvec)

        # Camera pose: the inverse of the extrinsic matrix (rotation + translation)
        camera_pose = np.eye(4)
        camera_pose[:3, :3] = rotation_matrix
        camera_pose[:3, 3] = tvec.flatten()

        # Plot the camera (each at its position)
        ax.scatter(tvec[0], tvec[1], tvec[2], color='r', s=100, label=f'Camera {idx + 1} Position')

        # Plot camera orientation using quivers (show orientation vectors)
        ax.quiver(tvec[0], tvec[1], tvec[2], rotation_matrix[0, 0], rotation_matrix[1, 0], rotation_matrix[2, 0], color='r', length=0.1)
        ax.quiver(tvec[0], tvec[1], tvec[2], rotation_matrix[0, 1], rotation_matrix[1, 1], rotation_matrix[2, 1], color='g', length=0.1)
        ax.quiver(tvec[0], tvec[1], tvec[2], rotation_matrix[0, 2], rotation_matrix[1, 2], rotation_matrix[2, 2], color='b', length=0.1)

    #  Apply a flip to the board's Z-coordinate to correct the orientation
    board_corners = board.getChessboardCorners()
    flip_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # Flip along the Z-axis

    for corner in board_corners:
        # Apply the flip to each corner point
        corner_flipped = np.dot(flip_matrix, corner.T).T
        ax.scatter(corner_flipped[0], corner_flipped[1], corner_flipped[2], color='b', s=50, label='Board Corners' if idx == 0 else None)

    # # Plot the board's corner points in 3D space
    # board_corners = board.getChessboardCorners()
    # for corner in board_corners:
    #     ax.scatter(corner[0], corner[1], 0, color='b', s=50, label='Board Corners' if idx == 0 else None)

    # Draw axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set aspect ratio and limits for better visualization
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim([-0.5, 0.5])
    ax.set_ylim([-0.5, 0.5])
    ax.set_zlim([-0.5, 0.5])

    # Display the plot
    plt.legend()
    plt.ion()
    plt.savefig("calib_result.png")

def plot_cameras_and_board_plotly(camera_rvecs, camera_tvecs, board):
    import plotly.graph_objects as go
    fig = go.Figure()

    # Iterate through each camera pose (rvec, tvec)
    for idx, (rvec, tvec) in enumerate(zip(camera_rvecs, camera_tvecs)):
        # Convert rotation vector to rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(rvec)

        # Camera position
        camera_position = tvec.flatten()

        # Plot the camera position
        fig.add_trace(go.Scatter3d(
            x=[camera_position[0]],
            y=[camera_position[1]],
            z=[camera_position[2]],
            mode='markers',
            marker=dict(size=5, color='red'),
            name=f'Camera {idx + 1} Position'
        ))

        # Plot camera orientation using quivers (show orientation vectors)
        quiver_length = 0.1
        fig.add_trace(go.Scatter3d(
            x=[camera_position[0], camera_position[0] + rotation_matrix[0, 0] * quiver_length],
            y=[camera_position[1], camera_position[1] + rotation_matrix[1, 0] * quiver_length],
            z=[camera_position[2], camera_position[2] + rotation_matrix[2, 0] * quiver_length],
            mode='lines',
            line=dict(color='red', width=4),
            name='X-axis'
        ))
        fig.add_trace(go.Scatter3d(
            x=[camera_position[0], camera_position[0] + rotation_matrix[0, 1] * quiver_length],
            y=[camera_position[1], camera_position[1] + rotation_matrix[1, 1] * quiver_length],
            z=[camera_position[2], camera_position[2] + rotation_matrix[2, 1] * quiver_length],
            mode='lines',
            line=dict(color='green', width=4),
            name='Y-axis'
        ))
        fig.add_trace(go.Scatter3d(
            x=[camera_position[0], camera_position[0] + rotation_matrix[0, 2] * quiver_length],
            y=[camera_position[1], camera_position[1] + rotation_matrix[1, 2] * quiver_length],
            z=[camera_position[2], camera_position[2] + rotation_matrix[2, 2] * quiver_length],
            mode='lines',
            line=dict(color='blue', width=4),
            name='Z-axis'
        ))

    # Apply a flip to the board's Z-coordinate to correct the orientation
    board_corners = board.getChessboardCorners()
    flip_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])  # Flip along the Z-axis

    for corner in board_corners:
        # Apply the flip to each corner point
        corner_flipped = np.dot(flip_matrix, corner.T).T
        fig.add_trace(go.Scatter3d(
            x=[corner_flipped[0]],
            y=[corner_flipped[1]],
            z=[corner_flipped[2]],
            mode='markers',
            marker=dict(size=5, color='blue'),
            name='Board Corners' if idx == 0 else None
        ))

    # Set axis labels
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'
        ),
        legend=dict(x=0, y=1)
    )

    # Save the figure as a self-contained HTML file
    fig.write_html("calib_result.html")


plot_cameras_and_board_plotly(rvecs, tvecs, board)