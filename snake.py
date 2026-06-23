import pygame
import random
from settings import cell_size, Colors, grid_size

# ─────────────────────────────────────────────
# تابع کمکی: تولید موقعیت تصادفی در داخل گرید
# از خانه ۱ تا grid_size-2 تا مار روی دیوار spawn نشه
# ─────────────────────────────────────────────
def random_position():
    return (random.randint(1, grid_size - 2), random.randint(1, grid_size - 2))


# ═══════════════════════════════════════════════
# کلاس Snake: مدیریت حرکت، رشد و رسم مار
# ═══════════════════════════════════════════════
class Snake:
    def __init__(self):
        self.body = [(15, 15)]
        self.dir = (1, 0)
        self.invincible = False
        self.speed_boost = False
    def move(self, wrap_enable=False):
        head = self.body[0]
        new_head = (head[0] + self.dir[0], head[1] + self.dir[1])
        if wrap_enable:
            new_head = (new_head[0] % grid_size, new_head[1] % grid_size)

        # بدن جدید: سر جدید + تمام بدن قدیمی به‌جز دُم آخر (شبیه‌سازی حرکت)
        self.body = [new_head] + self.body[:-1]

    def grow(self, amount=1):
        # برای هر واحد رشد، آخرین قطعه بدن رو کپی و اضافه میکنیم
        for i in range(amount):
            self.body.append(self.body[-1])

    def set_dir(self, dx, dy):
        # از برگشت ۱۸۰ درجه جلوگیری میکنیم (نمیذاریم مار مستقیم برگرده)
        if (dx, dy) != (-self.dir[0], -self.dir[1]):
            self.dir = (dx, dy)

    def draw(self, screen):
        # روی تمام قطعه‌های بدن loop میزنیم — i=0 یعنی سر مار
        for i, (x, y) in enumerate(self.body):

       
            if self.invincible:
                color = Colors.get("invincible", (255, 255, 255))
            elif self.speed_boost:
                color = Colors.get("speed", (255, 69, 0))
            else:
                color = Colors["snake_head"] if i == 0 else Colors["snake"]

            # تعریف مستطیل هر قطعه بر اساس موقعیت گرید × اندازه خانه
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)

            # ۱. رسم بدنه اصلی با گوشه‌های گرد (border_radius=5)
            pygame.draw.rect(screen, color, rect, border_radius=5)

            # ۲. رسم یک حاشیه ظریف تیره دور هر بلوک برای عمق دادن به گرافیک
            pygame.draw.rect(screen, (30, 30, 30), rect, 1, border_radius=5)

            # ۳. اضافه کردن چشم فقط برای سر مار (i==0)
            if i == 0:
                eye_color = (255, 255, 255)
                # مرکز سر مار رو حساب میکنیم
                eye_pos = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
                pygame.draw.circle(screen, eye_color, eye_pos, 3)


# ═══════════════════════════════════════════════
# کلاس Food: غذایی که مار باید بخوره
# ═══════════════════════════════════════════════
class Food:
    def __init__(self):
        # موقعیت اولیه غذا به صورت تصادفی تعیین میشه
        self.position = random_position()

    def draw(self, screen):
        # محاسبه مرکز بلاک برای رسم دایره
        center_x = self.position[0] * cell_size + cell_size // 2
        center_y = self.position[1] * cell_size + cell_size // 2
        radius = cell_size // 2 - 2

        # ۱. رسم سایه کوچک زیر غذا (offset 2px) برای جلوه عمق
        pygame.draw.circle(screen, (50, 50, 50), (center_x + 2, center_y + 2), radius)

        # ۲. رسم بدنه اصلی غذا با رنگ تعریف‌شده در settings
        pygame.draw.circle(screen, Colors["food"], (center_x, center_y), radius)

        # ۳. رسم نقطه درخشان (Highlight) در گوشه بالا-چپ برای جلوه براق
        pygame.draw.circle(screen, (255, 200, 200), (center_x - 3, center_y - 3), 3)


# ═══════════════════════════════════════════════
# کلاس Objects: موانع سنگی داخل صحنه
# ═══════════════════════════════════════════════
class Objects:
    def __init__(self, count=5):
        self.position = [random_position() for i in range(count)]

    def draw(self, screen):
        for pos in self.position:
            # مستطیل هر سنگ بر اساس موقعیت گرید
            rect = pygame.Rect(pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size)

            # ۱. رسم بدنه اصلی سنگ (خاکستری) با گوشه‌های کمی گرد
            pygame.draw.rect(screen, Colors["obstacle"], rect, border_radius=3)

            # ۲. رسم حاشیه تیره دور سنگ برای تفکیک از پس‌زمینه
            pygame.draw.rect(screen, (30, 30, 30), rect, 2, border_radius=3)

            # ۳. رسم خط مورب داخلی برای جلوه بافت سنگی
            start_line = (pos[0] * cell_size + 5, pos[1] * cell_size + 5)
            end_line = (pos[0] * cell_size + cell_size - 5, pos[1] * cell_size + cell_size - 5)
            pygame.draw.line(screen, (80, 80, 80), start_line, end_line, 2)


# ═══════════════════════════════════════════════
# کلاس Power_box: جعبه پاورآپ تصادفی
# ═══════════════════════════════════════════════
class Power_box:
    def __init__(self):
        self.position = random_position()
        self.active = True

    def draw(self, screen):
        if self.active:
            rect = pygame.Rect(
                self.position[0] * cell_size,
                self.position[1] * cell_size,
                cell_size, cell_size
            )

            # ۱. رسم هاله درخشان (Glow):
            glow_rect = rect.inflate(4, 4)
            pygame.draw.rect(screen, (255, 255, 200), glow_rect, border_radius=8)

            # ۲. رسم بدنه اصلی جعبه با رنگ طلایی و گوشه گرد
            pygame.draw.rect(screen, Colors["power"], rect, border_radius=6)

            # ۳. رسم مربع کوچک سفید داخلی (نشانه آیتم مخفی)
            inner_rect = rect.inflate(-12, -12)
            pygame.draw.rect(screen, (255, 255, 255), inner_rect, 2)