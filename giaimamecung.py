import pygame  # Import thư viện pygame cho việc vẽ đồ họa và xử lý sự kiện
from collections import deque  # Import deque (double-ended queue) để sử dụng trong thuật toán BFS
import random  # Import thư viện random để tạo mê cung ngẫu nhiên

# Kích thước cửa sổ Pygame
WINDOW_SIZE = (700, 700)

# Kích thước mê cung
MAZE_SIZE = (25, 25)
CELL_SIZE = (WINDOW_SIZE[0] // MAZE_SIZE[0], WINDOW_SIZE[1] // MAZE_SIZE[1])

# Định nghĩa màu sắc bằng các biến
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)  # Màu nâu cho hàng rào
BLUE = (0, 0, 255)

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)  # Tạo cửa sổ Pygame với kích thước WINDOW_SIZE
pygame.display.set_caption("Giai Ma Me Cung")  # Đặt tiêu đề của cửa sổ là "Giai Ma Me Cung"

# Hàm kiểm tra xem một vị trí có hợp lệ không
def is_valid_move(maze, visited, row, col):
    if row >= 0 and col >= 0 and row < len(maze) and col < len(maze[0]) and maze[row][col] != '#' and not visited[row][col]:
        return True
    return False

# Hàm giải mê cung bằng BFS và vẽ hình ảnh
def solve_maze(maze, start, end):
    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]  # Tạo mảng visited để theo dõi các ô đã thăm
    queue = deque()  # Sử dụng deque để triển khai hàng đợi cho thuật toán BFS
    queue.append((start[0], start[1], []))  # Bắt đầu từ điểm bắt đầu và đường đi trống

    dx = [-1, 1, 0, 0]  # Dịch chuyển theo hàng ngang
    dy = [0, 0, -1, 1]  # Dịch chuyển theo hàng dọc

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Khi sự kiện thoát khỏi cửa sổ được kích hoạt, dừng ứng dụng
                return

        row, col, path = queue.popleft()  # Lấy ô đầu hàng đợi
        visited[row][col] = True

        if (row, col) == end:
            return path  # Trả về danh sách các bước nếu đã đến điểm đích

        for i in range(4):
            new_row = row + dx[i]
            new_col = col + dy[i]

            if is_valid_move(maze, visited, new_row, new_col):
                new_path = path.copy()  # Tạo bản sao của đường đi hiện tại
                new_path.append((new_row, new_col))  # Thêm bước tiếp theo vào đường đi
                queue.append((new_row, new_col, new_path))  # Thêm ô mới vào hàng đợi

    print("Không tìm thấy đường đi.")
    return []

# Vẽ mê cung
def draw_maze(maze, start=None, end=None, path=None):
    screen.fill(WHITE)  # Xóa màn hình với màu trắng

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            rect = pygame.Rect(col * CELL_SIZE[0], row * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1])  # Tạo hình chữ nhật cho mỗi ô
            if maze[row][col] == '#':
                pygame.draw.rect(screen, BROWN, rect)  # Vẽ hàng rào màu nâu
            elif maze[row][col] == 'S':
                pygame.draw.rect(screen, GREEN, rect)  # Vẽ vị trí ban đầu màu xanh lá cây
            elif maze[row][col] == 'E':
                pygame.draw.rect(screen, RED, rect)  # Vẽ vị trí đích màu đỏ
            elif path and (row, col) in path:
                pygame.draw.rect(screen, BLUE, rect)  # Vẽ đường đi màu xanh
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Vẽ các ô trống màu trắng

    if start:
        pygame.draw.rect(screen, GREEN, pygame.Rect(start[1] * CELL_SIZE[0], start[0] * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]))  # Vẽ vị trí ban đầu
    if end:
        pygame.draw.rect(screen, RED, pygame.Rect(end[1] * CELL_SIZE[0], end[0] * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]))  # Vẽ vị trí đích

    pygame.display.flip()  # Cập nhật màn hình

# Tạo mê cung ngẫu nhiên kích thước MAZE_SIZE[0] x MAZE_SIZE[1]
def create_random_maze(m, n, density=0.25):
    maze = [['#' if random.random() < density else '.' for _ in range(n)] for _ in range(m)]  # Tạo mê cung với mật độ ngẫu nhiên
    return maze

random_maze = create_random_maze(MAZE_SIZE[0], MAZE_SIZE[1])

start = None  # Điểm bắt đầu của đường đi trong mê cung
end = None  # Điểm đích của đường đi trong mê cung
solving = False  # Biến xác định xem đang giải mê cung hay không

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Khi sự kiện thoát khỏi cửa sổ được kích hoạt, dừng vòng lặp

        if not solving:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_SIZE[0]  # Xác định cột dựa trên vị trí chuột
                row = mouse_y // CELL_SIZE[1]  # Xác định hàng dựa trên vị trí chuột
                if random_maze[row][col] != '#':
                    if start is None:
                        start = (row, col)
                        random_maze[row][col] = 'S'  # Đặt điểm bắt đầu
                    elif end is None:
                        end = (row, col)
                        random_maze[row][col] = 'E'  # Đặt điểm đích
                    if start and end:
                        path = solve_maze(random_maze, start, end)
                        if not path:
                            print("Không tìm thấy đường đi. Vui lòng chọn lại điểm bắt đầu và điểm kết thúc.")
                            random_maze[start[0]][start[1]] = '.'
                            random_maze[end[0]][end[1]] = '.'
                            start = None
                            end = None
                        solving = True  # Bắt đầu giải mê cung
        else:
            for step in path:
                pygame.time.delay(500)
                draw_maze(random_maze, start, end, [step])
            solving = False

    draw_maze(random_maze, start, end)

pygame.quit()  # Kết thúc ứng dụng Pygame khi kết thúc vòng lặp