'''
Compony: NUC
Date: 2026-05-22 15:19:02
LastEditors: Loong2525
LastEditTime: 2026-05-25 19:45:02
'''

import sys
import random
import pygame
from pygame.locals import *
import pygame.gfxdraw
from collections import namedtuple
from abc import ABC, abstractmethod
from enum import Enum

# ==================== 基础数据结构 ====================
Chessman = namedtuple('Chessman', 'Name Value Color')   #棋子 
Point = namedtuple('Point', 'X Y')                      #棋盘坐标点 

BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))      #黑色棋子，RGB(45, 45, 45)
WHITE_CHESSMAN = Chessman('白子', 2, (219, 219, 219))   #白色棋子，RGB(219, 219, 219)

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]          #四个方向：水平、垂直、主对角线、副对角线


'''
name: Difficulty
description: 棋力难度枚举，EASY（简单）: 40%随机落子，60%基本评估；MEDIUM（中等）: 基本评估；HARD（困难）: 加强评估，优先考虑己方连子
'''
class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

'''
name: Checkerboard
description: 棋盘类，负责维护棋盘状态、落子逻辑和胜利检测
'''
class Checkerboard:
    def __init__(self, line_points):
        #初始化棋盘，设置边长，创建二维列表表示棋盘状态（0=空，1=黑子，2=白子）
        self._line_points = line_points
        self._board = [[0] * line_points for _ in range(line_points)]

    @property
    def board(self):
        return self._board

    def reset(self):
        #重置棋盘状态为全空
        self._board = [[0] * self._line_points for _ in range(self._line_points)]

    def can_drop(self, point):
        #检查指定点是否可以落子
        return self._board[point.Y][point.X] == 0

    def drop(self, chessman, point):
        #落子，检查是否形成五子连线，返回胜利棋子和连线点列表
        if not self.can_drop(point):
            return None, []
        self._board[point.Y][point.X] = chessman.Value
        win_line = self._get_win_line(point)
        if win_line:
            return chessman, win_line
        return None, []

    def _get_win_line(self, point):
        #检查指定点是否形成五子连线，返回连线点列表
        cur_value = self._board[point.Y][point.X]
        if cur_value == 0:
            return []
        for dx, dy in DIRECTIONS:
            line_points = self._get_line_points(point, cur_value, dx, dy)
            if len(line_points) >= 5:
                return line_points[:5]  # 只取前五个连子
        return []

    def _get_line_points(self, point, value, dx, dy):
        #获取指定点在给定方向上连续的同色棋子点列表
        points = []
        # 正方向
        for step in range(-5, 6):  # 向两侧各延伸5步，保证能覆盖5连
            x = point.X + step * dx
            y = point.Y + step * dy
            if 0 <= x < self._line_points and 0 <= y < self._line_points and self._board[y][x] == value:
                points.append(Point(x, y))
            else:
                # 如果遇到非己方棋子或空，则截断，但注意需要先收集完整
                pass
        # 由于上面是从-5到+5无序，需要排序使得连续点按顺序
        if not points:
            return []
        # 按投影坐标排序（根据方向）
        if dx != 0:
            points.sort(key=lambda p: p.X)
        elif dy != 0:
            points.sort(key=lambda p: p.Y)
        else:
            return points
        # 找出最长的连续片段
        longest = []
        current = []
        for i, p in enumerate(points):
            if i == 0:
                current.append(p)
            else:
                # 检查是否与前一个点连续
                prev = current[-1]
                if (p.X - prev.X == dx and p.Y - prev.Y == dy) or (dx == 0 and dy == 0):
                    current.append(p)
                else:
                    if len(current) > len(longest):
                        longest = current
                    current = [p]
        if len(current) > len(longest):
            longest = current
        return longest

    # 为了兼容旧版调用的 _win 方法，保留一个向后兼容的接口（但不再使用）
    def _win(self, point):
        return len(self._get_win_line(point)) >= 5


# ==================== 玩家抽象基类 ====================
class Player(ABC):
    def __init__(self, chessman):
        self.chessman = chessman

    @abstractmethod
    def get_move(self, checkerboard):
        pass


class HumanPlayer(Player):
    def __init__(self, chessman, renderer):
        super().__init__(chessman)
        self.renderer = renderer
        self._pending_click = None

    def get_move(self, checkerboard):
        if self._pending_click is not None:
            point = self._pending_click
            self._pending_click = None
            if point and checkerboard.can_drop(point):
                return point
        return None

    def on_mouse_click(self, mouse_pos):
        point = self.renderer.screen_to_board(mouse_pos)
        if point is not None:
            self._pending_click = point


class AIPlayer(Player):
    def __init__(self, chessman, line_points):
        super().__init__(chessman)
        self._line_points = line_points
        self._opponent = BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
        self._board = [[0] * line_points for _ in range(line_points)]
        self.difficulty = Difficulty.MEDIUM

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def update_board(self, point, chessman):
        self._board[point.Y][point.X] = chessman.Value

    def get_move(self, checkerboard):
        if self.difficulty == Difficulty.EASY and random.random() < 0.4:
            empty_points = []
            for i in range(self._line_points):
                for j in range(self._line_points):
                    if self._board[j][i] == 0:
                        empty_points.append(Point(i, j))
            if empty_points:
                point = random.choice(empty_points)
                self._board[point.Y][point.X] = self.chessman.Value
                return point

        best_point = None
        best_score = -1
        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._board[j][i] == 0:
                    score = self._evaluate_point(Point(i, j))
                    if score > best_score:
                        best_score = score
                        best_point = Point(i, j)
                    elif score == best_score and score > 0:
                        if random.randint(0, 100) % 2 == 0:
                            best_point = Point(i, j)
        self._board[best_point.Y][best_point.X] = self.chessman.Value
        return best_point

    def _evaluate_point(self, point):
        total_score = 0
        for dx, dy in DIRECTIONS:
            total_score += self._direction_score(point, dx, dy)
        if self.difficulty == Difficulty.HARD:
            total_score *= 1.2
        return total_score

    def _direction_score(self, point, dx, dy):
        my_count = 0
        opp_count = 0
        my_blocked = 0
        opp_blocked = 0
        my_has_space = None
        opp_has_space = None

        first_color = self._first_stone_color(point, dx, dy)
        if first_color != 0:
            for step in range(1, 6):
                x = point.X + step * dx
                y = point.Y + step * dy
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if first_color == 1:
                        if self._board[y][x] == self.chessman.Value:
                            my_count += 1
                            if my_has_space is False:
                                my_has_space = True
                        elif self._board[y][x] == self._opponent.Value:
                            opp_blocked += 1
                            break
                        else:
                            if my_has_space is None:
                                my_has_space = False
                            else:
                                break
                    elif first_color == 2:
                        if self._board[y][x] == self.chessman.Value:
                            opp_blocked += 1
                            break
                        elif self._board[y][x] == self._opponent.Value:
                            opp_count += 1
                            if opp_has_space is False:
                                opp_has_space = True
                        else:
                            if opp_has_space is None:
                                opp_has_space = False
                            else:
                                break
                else:
                    if first_color == 1:
                        my_blocked += 1
                    else:
                        opp_blocked += 1

        rev_color = self._first_stone_color(point, -dx, -dy)
        if rev_color != 0:
            for step in range(1, 6):
                x = point.X - step * dx
                y = point.Y - step * dy
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if rev_color == 1:
                        if self._board[y][x] == self.chessman.Value:
                            my_count += 1
                            if my_has_space is False:
                                my_has_space = True
                        elif self._board[y][x] == self._opponent.Value:
                            opp_blocked += 1
                            break
                        else:
                            if my_has_space is None:
                                my_has_space = False
                            else:
                                break
                    elif rev_color == 2:
                        if self._board[y][x] == self.chessman.Value:
                            opp_blocked += 1
                            break
                        elif self._board[y][x] == self._opponent.Value:
                            opp_count += 1
                            if opp_has_space is False:
                                opp_has_space = True
                        else:
                            if opp_has_space is None:
                                opp_has_space = False
                            else:
                                break
                else:
                    if rev_color == 1:
                        my_blocked += 1
                    else:
                        opp_blocked += 1

        score = 0
        if my_count >= 4:
            score = 10000
        elif opp_count >= 4:
            score = 9000
        elif my_count == 3:
            if my_blocked == 0:
                score = 1000
            elif my_blocked == 1:
                score = 100
        elif opp_count == 3:
            if opp_blocked == 0:
                score = 900
            elif opp_blocked == 1:
                score = 90
        elif my_count == 2:
            if my_blocked == 0:
                score = 100
            elif my_blocked == 1:
                score = 10
        elif opp_count == 2:
            if opp_blocked == 0:
                score = 90
            elif opp_blocked == 1:
                score = 9
        elif my_count == 1:
            score = 10
        elif opp_count == 1:
            score = 9

        if my_has_space or opp_has_space:
            score /= 2

        if self.difficulty == Difficulty.HARD:
            if my_count >= 2:
                score *= 1.5
        return score

    def _first_stone_color(self, point, dx, dy):
        x = point.X + dx
        y = point.Y + dy
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._board[y][x] == self.chessman.Value:
                return 1
            elif self._board[y][x] == self._opponent.Value:
                return 2
            else:
                return self._first_stone_color(Point(x, y), dx, dy)
        return 0


'''
name: Renderer
description: 棋盘渲染器，负责绘制棋盘、棋子、游戏信息和胜利提示
'''
class Renderer:
    def __init__(self, config):
        self.config = config
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('五子棋')
        self.font_small = pygame.font.SysFont('SimHei', 28)
        self.font_large = pygame.font.SysFont('SimHei', 72)
        self.font_info = pygame.font.SysFont('SimHei', 24)

    # 绘制棋盘和棋子，若提供胜利连线则高亮显示
    def draw_board(self, checkerboard, win_line=None):
        self.screen.fill(self.config.BOARD_COLOR)
        pygame.draw.rect(self.screen, self.config.BORDER_COLOR,
                         (self.config.OUTER_WIDTH, self.config.OUTER_WIDTH,
                          self.config.BORDER_LENGTH, self.config.BORDER_LENGTH),
                         self.config.BORDER_WIDTH)
        start = self.config.START_POS
        size = self.config.CELL_SIZE
        points = self.config.LINE_POINTS
        for i in range(points):
            pygame.draw.line(self.screen, self.config.LINE_COLOR,
                             (start, start + size * i),
                             (start + size * (points - 1), start + size * i), 1)
            pygame.draw.line(self.screen, self.config.LINE_COLOR,
                             (start + size * i, start),
                             (start + size * i, start + size * (points - 1)), 1)

        for i in (3, 9, 15):
            for j in (3, 9, 15):
                radius = 5 if (i == j == 9) else 3
                cx = start + size * i
                cy = start + size * j
                pygame.gfxdraw.aacircle(self.screen, cx, cy, radius, self.config.LINE_COLOR)
                pygame.gfxdraw.filled_circle(self.screen, cx, cy, radius, self.config.LINE_COLOR)

        # 绘制棋子，若在胜利连线上则高亮
        for y, row in enumerate(checkerboard.board):
            for x, val in enumerate(row):
                if val == BLACK_CHESSMAN.Value:
                    self._draw_stone(Point(x, y), BLACK_CHESSMAN.Color, highlight=(win_line and Point(x,y) in win_line))
                elif val == WHITE_CHESSMAN.Value:
                    self._draw_stone(Point(x, y), WHITE_CHESSMAN.Color, highlight=(win_line and Point(x,y) in win_line))

    # 绘制棋子，若highlight为True则添加红色外圈高亮
    def _draw_stone(self, point, color, highlight=False):
        cx = self.config.START_POS + self.config.CELL_SIZE * point.X
        cy = self.config.START_POS + self.config.CELL_SIZE * point.Y
        radius = self.config.STONE_RADIUS
        pygame.gfxdraw.aacircle(self.screen, cx, cy, radius, color)
        pygame.gfxdraw.filled_circle(self.screen, cx, cy, radius, color)
        if highlight:
            # 绘制红色外圈高亮
            highlight_radius = radius + 3
            pygame.gfxdraw.aacircle(self.screen, cx, cy, highlight_radius, (255, 0, 0))
            pygame.gfxdraw.circle(self.screen, cx, cy, highlight_radius, (255, 0, 0))

    # 绘制游戏信息，包括当前玩家、胜利统计、难度和操作提示，若有赢家则显示胜利提示
    def draw_info(self, cur_player, black_win_count, white_win_count, winner, difficulty):
        info_x = self.config.SCREEN_HEIGHT + 20
        self._draw_icon((info_x, self.config.START_POS + 10), BLACK_CHESSMAN.Color)
        self._draw_icon((info_x, self.config.START_POS + 100), WHITE_CHESSMAN.Color)
        self.draw_text('玩家', info_x + 40, self.config.START_POS + 10, (30,30,200))
        self.draw_text('电脑', info_x + 40, self.config.START_POS + 100, (30,30,200))

        battle_y = self.config.SCREEN_HEIGHT - 160
        self.draw_text('战况：', info_x, battle_y, (30,30,200))
        self._draw_icon((info_x, battle_y + 40), BLACK_CHESSMAN.Color)
        self._draw_icon((info_x, battle_y + 100), WHITE_CHESSMAN.Color)
        self.draw_text(f'{black_win_count} 胜', info_x + 40, battle_y + 40, (30,30,200))
        self.draw_text(f'{white_win_count} 胜', info_x + 40, battle_y + 100, (30,30,200))

        hint_y = battle_y - 70
        diff_text = f"难度: {difficulty.name}"
        self.draw_text(diff_text, info_x, hint_y, (0,0,0), font=self.font_info)
        self.draw_text("R: 新的一局", info_x, hint_y - 30, (80,80,80), font=self.font_info)
        self.draw_text("1/2/3: 切换难度", info_x, hint_y - 60, (80,80,80), font=self.font_info)

        if winner:
            win_text = winner.Name + '获胜'
            fw, fh = self.font_large.size(win_text)
            self.draw_text(win_text, (self.config.SCREEN_WIDTH - fw)//2,
                           (self.config.SCREEN_HEIGHT - fh)//2, (200,30,30), use_large=True)
    
    # 绘制信息区域的小图标，用于显示当前玩家和胜利统计
    def _draw_icon(self, pos, color):
        cx, cy = pos
        radius = self.config.STONE_RADIUS + 3
        pygame.gfxdraw.aacircle(self.screen, cx, cy, radius, color)
        pygame.gfxdraw.filled_circle(self.screen, cx, cy, radius, color)
    
    # 绘制文本信息，支持选择字体大小和颜色
    def draw_text(self, text, x, y, color, use_large=False, font=None):
        if font is None:
            font = self.font_large if use_large else self.font_small
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    # 将屏幕坐标转换为棋盘坐标，返回Point对象或None
    def screen_to_board(self, click_pos):
        px = click_pos[0] - self.config.START_POS
        py = click_pos[1] - self.config.START_POS
        if px < -self.config.INSIDE_WIDTH or py < -self.config.INSIDE_WIDTH:
            return None
        x = px // self.config.CELL_SIZE
        y = py // self.config.CELL_SIZE
        if px % self.config.CELL_SIZE > self.config.STONE_RADIUS:
            x += 1
        if py % self.config.CELL_SIZE > self.config.STONE_RADIUS:
            y += 1
        if 0 <= x < self.config.LINE_POINTS and 0 <= y < self.config.LINE_POINTS:
            return Point(x, y)
        return None


# ==================== 配置类 ====================
class GameConfig:
    CELL_SIZE = 30              #每个格子的像素大小
    LINE_POINTS = 19            #棋盘边长（格子数），标准五子棋为19x19  
    OUTER_WIDTH = 20            #棋盘外边距，确保棋盘不贴边显示
    BORDER_WIDTH = 4            #棋盘边框宽度，增加视觉分隔感
    INSIDE_WIDTH = 4            #棋盘内边距，确保棋盘线条不贴边框显示
    BORDER_LENGTH = CELL_SIZE * (LINE_POINTS - 1) + INSIDE_WIDTH * 2 + BORDER_WIDTH    #边框实际覆盖的长度，包含内边距和边框宽度    
    START_POS = OUTER_WIDTH + BORDER_WIDTH // 2 + INSIDE_WIDTH                         #棋盘起始位置
    SCREEN_HEIGHT = CELL_SIZE * (LINE_POINTS - 1) + OUTER_WIDTH * 2 + BORDER_WIDTH + INSIDE_WIDTH * 2   #屏幕高度，刚好容纳棋盘和边距
    SCREEN_WIDTH = SCREEN_HEIGHT + 220  #屏幕宽度，预留信息显示区域
    STONE_RADIUS = CELL_SIZE // 2 - 3   #棋子半径，稍微小于格子的一半，确保棋子不会触碰到棋盘线条
    BOARD_COLOR = (0xE3, 0x92, 0x65)    #棋盘颜色，RGB(227, 146, 101)，类似木质棋盘的颜色
    LINE_COLOR = (0, 0, 0)              #棋盘线条颜色
    BORDER_COLOR = (0, 0, 0)            #棋盘边框颜色


# ==================== 游戏主控类 ====================
class Game:
    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.renderer = Renderer(self.config)
        self.board = Checkerboard(self.config.LINE_POINTS)
        self.black_win_count = 0
        self.white_win_count = 0
        self.winner = None
        self.win_line = []          # 保存胜利连线点
        self.current_player = None
        self.human = None
        self.ai = None
        self._init_players()
        self.difficulty = Difficulty.MEDIUM
        self.ai.set_difficulty(self.difficulty)

    def _init_players(self):
        self.human = HumanPlayer(BLACK_CHESSMAN, self.renderer)
        self.ai = AIPlayer(WHITE_CHESSMAN, self.config.LINE_POINTS)
        self.current_player = self.human

    def reset_game(self):
        self.board.reset()
        self.ai._board = [[0] * self.config.LINE_POINTS for _ in range(self.config.LINE_POINTS)]
        self.winner = None
        self.win_line = []
        self.current_player = self.human

    def switch_player(self):
        self.current_player = self.human if self.current_player == self.ai else self.ai

    def handle_move(self, point, player):
        winner, win_line = self.board.drop(player.chessman, point)
        # 同步AI内部棋盘
        self.ai.update_board(point, player.chessman)
        if winner:
            self.winner = winner
            self.win_line = win_line
            if winner == BLACK_CHESSMAN:
                self.black_win_count += 1
            else:
                self.white_win_count += 1
            return True
        return False

    def change_difficulty(self, new_difficulty):
        if new_difficulty != self.difficulty:
            self.difficulty = new_difficulty
            self.ai.set_difficulty(self.difficulty)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.reset_game()
                    if event.key == K_1:
                        self.change_difficulty(Difficulty.EASY)
                    elif event.key == K_2:
                        self.change_difficulty(Difficulty.MEDIUM)
                    elif event.key == K_3:
                        self.change_difficulty(Difficulty.HARD)
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.winner is None and self.current_player == self.human:
                        self.human.on_mouse_click(pygame.mouse.get_pos())

            # 人类玩家
            if self.winner is None and self.current_player == self.human:
                move = self.human.get_move(self.board)
                if move:
                    if self.handle_move(move, self.human):
                        pass
                    else:
                        self.switch_player()

            # AI 玩家
            if self.winner is None and self.current_player == self.ai:
                move = self.ai.get_move(self.board)
                if move:
                    if self.handle_move(move, self.ai):
                        pass
                    else:
                        self.switch_player()

            # 绘制，传入胜利连线
            self.renderer.draw_board(self.board, win_line=self.win_line)
            self.renderer.draw_info(self.current_player, self.black_win_count,
                                    self.white_win_count, self.winner, self.difficulty)
            pygame.display.flip()
            clock.tick(30)


if __name__ == '__main__':
    game = Game()
    game.run()