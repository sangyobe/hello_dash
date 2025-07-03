import plotly.graph_objects as go
import numpy as np

# 1. 샘플 데이터 생성 (시간에 따른 x, y, theta)
# 실제 데이터로 대체하시면 됩니다.
num_points = 100
time = np.linspace(0, 10, num_points) # 0초부터 10초까지
x = np.sin(time) * 2 + time * 0.5
y = np.cos(time) * 2 + time * 0.3

# theta 값 생성: 여기서는 시간에 따라 0에서 360도까지 반복적으로 변하도록 설정
# 실제 로봇이나 객체의 방향 데이터로 대체하시면 됩니다.
theta_radians = np.pi * 0.5 - np.unwrap(np.arctan2(np.diff(y, prepend=y[0]), np.diff(x, prepend=x[0]))) # x, y 변화량으로 대략적인 각도 계산
# theta_radians = np.linspace(0, 4 * np.pi, num_points) # 0에서 4파이까지 변화
theta_degrees = np.degrees(theta_radians) # Plotly marker.angle은 도(degrees)를 사용

# 2. (x, y) 궤적 그래프 생성
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='lines+markers', # 선과 마커 모두 표시
    name='(x, y) Trajectory with Orientation',
    marker=dict(
        symbol='triangle-up', # 방향을 나타내기 좋은 위쪽 삼각형 마커 사용
        size=10, # 마커 크기
        color='blue', # 마커 색상
        angle=theta_degrees, # theta 값에 따라 마커 회전 (도 단위)
        line=dict(width=1, color='DarkSlateGrey') # 마커 테두리
    ),
    line=dict(color='lightgrey', width=2), # 궤적 선 색상 및 두께
    hovertemplate=
    '<b>Time</b>: %{customdata[0]:.2f}s<br>' +
    '<b>X</b>: %{x:.2f}<br>' +
    '<b>Y</b>: %{y:.2f}<br>' +
    '<b>Theta (rad)</b>: %{customdata[1]:.2f}<br>' +
    '<b>Theta (deg)</b>: %{customdata[2]:.2f}<extra></extra>',
    customdata=np.stack((time, theta_radians, theta_degrees), axis=-1)
))

# 3. 레이아웃 설정
fig.update_layout(
    title_text='2D Trajectory with Marker Orientation (x, y, theta)',
    xaxis_title='X Position',
    yaxis_title='Y Position',
    hovermode='closest', # 마우스 가까이에 있는 데이터 포인트에 툴팁 표시
    height=600,
    width=800,
    yaxis=dict(scaleanchor="x", scaleratio=1), # X, Y 축 비율을 1:1로 유지하여 왜곡 방지
    showlegend=True
)

# 4. 그래프 표시
fig.show()