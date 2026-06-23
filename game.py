import pygame, random
from snake import Snake, Food, Objects, Power_box, random_position
from settings import *  
import json, os
from sound import play_eat_sound, play_power_sound, play_game_over_sound

# ─────────────────────────────────────────────
# مسیر فایل JSON برای ذخیره و بارگذاری امتیازها
# ─────────────────────────────────────────────
Path = "data/scores.json"


def load_scores():
    """امتیازهای ذخیره‌شده رو از فایل JSON میخونه؛ اگه فایل نبود لیست خالی برمیگردونه."""
    if not os.path.exists(Path):
        return []
    with open(Path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_scores(name, score):
   # امتیاز جدید رو ذخیره میکنه و فقط ۱۰ رکورد برتر رو نگه میداره.
    scores = load_scores()                             
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    os.makedirs("data", exist_ok=True)                 
    with open(Path, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False)        # با پشتیبانی از فارسی ذخیره کن


# ═══════════════════════════════════════════════
# کلاس Game: مدیریت اصلی منطق و حلقه بازی
# ═══════════════════════════════════════════════
class Game:
    def __init__(self, difficulty="normal"):
        # ساخت اشیاء اصلی بازی
        self.snake = Snake()
        self.food = Food()

        # تعداد موانع بر اساس سطح سختی
        obstacle_count = 0 if difficulty == "easy" else 6 if difficulty == "normal" else 10
        self.obstacle = Objects(obstacle_count)

        # جعبه پاورآپ و وضعیت نمایش اون
        self.power_box = Power_box()
        self.power_visible = False                          
        self.last_visible_time = pygame.time.get_ticks()   

        # متغیرهای وضعیت بازی
        self.score = 0
        self.difficulty = difficulty
        self.game_over = False
        self.won = False   

        # نوع پاورآپ فعال ("invincible" / "speed" / None) و زمان پایانش
        self.active_power = None
        self.power_end_tick = 0     

        # چیدمان اولیه همه اشیاء به‌طوری که روی هم نیفتند
        self.relocate_all()

        self.paused = False

    def occupied(self):
        #مجموعه همه خانه‌های اشغال‌شده (بدن مار + سنگ‌ها) رو برمیگردونه.
        return set(self.snake.body) | set(self.obstacle.position)

    def random_free_cell(self):
        #یه خانه تصادفی که آزاد باشه (نه روی مار، نه روی سنگ) برمیگردونه.
        occ = self.occupied()
        while True:
            p = random_position()
            if p not in occ:    
                return p

    def relocate_all(self):
        """
        موقعیت همه اشیاء (سنگ‌ها، غذا، جعبه پاورآپ) رو به‌طور تصادفی
        دوباره تعیین میکنه تا روی بدن مار یا روی هم نیفتند.
        """
        occupied = set(self.snake.body)     
        new_obstacles = []
        for _ in range(len(self.obstacle.position)):
            while True:
                p = random_position()
                if p not in occupied:
                    new_obstacles.append(p)
                    occupied.add(p)        
                    break
        self.obstacle.position = new_obstacles
        self.food.position = self.random_free_cell()
        self.power_box.position = self.random_free_cell()

    def power_active(self):
        """True برمیگردونه اگه هنوز تایمر پاورآپ تموم نشده باشه."""
        return pygame.time.get_ticks() < self.power_end_tick

    def check_win(self):
        # همه خانه‌های داخل گرید (بدون دیوار)
        all_inner_cells = set(
            (x, y)
            for x in range(1, grid_size - 1)
            for y in range(1, grid_size - 1)
        )

        # خانه‌های در دسترس = همه داخلی‌ها منهای موانع
        available_cells = all_inner_cells - set(self.obstacle.position)

        # اگه بدن مار همه خانه‌های در دسترس رو پر کرد → برنده!
        return set(self.snake.body) >= available_cells

    def update(self):
        """
        منطق اصلی هر فریم بازی:
        حرکت مار، بررسی برخوردها، خوردن غذا و پاورآپ، مدیریت تایمرها.
        """
        # اگه بازی تموم شده هیچ‌کاری نکن
        if self.game_over:
            return

        # اگه تایمر پاورآپ تموم شده، همه اثرها رو خاموش کن
        if not self.power_active():
            self.snake.invincible = False
            self.snake.speed_boost = False
            self.active_power = None

        # حرکت مار — wrap فقط در حالت invincible فعاله
        self.snake.move(wrap_enable=self.snake.invincible)
        head = self.snake.body[0]   # موقعیت جدید سر مار

        # ── بررسی برخوردها ──────────────────
        if not self.snake.invincible:

            # برخورد با دیوار
            if head[0] <= 0 or head[0] >= grid_size - 1 or head[1] <= 0 or head[1] >= grid_size - 1:
                self.game_over = True
                play_game_over_sound()
                return

            # برخورد با بدن خودش (از قطعه دوم به بعد)
            if head in self.snake.body[1:]:
                self.game_over = True
                play_game_over_sound()
                return

            # برخورد با موانع سنگی
            if head in self.obstacle.position:
                self.game_over = True
                play_game_over_sound()
                return

        # ── خوردن غذا ────────────────────────────────────────────────────────
        if head == self.food.position:
            self.snake.grow()          
            self.score += 10            
            play_eat_sound()

            # بررسی شرط برنده شدن بعد از هر غذا خوردن
            if self.check_win():
                self.won = True
                self.game_over = True   
                return

            self.relocate_all()       

        # ── مدیریت نمایش جعبه پاورآپ ─────────────────────────────────────────
        current_time = pygame.time.get_ticks()

        if not self.power_visible:
            # هر ۱۰ ثانیه یه‌بار جعبه ظاهر میشه
            if current_time - self.last_visible_time > 10000:
                self.power_visible = True
                self.power_box.position = self.random_free_cell()
                self.last_visible_time = current_time

        # ── خوردن جعبه پاورآپ ────────────────────────────────────────────────
        if self.power_visible and head == self.power_box.position:
            self.power_visible = False
            self.last_visible_time = current_time
            play_power_sound()
            effect = random.choice(["invincible", "score_boost", "speed_boost"])

            if effect == "invincible":
                self.snake.invincible = True
                self.snake.speed_boost = False
                self.active_power = "invincible"
                self.power_end_tick = pygame.time.get_ticks() + 5000

            elif effect == "speed_boost":
                self.snake.speed_boost = True
                self.snake.invincible = False
                self.active_power = "speed"
                self.power_end_tick = pygame.time.get_ticks() + 5000

            else:   # score_boost
                self.score += 50
                self.snake.grow(amount=5)
                self.active_power = None
                self.power_end_tick = 0

            self.relocate_all()

    def power_seconds_left(self):
        """ ثانیه‌های باقی‌مونده از پاورآپ فعال رو برمیگردونه. """
        if not self.power_active():    
            return 0
        return max(0, (self.power_end_tick - pygame.time.get_ticks()) / 1000.0)
