import random as r
import time

def initMaze():
    maze = [
        ['B', 'B', 'B', 'B', 'B', 'B'],
        ['B', ' ', ' ', ' ', ' ', 'B'],
        ['B', ' ', ' ', ' ', ' ', 'B'],
        ['B', ' ', ' ', ' ', ' ', 'B'],
        ['B', ' ', ' ', ' ', ' ', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B']
    ]
    return maze

def SetMaze():
    maze = [ ['B' for _ in range(6)] for _ in range(6)]
    for row in range(6):
        #벽
        if row == 0 or row == 5:
            continue
        for col in range(6):
            # 벽은 건너뜀.
            if col == 0 or col == 5:
                continue
            # 미로의 기본 값은 공백
            maze[row][col] = ' '
            # 확률 생성을 위한 값 생성
            wumpus = r.randint(1, 100)
            pit = r.randint(1, 100)
            # (1, 1), (0, 1), (2, 1) 위치일 땐 건너뜀.
            if( row == 3 and col == 1) or (row == 4 and (col == 1 or col == 2)):
                continue
            maze[row][col] = ' '
            if wumpus <= 15:
                maze[row][col] = 'W'
            if pit <= 15:
                maze[row][col] = 'P'
            if wumpus <= 15 and pit <= 15:
                maze[row][col] = 'D'
    # 금 위치 설정
    while True:
        gold_row = r.randint(1, 4)
        gold_col = r.randint(1, 4)
        
        if( gold_row == 3 and gold_col == 1) or (gold_row == 4 and (gold_col == 1 or gold_col == 2)):
            maze[gold_row][gold_col] = ' '
            continue
        else:
            
            maze[gold_row][gold_col] = 'G'
            break
    return maze


# 탐험가 초기 설정
# position : 위치
# prevPosition : 이전 위치
# arrow : 화살 개수
# breeze, stench, glitter, bump : 근처에 해당 물체가 있는지 여부
# encounter : 현재까지 마주친 P,W의 좌표 저장
# direction : 현재 진행 방향
# route : 현재 위치까지의 이동 경로
# hasGold : 금 보유 유무
def SetExplorer():
    explorer = {
        'position' : (4, 1), 
        'prevPosition' : (4, 1),
        'arrow' : 3, 
        "breeze" : False, 
        'stench' : False, 
        'glitter' : False, 
        'bump' : False, 
        'scream' : False, 
        'encounter' : [],
        'direction' : 'right',
        'route' : [],
        'hasGold' : False
        }
    return explorer

# 구덩이가 근처에 있는지 체크
def CheckBreeze():
    row, col = explorer['position']
    # if 'P', 또는 'D'가 가 상,하,좌,우에 있으면 breeze True.
    if 'P' in globalMaze[row+1][col] + globalMaze[row-1][col] + globalMaze[row][col-1] + globalMaze[row][col+1]:
        explorer['breeze'] = True
    elif 'D' in globalMaze[row+1][col] + globalMaze[row-1][col] + globalMaze[row][col-1] + globalMaze[row][col+1]:
        explorer['breeze'] = True
    else:
        explorer['breeze'] = False
    return explorer

# 금이 근처에 있는지 체크
def CheckGlitter():
    row, col = explorer['position']

    if 'G' in globalMaze[row+1][col] + globalMaze[row-1][col] + globalMaze[row][col-1] + globalMaze[row][col+1]:
        explorer['glitter'] = True
    else:
        explorer['glitter'] = False
    return explorer
    
# 벽이 근처에 있는지 체크
def CheckBump():
    row, col = explorer['position']

    if 'B' in globalMaze[row+1][col] +globalMaze[row-1][col] + globalMaze[row][col-1] + globalMaze[row][col+1]:
        explorer['bump'] = True
    else:
        explorer['bump'] = False
    return explorer

# 괴물 이 근처에 있는지 체크
def CheckStench():
    row, col = explorer['position']

    if 'W' in globalMaze[row+1][col] + globalMaze[row-1][col] + globalMaze[row][col-1] + globalMaze[row][col+1]:
        explorer['stench'] = True
    elif 'D' in globalMaze[row+1][col] + globalMaze[row-1][col] + globalMaze[row][col-1] + globalMaze[row][col+1]:
        explorer['stench'] = True
    else:
        explorer['stench'] = False
    return explorer

# 이동한 위치에서 몬스터를 잡았다면, 비명 출력
def PrintScream():
    if explorer['scream']:
        print('Scream')
    explorer['scream'] = False


# 해당 좌표의 괴물, 웅덩이가 처음 조우한것인지 체크
def CheckFirstEncounter():
    row, col = explorer['position']
    nextCounter = globalMaze[row][col]
    if nextCounter == 'W' or nextCounter == 'P' or nextCounter == 'D':
        if not ((row, col) in explorer['encounter']):
            explorer['encounter'].append((row, col))
            maze[row][col] = globalMaze[row][col]
            return True
    return False
#좌회전
def TurnLeft():
    explorer['position'] = explorer['prevPosition']
    direction = explorer['direction']
    turn = {'right' : 'up', 'up' : 'left', 'left' : 'down', 'down' : 'right'}
    explorer['direction'] = turn[direction]
#우회전
def TurnRight():
    explorer['position'] = explorer['prevPosition']
    direction = explorer['direction']
    turn = {'right' : 'down', 'down' : 'left', 'left' : 'up', 'up' : 'right'}
    explorer['direction'] = turn[direction]

# 괴물을 다시 만났을 때 호출, 화살 발사
def Shoot():
    row, col = explorer['position']
    explorer['scream'] = True
    explorer['arrow'] -= 1

# 주요 행동. 이동 하고자 하는 좌표가 어떤 것이냐에 따라 다른 행위 수행.
def Act():
    row, col = explorer['position']
    # 이동하고자 하는 좌표가 W라면
    if maze[row][col] == 'W':
        # 화살 발사
        if explorer['arrow'] > 0:
            Shoot()
            maze[row][col] = ' '
            globalMaze[row][col] = ' '
        # 혹은 좌,우로 방향 전환.
        # 두 Left, Right 함수 중 임의로 하나 선택.
        else:
            [TurnLeft, TurnRight][r.randint(0, 1)]()
    # 이동하고자 하는 좌표가 D라면,
    elif maze[row][col] == 'D':
        # 발사 후 해당 위치를 P로 변환.
        if explorer['arrow'] > 0:
            Shoot()
            maze[row][col] = 'P'
        else:
            [TurnLeft, TurnRight][r.randint(0, 1)]()

    elif maze[row][col] == 'B':
        [TurnLeft, TurnRight][r.randint(0, 1)]()
    # 이동하고자 하는 좌표가 G라면,
    # 금을 잡았다는 판정.
    elif globalMaze[row][col] == 'G':
        maze[row][col] = 'G'
        explorer['position'] = explorer['prevPosition']
        PrintMaze()
        time.sleep(1)
        maze[row][col] = ' '
        explorer['position'] = (row, col)
        Grab()
    # maze가 D였다면, 괴물을 잡은 위치가 P로 변경됨.
    # P는 따로 검사.
    if maze[row][col] == 'P':
        [TurnLeft, TurnRight][r.randint(0, 1)]()

def Grab():
    explorer['hasGold'] = True


# 지금까지 지나온 루트 저장
def SaveRoute():
    explorer['route'].append(explorer['position'])

# 탐험가를 이동시킴
def GoForward():
    row, col = explorer['position']
    explorer['prevPosition'] = explorer['position']
    if explorer['direction'] == 'right':
        col += 1
    elif explorer['direction'] == 'left':
        col -= 1
    elif explorer['direction'] == 'up':
        row -= 1
    elif explorer['direction'] == 'down':
        row += 1
    explorer['position'] = (row, col)

# 처음 괴물/구덩이를 마주쳤을 때 실행
# 탐험가의 현재 위치를 초기화
def ResetToInit():
    explorer['direction'] = 'right'
    explorer['position'] = (4, 1)
    explorer['route'] = []

# 미로를 출력하는 함수
def PrintMaze():
    r, c = explorer['position']
    x = c
    y = 5 - r
    print(f"({x}, {y})")
    for row in range(len(maze)):
        for col in range(len(maze)):
            if (row, col) == explorer['position']:
                print("A", end = '')
            else:
                print(maze[row][col], end = '')
            
        print("     ", end = '')
        for col in range(len(maze)):
            print(globalMaze[row][col], end = '')
        print()
    print(f"arrow : {explorer['arrow']}")
    print(f"breezy : {explorer['breeze']}")
    print(f"stenchy : {explorer['stench']}")
    print(f"glitter : {explorer['glitter']}")
    print()

# 탐험가가 금을 획득했을 때 호출
# 저장한 route를 따라가, (1, 1) 위치에 도달 시 종료,
def Climb():
    route = [(4, 1)]
    route += explorer['route']
    route.reverse()
    print(route)
    for row, col in route:
        explorer['position'] = (row, col)
        PrintMaze()
        time.sleep(0.3)
        if row == 4 and col == 1:##########################################################################
            break
    print('Clear!')
    exit(0)

def StartExp():
    global maze, explorer, globalMaze
    globalMaze = SetMaze()
    explorer = SetExplorer()
    maze = initMaze()
    count = 0
    while True:
        if CheckFirstEncounter():
            ResetToInit()
        else:
            Act()
            SaveRoute()
            CheckBreeze()
            CheckStench()
            CheckGlitter()
            CheckBump()
        PrintMaze()
        PrintScream()
        time.sleep(0.3)
        if explorer['hasGold']:
            Climb()
        GoForward()
        count += 1
        if count == 100:
            globalMaze = SetMaze()
            explorer = SetExplorer()
            maze = initMaze()
            count = 0

StartExp()