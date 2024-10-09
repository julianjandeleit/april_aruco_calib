#  creation of apriltags
`rosrun tagslam make_tag.py --nx 1 --ny 1 --marginx 0.025 --marginy 0.025 --tsize 0.16 --tspace 0.0 --startid 19 --tfam t36h11 --borderbits 1 --draw_box`

# extrinsic calibration (each subsection in seperate tmux shell)

this will execute example and visualize it. make sure to start docker with how to gui instructions.

start always with: 
`source ~/tagslam_root/devel/setup.bash`
`rosparam set use_sim_time true`


## rviz
roscore &
rosrun rviz rviz

manuallz add robot models with robot describtion "tags" and "cameras"

## tagslam

roslaunch tagslam tagslam.launch bag:=`rospack find tagslam`/example/example.bag

to replay video:
rosservice call /tagslam/replay


## tagslam viz

roslaunch tagslam_viz visualize_tags.launch tag_id_file:=$HOME/.ros/poses.yaml

oslaunch tagslam_viz visualize_cameras.launch cameras_file:=/root/tagslam_root/src/tagslam/example/cameras.yaml





