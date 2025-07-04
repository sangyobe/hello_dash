import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

# 파일 설정
csv_filename = "data/leoquad_odom_demo.csv"

# 데이터 로드
df = pd.read_csv(csv_filename)
time = df['time'].to_list()
x = df['x'].to_list()
y = df['y'].to_list()
theta = df['theta'].to_list()
vx_des = df['vx_des'].to_list()
vy_des = df['vy_des'].to_list()
wz_des = df['wz_des'].to_list()

# Plot
fig = make_subplots(rows=4, cols=1,
                    # shared_xaxes=True, # x축을 공유하여 시간 동기화
                    vertical_spacing=0.05,
                    subplot_titles=("2D Trajectory (x, y) with heading angle(theta)", "Vx over Time", "Vy over Time", "Wz over Time"),
                    row_heights=[0.5,0.25,0.25,0.25])

fig.add_trace(go.Scatter(x=x, y=y,
                         mode='lines+markers',
                         name='(x, y) Trajectory',
                         marker=dict(size=5),
                         hovertemplate=
                         '<b>Time</b>: %{customdata[0]:.2f}s<br>' +
                         '<b>X</b>: %{x:.2f}<br>' +
                         '<b>Y</b>: %{y:.2f}<br>' +
                         '<b>Theta</b>: %{customdata[1]:.2f} radians<extra></extra>',
                         customdata=np.stack((time, theta), axis=-1)),
              row=1, col=1)

fig.add_trace(go.Scatter(x=time, y=vx_des,
                         mode='lines',
                         name='vx_des',
                         line=dict(color='red'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.2f}s<br>' +
                         '<b>Vw</b>: %{y:.2f} m/sec<extra></extra>'),
              row=2, col=1)

fig.add_trace(go.Scatter(x=time, y=vy_des,
                         mode='lines',
                         name='vy_des',
                         line=dict(color='red'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.2f}s<br>' +
                         '<b>Vw</b>: %{y:.2f} m/sec<extra></extra>'),
              row=3, col=1)

fig.add_trace(go.Scatter(x=time, y=wz_des,
                         mode='lines',
                         name='wz_des',
                         line=dict(color='red'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.2f}s<br>' +
                         '<b>Vw</b>: %{y:.2f} rad/sec<extra></extra>'),
              row=4, col=1)

fig.update_layout(title_text='Time-Varying (x, y, Vw_des) Visualization',
                  hovermode='closest', # 마우스 가까이에 있는 데이터 포인트에 툴팁 표시
                  height=1000, # 그래프 전체 높이
                  showlegend=True) # 범례 표시

# x, y 축 라벨 설정
fig.update_xaxes(title_text="Time (s)", row=4, col=1)
fig.update_yaxes(title_text="X position", row=1, col=1)
fig.update_yaxes(title_text="Y position", scaleanchor="x", scaleratio=1, row=1, col=1) # X, Y 축 비율을 같게 유지
fig.update_yaxes(title_text="Vx (m/sec)", row=2, col=1)
fig.update_yaxes(title_text="Vy (m/sec)", row=3, col=1)
fig.update_yaxes(title_text="Wz (rad/sec)", row=4, col=1)

# 6. 그래프 표시
fig.show()