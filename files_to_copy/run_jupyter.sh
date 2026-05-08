export DISPLAY=:1.0
echo "Open Jupyter Notebook at: http://localhost:8888/"
jupyter notebook --notebook-dir="/home/ubuntu/turtlebot3_ws/src/jupyter_notebooks" --ip 0.0.0.0
