import pygame
import random
import math
import time

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
# 金色系
GOLD = (255, 215, 0)  # 金色
GOLD_LIGHT = (255, 235, 59)  # 浅金色（高光）
GOLD_DARK = (184, 134, 11)  # 深金色（阴影）
# 黑金色系
BLACK_GOLD = (139, 120, 50)  # 黑金色（主色）
BLACK_GOLD_LIGHT = (205, 173, 0)  # 浅黑金色（高光）
BLACK_GOLD_DARK = (85, 65, 0)  # 深黑金色（阴影）
# 灰色系（墙体）
GRAY_DARK = (64, 64, 64)  # 深灰色（阴影）
GRAY_MID = (128, 128, 128)  # 中灰色（主色）
GRAY_LIGHT = (192, 192, 192)  # 浅灰色（高光）

# 游戏状态
class GameState:
    MENU = 0
    COUNTDOWN = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4
    SUCCESS = 5

class Tank:
    def __init__(self, x, y, color, is_player=False):
        self.x = x
        self.y = y
        self.color = color
        self.is_player = is_player
        self.width = 30
        self.height = 30
        self.direction = 0  # 0: 上, 1: 右, 2: 下, 3: 左
        self.speed = 3 if is_player else 0.3  # 玩家速度是敌方的10倍
        self.health = 10 if is_player else 1
        self.max_health = 10 if is_player else 1
        self.last_shot = 0
        self.shot_cooldown = 500 if is_player else 2000  # 玩家射击冷却时间更短
        self.alive = True
        
    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 边界检查
        if 0 <= new_x <= SCREEN_WIDTH - self.width:
            self.x = new_x
        if 0 <= new_y <= SCREEN_HEIGHT - self.height:
            self.y = new_y
    
    def rotate(self, direction):
        self.direction = direction
    
    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot > self.shot_cooldown
    
    def shoot(self):
        if self.can_shoot():
            self.last_shot = pygame.time.get_ticks()
            bullet_speed = 8 if self.is_player else 0.8  # 玩家子弹速度是敌方的10倍
            
            # 根据方向计算子弹起始位置和方向
            if self.direction == 0:  # 上
                bullet_x = self.x + self.width // 2
                bullet_y = self.y
                bullet_dx = 0
                bullet_dy = -bullet_speed
            elif self.direction == 1:  # 右
                bullet_x = self.x + self.width
                bullet_y = self.y + self.height // 2
                bullet_dx = bullet_speed
                bullet_dy = 0
            elif self.direction == 2:  # 下
                bullet_x = self.x + self.width // 2
                bullet_y = self.y + self.height
                bullet_dx = 0
                bullet_dy = bullet_speed
            else:  # 左
                bullet_x = self.x
                bullet_y = self.y + self.height // 2
                bullet_dx = -bullet_speed
                bullet_dy = 0
            
            return Bullet(bullet_x, bullet_y, bullet_dx, bullet_dy, self.is_player)
        return None
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
    
    def draw(self, screen):
        if not self.alive:
            return
        
        # 根据玩家类型选择颜色
        if self.is_player:
            # 玩家：黑金色
            base_color = BLACK_GOLD
            light_color = BLACK_GOLD_LIGHT
            dark_color = BLACK_GOLD_DARK
            cannon_color = BLACK_GOLD_LIGHT
        else:
            # 敌人：金色
            base_color = GOLD
            light_color = GOLD_LIGHT
            dark_color = GOLD_DARK
            cannon_color = GOLD_LIGHT
        
        # 绘制立体坦克主体
        # 1. 先绘制主体 - 主色（作为基础）
        pygame.draw.rect(screen, base_color, 
                        (self.x, self.y, self.width, self.height))
        
        # 2. 绘制顶部和左侧高光（模拟光照）
        # 顶部高光
        pygame.draw.rect(screen, light_color, 
                        (self.x + 2, self.y + 2, self.width - 4, 8))
        # 左侧高光
        pygame.draw.rect(screen, light_color, 
                        (self.x + 2, self.y + 2, 8, self.height - 4))
        
        # 3. 绘制底部和右侧阴影（模拟阴影）
        # 底部阴影
        pygame.draw.rect(screen, dark_color, 
                        (self.x + 2, self.y + self.height - 8, self.width - 4, 8))
        # 右侧阴影
        pygame.draw.rect(screen, dark_color, 
                        (self.x + self.width - 8, self.y + 8, 8, self.height - 10))
        
        # 4. 绘制边缘轮廓（增强立体感）
        # 顶部边缘
        pygame.draw.line(screen, light_color, 
                        (self.x + 2, self.y + 2), 
                        (self.x + self.width - 2, self.y + 2), 2)
        # 左侧边缘
        pygame.draw.line(screen, light_color, 
                        (self.x + 2, self.y + 2), 
                        (self.x + 2, self.y + self.height - 2), 2)
        # 底部边缘
        pygame.draw.line(screen, dark_color, 
                        (self.x + 2, self.y + self.height - 2), 
                        (self.x + self.width - 2, self.y + self.height - 2), 2)
        # 右侧边缘
        pygame.draw.line(screen, dark_color, 
                        (self.x + self.width - 2, self.y + 2), 
                        (self.x + self.width - 2, self.y + self.height - 2), 2)
        
        # 5. 绘制中心装饰（增加立体感）
        center_rect_size = 10
        center_x = self.x + (self.width - center_rect_size) // 2
        center_y = self.y + (self.height - center_rect_size) // 2
        # 中心阴影
        pygame.draw.rect(screen, dark_color, 
                        (center_x + 1, center_y + 1, center_rect_size, center_rect_size))
        # 中心主体
        pygame.draw.rect(screen, base_color, 
                        (center_x, center_y, center_rect_size, center_rect_size))
        # 中心高光
        pygame.draw.rect(screen, light_color, 
                        (center_x + 1, center_y + 1, center_rect_size - 3, center_rect_size - 3))
        
        # 绘制坦克炮管（立体效果）
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        cannon_thickness = 6
        cannon_length = 22
        
        if self.direction == 0:  # 上
            # 炮管底部阴影
            pygame.draw.line(screen, dark_color, 
                           (center_x + 1, center_y - 1), 
                           (center_x + 1, center_y - cannon_length + 1), cannon_thickness + 1)
            # 炮管主体
            pygame.draw.line(screen, base_color, 
                           (center_x, center_y), 
                           (center_x, center_y - cannon_length), cannon_thickness)
            # 炮管顶部高光
            pygame.draw.line(screen, cannon_color, 
                           (center_x - 1, center_y - 2), 
                           (center_x - 1, center_y - cannon_length + 2), 2)
        elif self.direction == 1:  # 右
            # 炮管底部阴影
            pygame.draw.line(screen, dark_color, 
                           (center_x + 1, center_y + 1), 
                           (center_x + cannon_length - 1, center_y + 1), cannon_thickness + 1)
            # 炮管主体
            pygame.draw.line(screen, base_color, 
                           (center_x, center_y), 
                           (center_x + cannon_length, center_y), cannon_thickness)
            # 炮管顶部高光
            pygame.draw.line(screen, cannon_color, 
                           (center_x + 2, center_y - 1), 
                           (center_x + cannon_length - 2, center_y - 1), 2)
        elif self.direction == 2:  # 下
            # 炮管底部阴影
            pygame.draw.line(screen, dark_color, 
                           (center_x + 1, center_y + 1), 
                           (center_x + 1, center_y + cannon_length - 1), cannon_thickness + 1)
            # 炮管主体
            pygame.draw.line(screen, base_color, 
                           (center_x, center_y), 
                           (center_x, center_y + cannon_length), cannon_thickness)
            # 炮管顶部高光
            pygame.draw.line(screen, cannon_color, 
                           (center_x - 1, center_y + 2), 
                           (center_x - 1, center_y + cannon_length - 2), 2)
        else:  # 左
            # 炮管底部阴影
            pygame.draw.line(screen, dark_color, 
                           (center_x - 1, center_y + 1), 
                           (center_x - cannon_length + 1, center_y + 1), cannon_thickness + 1)
            # 炮管主体
            pygame.draw.line(screen, base_color, 
                           (center_x, center_y), 
                           (center_x - cannon_length, center_y), cannon_thickness)
            # 炮管顶部高光
            pygame.draw.line(screen, cannon_color, 
                           (center_x - 2, center_y - 1), 
                           (center_x - cannon_length + 2, center_y - 1), 2)
        
        # 绘制生命值条（仅玩家）
        if self.is_player and self.health < self.max_health:
            bar_width = self.width
            bar_height = 4
            bar_x = self.x
            bar_y = self.y - 8
            
            # 背景
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            # 生命值
            health_width = int(bar_width * (self.health / self.max_health))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Bullet:
    def __init__(self, x, y, dx, dy, is_player_bullet=False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 3
        self.is_player_bullet = is_player_bullet
        self.alive = True
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        # 检查是否超出屏幕
        if (self.x < 0 or self.x > SCREEN_WIDTH or 
            self.y < 0 or self.y > SCREEN_HEIGHT):
            self.alive = False
    
    def draw(self, screen):
        if self.alive:
            # 玩家子弹：黑金色，敌人子弹：金色
            if self.is_player_bullet:
                # 绘制黑金色子弹（立体效果）
                pygame.draw.circle(screen, BLACK_GOLD_DARK, (int(self.x) + 1, int(self.y) + 1), self.radius)
                pygame.draw.circle(screen, BLACK_GOLD, (int(self.x), int(self.y)), self.radius)
                pygame.draw.circle(screen, BLACK_GOLD_LIGHT, (int(self.x) - 1, int(self.y) - 1), self.radius - 1)
            else:
                # 绘制金色子弹（立体效果）
                pygame.draw.circle(screen, GOLD_DARK, (int(self.x) + 1, int(self.y) + 1), self.radius)
                pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.radius)
                pygame.draw.circle(screen, GOLD_LIGHT, (int(self.x) - 1, int(self.y) - 1), self.radius - 1)

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.health = 10  # 墙体生命值
        self.max_health = 10
        self.alive = True
    
    def take_damage(self):
        """墙体受到伤害"""
        self.health -= 1
        if self.health <= 0:
            self.alive = False
    
    def draw(self, screen):
        if not self.alive:
            return
        
        # 根据生命值调整颜色强度（生命值越低越暗）
        health_ratio = self.health / self.max_health
        base_gray = (
            int(GRAY_MID[0] * health_ratio + GRAY_DARK[0] * (1 - health_ratio)),
            int(GRAY_MID[1] * health_ratio + GRAY_DARK[1] * (1 - health_ratio)),
            int(GRAY_MID[2] * health_ratio + GRAY_DARK[2] * (1 - health_ratio))
        )
        light_gray = (
            int(GRAY_LIGHT[0] * health_ratio + GRAY_MID[0] * (1 - health_ratio)),
            int(GRAY_LIGHT[1] * health_ratio + GRAY_MID[1] * (1 - health_ratio)),
            int(GRAY_LIGHT[2] * health_ratio + GRAY_MID[2] * (1 - health_ratio))
        )
        dark_gray = (
            int(GRAY_DARK[0] * health_ratio + (GRAY_DARK[0] * 0.5) * (1 - health_ratio)),
            int(GRAY_DARK[1] * health_ratio + (GRAY_DARK[1] * 0.5) * (1 - health_ratio)),
            int(GRAY_DARK[2] * health_ratio + (GRAY_DARK[2] * 0.5) * (1 - health_ratio))
        )
        
        # 绘制立体墙体主体
        # 1. 先绘制主体 - 主色
        pygame.draw.rect(screen, base_gray, self.rect)
        
        # 2. 绘制顶部和左侧高光（模拟光照）
        highlight_thickness = min(6, max(2, int(self.width * 0.15)))
        # 顶部高光
        pygame.draw.rect(screen, light_gray, 
                        (self.x + 2, self.y + 2, self.width - 4, highlight_thickness))
        # 左侧高光
        pygame.draw.rect(screen, light_gray, 
                        (self.x + 2, self.y + 2, highlight_thickness, self.height - 4))
        
        # 3. 绘制底部和右侧阴影（模拟阴影）
        shadow_thickness = min(6, max(2, int(self.width * 0.15)))
        # 底部阴影
        pygame.draw.rect(screen, dark_gray, 
                        (self.x + 2, self.y + self.height - shadow_thickness, 
                         self.width - 4, shadow_thickness))
        # 右侧阴影
        pygame.draw.rect(screen, dark_gray, 
                        (self.x + self.width - shadow_thickness, self.y + highlight_thickness, 
                         shadow_thickness, self.height - highlight_thickness - 2))
        
        # 4. 绘制边缘轮廓（增强立体感）
        # 顶部边缘
        pygame.draw.line(screen, light_gray, 
                        (self.x + 2, self.y + 2), 
                        (self.x + self.width - 2, self.y + 2), 2)
        # 左侧边缘
        pygame.draw.line(screen, light_gray, 
                        (self.x + 2, self.y + 2), 
                        (self.x + 2, self.y + self.height - 2), 2)
        # 底部边缘
        pygame.draw.line(screen, dark_gray, 
                        (self.x + 2, self.y + self.height - 2), 
                        (self.x + self.width - 2, self.y + self.height - 2), 2)
        # 右侧边缘
        pygame.draw.line(screen, dark_gray, 
                        (self.x + self.width - 2, self.y + 2), 
                        (self.x + self.width - 2, self.y + self.height - 2), 2)
        
        # 5. 绘制砖块纹理（增加真实感）
        brick_size = 12
        for by in range(self.y + 4, self.y + self.height - 4, brick_size):
            for bx in range(self.x + 4, self.x + self.width - 4, brick_size):
                # 绘制砖块阴影
                brick_rect = pygame.Rect(bx + 1, by + 1, brick_size - 2, brick_size - 2)
                pygame.draw.rect(screen, dark_gray, brick_rect, 1)
                # 绘制砖块高光
                pygame.draw.line(screen, light_gray, 
                               (bx + 2, by + 2), 
                               (bx + brick_size - 3, by + 2), 1)

class TankBattleGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("坦克大战")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # 游戏状态
        self.state = GameState.MENU
        self.current_level = 1
        self.max_levels = 3
        self.enemies_killed = 0
        self.enemies_per_level = 10
        
        # 游戏对象
        self.player = None
        self.enemies = []
        self.bullets = []
        self.walls = []
        
        # 倒计时
        self.countdown_time = 0
        self.countdown_duration = 5000  # 5秒倒计时
        
        # 关卡完成计时
        self.level_complete_time = 0
        self.level_complete_duration = 2000  # 2秒显示
        
        self.reset_game()
    
    def reset_game(self):
        self.current_level = 1
        self.enemies_killed = 0
        self.state = GameState.MENU
        self.create_level()
    
    def create_level(self):
        # 创建玩家坦克（黑金色）
        self.player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, BLACK_GOLD, True)
        
        # 清空敌人和子弹
        self.enemies = []
        self.bullets = []
        
        # 创建墙体
        self.walls = []
        self.create_walls()
        
        # 创建敌人坦克
        self.create_enemies()
        
        # 开始倒计时
        self.state = GameState.COUNTDOWN
        self.countdown_time = pygame.time.get_ticks()
    
    def create_walls(self):
        # 重新构建墙体布局 - 创建战略性的地图
        wall_positions = []
        
        # 1. 左侧区域墙体
        wall_positions.extend([
            (50, 100, 120, 20),    # 左上横墙
            (50, 150, 20, 80),     # 左上竖墙
            (150, 200, 80, 20),    # 左中横墙
            (50, 300, 100, 20),    # 左中下横墙
            (50, 400, 20, 100),    # 左下竖墙
        ])
        
        # 2. 中央区域墙体（形成障碍和掩护）
        wall_positions.extend([
            (250, 120, 20, 100),   # 中央左侧竖墙
            (350, 180, 100, 20),   # 中央上方横墙
            (450, 250, 20, 80),    # 中央竖墙
            (300, 350, 120, 20),   # 中央横墙
            (400, 420, 20, 80),    # 中央右侧竖墙
        ])
        
        # 3. 右侧区域墙体
        wall_positions.extend([
            (700, 100, 20, 120),   # 右上竖墙
            (750, 150, 100, 20),   # 右中上横墙
            (830, 200, 20, 100),   # 右中竖墙
            (700, 320, 120, 20),   # 右中下横墙
            (850, 380, 20, 100),   # 右下竖墙
        ])
        
        # 4. 顶部和底部边界墙体（部分遮挡）
        wall_positions.extend([
            (200, 50, 150, 20),    # 顶部左侧横墙
            (650, 50, 150, 20),    # 顶部右侧横墙
            (300, SCREEN_HEIGHT - 70, 200, 20),  # 底部中央横墙（避开玩家起始位置）
            (600, SCREEN_HEIGHT - 70, 150, 20),  # 底部右侧横墙
        ])
        
        # 5. 小型掩护墙体（分散在地图上）
        wall_positions.extend([
            (180, 250, 40, 20),    # 小墙体1
            (520, 280, 40, 20),    # 小墙体2
            (220, 480, 20, 40),    # 小墙体3
            (680, 450, 40, 20),    # 小墙体4
            (480, 550, 20, 40),    # 小墙体5
        ])
        
        # 创建所有墙体
        for pos in wall_positions:
            self.walls.append(Wall(*pos))
    
    def create_enemies(self):
        # 随机生成敌人坦克位置
        for _ in range(self.enemies_per_level):
            attempts = 0
            while attempts < 100:  # 限制尝试次数，避免无限循环
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 200)  # 避免生成在玩家附近
                
                # 检查是否与墙体碰撞（只检查存活的墙体）
                enemy_rect = pygame.Rect(x, y, 30, 30)
                collision = False
                for wall in self.walls:
                    if wall.alive and enemy_rect.colliderect(wall.rect):
                        collision = True
                        break
                
                # 检查是否与玩家太近
                if self.player:
                    player_rect = pygame.Rect(self.player.x, self.player.y, 
                                            self.player.width, self.player.height)
                    if enemy_rect.colliderect(player_rect):
                        collision = True
                
                if not collision:
                    enemy = Tank(x, y, GOLD, False)  # 金色敌人坦克
                    enemy.direction = random.randint(0, 3)
                    self.enemies.append(enemy)
                    break
                
                attempts += 1
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if self.state == GameState.PLAYING and self.player.alive:
            # 移动控制
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.move(0, -1)
                self.player.rotate(0)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.move(0, 1)
                self.player.rotate(2)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-1, 0)
                self.player.rotate(3)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(1, 0)
                self.player.rotate(1)
            
            # 射击控制
            if keys[pygame.K_SPACE]:
                bullet = self.player.shoot()
                if bullet:
                    self.bullets.append(bullet)
    
    def update_enemies(self):
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            
            # 简单的AI：随机移动和射击
            if random.random() < 0.02:  # 2%概率改变方向
                enemy.direction = random.randint(0, 3)
            
            # 移动
            if enemy.direction == 0:  # 上
                enemy.move(0, -1)
            elif enemy.direction == 1:  # 右
                enemy.move(1, 0)
            elif enemy.direction == 2:  # 下
                enemy.move(0, 1)
            else:  # 左
                enemy.move(-1, 0)
            
            # 随机射击
            if random.random() < 0.01:  # 1%概率射击
                bullet = enemy.shoot()
                if bullet:
                    self.bullets.append(bullet)
    
    def check_collisions(self):
        # 子弹与坦克碰撞
        for bullet in self.bullets[:]:
            if not bullet.alive:
                continue
            
            bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, 
                                    bullet.radius * 2, bullet.radius * 2)
            
            # 检查与玩家坦克碰撞
            if not bullet.is_player_bullet and self.player.alive:
                player_rect = pygame.Rect(self.player.x, self.player.y, 
                                        self.player.width, self.player.height)
                if bullet_rect.colliderect(player_rect):
                    self.player.take_damage()
                    bullet.alive = False
                    if not self.player.alive:
                        self.state = GameState.GAME_OVER
            
            # 检查与敌人坦克碰撞
            if bullet.is_player_bullet:
                for enemy in self.enemies:
                    if not enemy.alive:
                        continue
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    if bullet_rect.colliderect(enemy_rect):
                        enemy.take_damage()
                        bullet.alive = False
                        if not enemy.alive:
                            self.enemies_killed += 1
                            if self.enemies_killed >= self.enemies_per_level:
                                self.state = GameState.LEVEL_COMPLETE
                                self.level_complete_time = pygame.time.get_ticks()
                        break
        
        # 子弹与墙体碰撞
        for bullet in self.bullets[:]:
            if not bullet.alive:
                continue
            
            bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, 
                                    bullet.radius * 2, bullet.radius * 2)
            
            for wall in self.walls:
                if not wall.alive:
                    continue
                if bullet_rect.colliderect(wall.rect):
                    wall.take_damage()  # 减少墙体生命值
                    bullet.alive = False
                    # 墙体生命值归零后会在update中自动清理
                    break
        
        # 坦克与墙体碰撞
        for tank in [self.player] + self.enemies:
            if not tank.alive:
                continue
            
            tank_rect = pygame.Rect(tank.x, tank.y, tank.width, tank.height)
            for wall in self.walls:
                if not wall.alive:
                    continue
                if tank_rect.colliderect(wall.rect):
                    # 简单的碰撞回退
                    if tank.x < wall.x:
                        tank.x = wall.x - tank.width
                    elif tank.x > wall.x:
                        tank.x = wall.x + wall.width
                    if tank.y < wall.y:
                        tank.y = wall.y - tank.height
                    elif tank.y > wall.y:
                        tank.y = wall.y + wall.height
    
    def update(self):
        if self.state == GameState.COUNTDOWN:
            elapsed = pygame.time.get_ticks() - self.countdown_time
            if elapsed >= self.countdown_duration:
                self.state = GameState.PLAYING
        
        elif self.state == GameState.PLAYING:
            self.handle_input()
            self.update_enemies()
            
            # 清理死亡的墙体
            self.walls = [wall for wall in self.walls if wall.alive]
            
            # 更新子弹
            for bullet in self.bullets[:]:
                bullet.update()
                if not bullet.alive:
                    self.bullets.remove(bullet)
            
            self.check_collisions()
        
        elif self.state == GameState.LEVEL_COMPLETE:
            elapsed = pygame.time.get_ticks() - self.level_complete_time
            if elapsed >= self.level_complete_duration:
                if self.current_level >= self.max_levels:
                    self.state = GameState.SUCCESS
                else:
                    self.current_level += 1
                    self.enemies_killed = 0
                    self.create_level()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.COUNTDOWN:
            self.draw_countdown()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_level_complete()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.SUCCESS:
            self.draw_success()
        
        pygame.display.flip()
    
    def draw_menu(self):
        title_text = self.big_font.render("坦克大战", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(title_text, title_rect)
        
        start_text = self.font.render("按空格键开始游戏", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(start_text, start_rect)
    
    def draw_countdown(self):
        elapsed = pygame.time.get_ticks() - self.countdown_time
        remaining = max(0, self.countdown_duration - elapsed)
        
        if remaining > 4000:
            text = "5"
        elif remaining > 3000:
            text = "4"
        elif remaining > 2000:
            text = "3"
        elif remaining > 1000:
            text = "2"
        elif remaining > 0:
            text = "1"
        else:
            text = "开始"
        
        countdown_text = self.big_font.render(text, True, YELLOW)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(countdown_text, countdown_rect)
    
    def draw_game(self):
        # 绘制墙体
        for wall in self.walls:
            wall.draw(self.screen)
        
        # 绘制坦克
        if self.player.alive:
            self.player.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # 绘制UI
        level_text = self.font.render(f"第{self.current_level}关", True, WHITE)
        self.screen.blit(level_text, (10, 10))
        
        kills_text = self.font.render(f"击毁: {self.enemies_killed}/{self.enemies_per_level}", True, WHITE)
        self.screen.blit(kills_text, (10, 50))
    
    def draw_level_complete(self):
        complete_text = self.big_font.render(f"第{self.current_level}关完成!", True, GREEN)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(complete_text, complete_rect)
    
    def draw_game_over(self):
        game_over_text = self.big_font.render("游戏结束", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_text = self.font.render("按R键重新开始", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_success(self):
        success_text = self.big_font.render("胜利", True, GREEN)
        success_rect = success_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(success_text, success_rect)
        
        restart_text = self.font.render("按R键重新开始", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == GameState.MENU:
                        self.create_level()
                    elif event.key == pygame.K_r and (self.state == GameState.GAME_OVER or self.state == GameState.SUCCESS):
                        self.reset_game()
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = TankBattleGame()
    game.run()
