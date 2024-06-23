import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Константи
WIDTH, HEIGHT = 800, 600
SIZE_BLOCK = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Налаштування вікна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Клас змійки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WIDTH / 2, HEIGHT / 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.color = GREEN
        self.score = 0  # Початковий рахунок

    def move(self, food):
        # Обробка подій клавіш для зміни напрямку
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.change_direction("RIGHT")
                elif event.key == pygame.K_SPACE:
                    self.reset()

        # Рух змійки
        if self.direction == "UP":
            new_head = (self.positions[0][0], self.positions[0][1] - SIZE_BLOCK)
        elif self.direction == "DOWN":
            new_head = (self.positions[0][0], self.positions[0][1] + SIZE_BLOCK)
        elif self.direction == "LEFT":
            new_head = (self.positions[0][0] - SIZE_BLOCK, self.positions[0][1])
        elif self.direction == "RIGHT":
            new_head = (self.positions[0][0] + SIZE_BLOCK, self.positions[0][1])

        # Перевірка, чи змійка виходить за межі екрана
        if new_head[0] < 0:
            new_head = (WIDTH - SIZE_BLOCK, self.positions[0][1])
        elif new_head[0] >= WIDTH:
            new_head = (0, self.positions[0][1])
        elif new_head[1] < 0:
            new_head = (self.positions[0][0], HEIGHT - SIZE_BLOCK)
        elif new_head[1] >= HEIGHT:
            new_head = (self.positions[0][0], 0)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

        # Перевірка, чи змійка з'їла їжу
        if self.positions[0] == food.position:
            self.length += 1
            self.score += 1  # Збільшуємо рахунок
            food.randomize_position()

    def change_direction(self, new_direction):
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def reset(self):
        self.length = 1
        self.positions = [(WIDTH / 2, HEIGHT / 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.score = 0

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(screen, self.color, pygame.Rect(position[0], position[1], SIZE_BLOCK, SIZE_BLOCK))

# Клас їжі
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, WIDTH // SIZE_BLOCK - 1) * SIZE_BLOCK,
                         random.randint(0, HEIGHT // SIZE_BLOCK - 1) * SIZE_BLOCK)

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], SIZE_BLOCK, SIZE_BLOCK))

# Основна функція
def main():
    snake = Snake()
    food = Food()

    font = pygame.font.Font(None, 36)  # Шрифт для відображення тексту

    while True:
        screen.fill(BLACK)

        snake.move(food)  # Передаємо їжу як аргумент в метод move

        # Відображення рахунку
        text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(text, (10, 10))

        snake.draw()
        food.draw()

        pygame.display.update()  # Забезпечуємо правильне оновлення вікна
        clock.tick(5)

if __name__ == "__main__":
    main()
