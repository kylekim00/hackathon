import pandas as pd

csv_file_path = '/Users/gimhong-gwon/Desktop/flask/second.csv'


df = pd.read_csv(csv_file_path)
TIME = df[df['data_channel_id']=='/VDR/GPGGA/GPGGA_CH4'].copy()['created_time']
LON = df[df['data_channel_id']=='/VDR/GPGGA/GPGGA_CH4'].copy()['double_v']
LAT = df[df['data_channel_id']=='/VDR/GPGGA/GPGGA_CH2'].copy()['double_v']
LAT.reset_index(drop=True, inplace=True)
LON.reset_index(drop=True, inplace=True)
pos = pd.concat([LON, LAT], keys=['LON','LAT'] ,axis=1)
data_list = pos.values.tolist()

latmin=pos["LAT"].min()
lonmin=pos["LON"].min()
pos["LAT"] = pos['LAT'] - latmin
pos["LON"] = pos["LON"] - lonmin
pos = pos[pos.index % 100 ==0]
pos.reset_index(drop=True, inplace=True)
import pygame

# 초기화
pygame.init()

# 지도 이미지 불러오기
bg_image = pygame.image.load('map_image1.png')

# 창 설정
screen = pygame.display.set_mode((bg_image.get_width(), bg_image.get_height()))
pygame.display.set_caption('geo track')
# 경로 데이터
data = pos
print(data['LON'][1], data['LAT'][1])


# 지도 위의 좌표로 변환 (이 부분은 지도의 크기와 영역에 따라 조정해야 합니다)
def convert_coordinates(lon, lat):
    # 변환 로직을 작성해주세요. 예시로 단순 스케일링만을 적용하였습니다.
    x = int(23 * lon + 150)
    y = int(500 - 26 * lat)  # 수정된 부분
    return x, y

grid_interval = 10  # 그리드의 간격 설정
def draw_grid():
    grid_color = (200, 200, 200)  # 그리드의 색상 (회색)
    

    # 가로 선 그리기
    for y in range(0, bg_image.get_height(), grid_interval):
        pygame.draw.line(screen, grid_color, (0, y), (bg_image.get_width(), y))

    # 세로 선 그리기
    for x in range(0, bg_image.get_width(), grid_interval):
        pygame.draw.line(screen, grid_color, (x, 0), (x, bg_image.get_height()))



def fill_transparent_cell(top_left, color=(255,0,0), cell_size=(grid_interval, grid_interval), alpha=128):
    # 새로운 Surface 객체 생성 (with per-pixel alpha)
    top_left  = (grid_interval*top_left[0], grid_interval* top_left[1])
    temp_surface = pygame.Surface((cell_size[0], cell_size[1]), pygame.SRCALPHA)
    
    # Surface에 색칠
    temp_surface.fill((color[0], color[1], color[2], alpha))

    # 메인 스크린에 렌더링
    screen.blit(temp_surface, top_left)


# 메인 루프
running = True
index = 0
path_points = []  # 경로를 그리기 위한 좌표들을 저장할 리스트
dot_interval = 1  # 점선의 간격 설정. 이 값을 조절하여 원하는 간격으로 점선을 그릴 수 있습니다.
dotted_path_points = [(convert_coordinates(data['LON'][i], data['LAT'][i])) for i in range(0, len(data), dot_interval)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 배경 그리기
    screen.blit(bg_image, (0, 0))
    for point in dotted_path_points:
        pygame.draw.circle(screen, (255, 255, 0), point, 2)  # 노란색 점으로 점선 그리기
    
    draw_grid()
    fill_transparent_cell((44,19), (255, 0, 0))
    fill_transparent_cell((44, 20), (255, 0, 0))
    fill_transparent_cell((44, 21), (255, 255, 0))
    fill_transparent_cell((45,19), (255, 0, 0))
    fill_transparent_cell((45, 20), (255, 0, 0))
    fill_transparent_cell((45, 21), (255, 255, 0))
    fill_transparent_cell((46, 19), (180, 255, 0))
    fill_transparent_cell((46, 20), (190, 55, 0))
    fill_transparent_cell((46, 21), (170, 255, 0))
    # 경로 그리기
    if index < len(data):
        x, y = convert_coordinates(data['LON'][index], data['LAT'][index])
        path_points.append((x, y))  # 좌표를 경로 리스트에 추가
        # print(index ,x, y)
        
        # 경로 위의 점선 그리기

        # 경로를 그릴 좌표가 2개 이상일 때, 자국을 남깁니다.
        if len(path_points) > 1:
            pygame.draw.lines(screen, (0, 255, 0), False, path_points, 3)
        
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)  # 빨간색 원으로 표시
        
        index += 1
    else:
        index = 0
        path_points = []
    pygame.time.wait(100)  # 1초 대기
    pygame.display.flip()

pygame.quit()