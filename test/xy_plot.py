import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 1. 샘플 데이터 생성 (시간에 따른 x, y, theta)
# 실제 데이터로 대체하시면 됩니다.
num_points = 100
time = np.linspace(0, 10, num_points) # 0초부터 10초까지
x = np.sin(time) + time * 0.1
y = np.cos(time) + time * 0.2
theta = np.unwrap(np.arctan2(np.diff(y, prepend=y[0]), np.diff(x, prepend=x[0]))) # x, y 변화량으로 대략적인 각도 계산
# theta = np.linspace(0, 2 * np.pi, num_points) # 또는 독립적인 theta 값

# 2. 서브플롯 생성: 2행 1열 구조
# 첫 번째 행에는 (x,y) 궤적, 두 번째 행에는 theta(시간에 따라)
fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True, # x축을 공유하여 시간 동기화
                    vertical_spacing=0.15,
                    subplot_titles=("2D Trajectory (x, y)", "Orientation (theta) over Time"))

# 3. (x, y) 궤적 그래프 추가 (첫 번째 서브플롯)
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

# 4. Theta(시간에 따라) 그래프 추가 (두 번째 서브플롯)
fig.add_trace(go.Scatter(x=time, y=theta,
                         mode='lines',
                         name='Theta',
                         line=dict(color='red'),
                         hovertemplate=
                         '<b>Time</b>: %{x:.2f}s<br>' +
                         '<b>Theta</b>: %{y:.2f} radians<extra></extra>'),
              row=2, col=1)

# 5. 레이아웃 설정
fig.update_layout(title_text='Time-Varying (x, y, theta) Visualization',
                  hovermode='closest', # 마우스 가까이에 있는 데이터 포인트에 툴팁 표시
                  height=700, # 그래프 전체 높이
                  showlegend=True) # 범례 표시

# x, y 축 라벨 설정
fig.update_xaxes(title_text="Time (s)", row=2, col=1)
fig.update_yaxes(title_text="X position", row=1, col=1)
fig.update_yaxes(title_text="Y position", scaleanchor="x", scaleratio=1, row=1, col=1) # X, Y 축 비율을 같게 유지
fig.update_yaxes(title_text="Theta (radians)", row=2, col=1)

# 6. 그래프 표시
fig.show()