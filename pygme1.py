import pandas as pd

csv_file_path = './Hannara_modi.csv'
df = pd.read_csv(csv_file_path)
LAT = df['LA']; LON = df['LO']
LAT.reset_index(drop=True, inplace=True)
LON.reset_index(drop=True, inplace=True)
pos = pd.concat([LON, LAT], keys=['LON','LAT'] ,axis=1)
data_list = pos.values.tolist()

latmin=pos["LAT"].min()
lonmin=pos["LON"].min()
pos["LAT"] = pos['LAT'] - latmin
pos["LON"] = pos["LON"] - lonmin

pos = pos[pos.index % 50 ==0]
pos.reset_index(drop=True, inplace=True)
import pygame

# 초기화
pygame.init()

# 지도 이미지 불러오기
bg_image = pygame.image.load('map_image2.png')

# 창 설정
screen = pygame.display.set_mode((bg_image.get_width(), bg_image.get_height()))
pygame.display.set_caption('geo track')
# 경로 데이터
data = pos
print(data['LON'][1], data['LAT'][1])

# 지도 위의 좌표로 변환 (이 부분은 지도의 크기와 영역에 따라 조정해야 합니다)
def convert_coordinates(lon, lat):
    # 변환 로직을 작성해주세요. 예시로 단순 스케일링만을 적용하였습니다.
    x = int(50 * lon + 230)
    y = int(450 - 63 * lat)  # 수정된 부분
    return x, y

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
