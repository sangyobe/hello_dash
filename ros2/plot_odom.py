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
theta_degree = np.degrees(theta)
theta_degree_disp = np.degrees([(np.pi*0.5-x) for x in theta])
vx = df['vx'].to_list()
vy = df['vy'].to_list()
wz = df['wz'].to_list()
vx_des = df['vx_des'].to_list()
vy_des = df['vy_des'].to_list()
wz_des = df['wz_des'].to_list()


# Plot
fig = make_subplots(rows=3, cols=2,
                    specs=[[{'rowspan': 3}, {}], [None, {}], [None, {}]],
                    shared_xaxes=True, # x축을 공유하여 시간 동기화
                    vertical_spacing=0.05,
                    subplot_titles=("2D Trajectory (x, y) with heading angle(theta)", "Vx over Time", "Vy over Time", "Wz over Time"),
                    column_widths=[0.6, 0.4],
                    row_heights=[0.25,0.25,0.25])

fig.add_trace(go.Scatter(x=x, y=y,
                         mode='lines+markers',
                         name='(x, y) Trajectory',
                         marker=dict(
                             symbol='triangle-up', # 방향을 나타내기 좋은 위쪽 삼각형 마커 사용
                             size=10, # 마커 크기
                             color='blue', # 마커 색상
                             angle=theta_degree_disp, # theta 값에 따라 마커 회전 (도 단위)
                             line=dict(width=1, color='DarkSlateGrey') # 마커 테두리
                         ),
                         line=dict(color='lightgrey', width=1), # 궤적 선 색상 및 두께
                         hovertemplate=
                         '<b>Time</b>: %{customdata[0]:.5f}s<br>' +
                         '<b>X</b>: %{x:.5f}<br>' +
                         '<b>Y</b>: %{y:.5f}<br>' +
                         '<b>Theta</b>: %{customdata[1]:.5f} degrees<extra></extra>',
                         customdata=np.stack((time, theta_degree), axis=-1)),
              row=1, col=1)

fig.add_trace(go.Scatter(x=time, y=vx,
                         mode='lines',
                         name='vx',
                         line=dict(color='green'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.5f}s<br>' +
                         '<b>Vx</b>: %{y:.5f} m/sec<extra></extra>'),
              row=1, col=2)
fig.add_trace(go.Scatter(x=time, y=vx_des,
                         mode='lines',
                         name='vx_des',
                         line=dict(color='red'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.5f}s<br>' +
                         '<b>vx_des</b>: %{y:.5f} m/sec<extra></extra>'),
              row=1, col=2)

fig.add_trace(go.Scatter(x=time, y=vy,
                         mode='lines',
                         name='vy',
                         line=dict(color='green'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.5f}s<br>' +
                         '<b>vy</b>: %{y:.5f} m/sec<extra></extra>'),
              row=2, col=2)
fig.add_trace(go.Scatter(x=time, y=vy_des,
                         mode='lines',
                         name='vy_des',
                         line=dict(color='red'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.5f}s<br>' +
                         '<b>vy_des</b>: %{y:.5f} m/sec<extra></extra>'),
              row=2, col=2)

fig.add_trace(go.Scatter(x=time, y=wz,
                         mode='lines',
                         name='wz',
                         line=dict(color='green'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.5f}s<br>' +
                         '<b>wz</b>: %{y:.5f} rad/sec<extra></extra>'),
              row=3, col=2)
fig.add_trace(go.Scatter(x=time, y=wz_des,
                         mode='lines',
                         name='wz_des',
                         line=dict(color='red'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.5f}s<br>' +
                         '<b>Vw</b>: %{y:.5f} rad/sec<extra></extra>'),
              row=3, col=2)

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

# x축 공유
fig.update_xaxes(matches='x', row=2, col=1)
fig.update_xaxes(matches='x', row=3, col=1)
fig.update_xaxes(matches='x', row=4, col=1)

# 6. 그래프 표시
fig.show()