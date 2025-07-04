import rosbag2_py
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import rclpy
from rclpy.serialization import deserialize_message
# from tf_transformations import euler_from_quaternion
from scipy.spatial.transform import Rotation as R
import pandas as pd

# Data 준비
time_curr = 0
x_curr = 0.0
y_curr = 0.0
theta_curr = 0.0
vx_curr = 0.0
vy_curr = 0.0
wz_curr = 0.0

time = []
x = []  # robot pose
y = []
theta = []
vx = []
vy = []
wz = []
vx_des = [] # cmd_vel
vy_des = []
wz_des = []


# 파일 설정
csv_filename = "data/leoquad_odom_demo.csv"
bag_filename = 'data/TestSite_LEOQUAD02_2025_07_03-13_55_09_0005_0.db3'
topics = ['/navi/mapping/local_odom/odometry', '/cmd_vel']

# 토픽 Reader 생성 및 설정
storage_options = rosbag2_py.StorageOptions(uri=bag_filename, storage_id='sqlite3')
converter_options = rosbag2_py.ConverterOptions(
    input_serialization_format='cdr',
    output_serialization_format='cdr'
)
reader = rosbag2_py.SequentialReader()
reader.open(storage_options, converter_options)

# 특정 토픽 필터링
reader.set_filter(rosbag2_py._storage.StorageFilter(topics))

# 데이터 읽기
time_init = -1
# for _ in range(100):
while reader.has_next():
    (topic, data, timestamp) = reader.read_next()
    # print(f"Topic: {topic}, Timestamp: {timestamp}, Data: ")
    if topic == '/navi/mapping/local_odom/odometry':
        odom = deserialize_message(data, Odometry)
        # print(f"{odom.pose.pose.position.x} {odom.pose.pose.position.y} ")
        
        if time_init < 0:
            time_init = timestamp
        time_curr = timestamp - time_init
        
        x_curr = odom.pose.pose.position.x
        y_curr = odom.pose.pose.position.y
        # theta_curr = 0.0        
        quat = [odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w]
        # (roll, pitch, yaw) = euler_from_quaternion(quat)
        rotation = R.from_quat(quat)
        (yaw, pitch, roll) = rotation.as_euler('zyx')
        theta_curr = yaw
        vx_curr = odom.twist.twist.linear.x
        vy_curr = odom.twist.twist.linear.y
        wz_curr = odom.twist.twist.angular.z
        
    elif topic == '/cmd_vel':
        cmd_vel = deserialize_message(data, Twist)
        # print(f"{cmd_vel.linear.x} {cmd_vel.linear.y} {cmd_vel.angular.z}")
        time.append(time_curr * 1.0e-9)
        x.append(x_curr)
        y.append(y_curr)
        theta.append(theta_curr)
        vx.append(vx_curr)
        vy.append(vy_curr)
        wz.append(wz_curr)
        vx_des.append(cmd_vel.linear.x)
        vy_des.append(cmd_vel.linear.y)
        wz_des.append(cmd_vel.angular.z)

# print(f'time = {time}')
# print(f'x = {x}')
# print(f'y = {y}')
# print(f'theta = {theta}')
# print(f'vx_des = {vx_des}')
# print(f'vy_dex = {vy_des}')
# print(f'wz_des = {wz_des}')

df = pd.DataFrame({
    'time': time,
    'x': x,
    'y': y,
    'theta': theta,
    'vx': vx,
    'vy': vy,
    'wz': wz,
    'vx_des': vx_des,
    'vy_des': vy_des,
    'wz_des': wz_des,
})
df.to_csv(csv_filename, index=False)