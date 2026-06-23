import pygame
import sys
from game import Game, load_scores, save_scores
from settings import width, hight, Colors, fps, cell_size
from sound import toggle_sound, is_sound_enabled

# ─────────────────────────────────────────────
# راه‌اندازی اولیه pygame و تنظیمات پنجره
# ─────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((width, hight))          # ساخت پنجره بازی
pygame.display.set_caption("Snake Project - Modern Earthy Theme")
clock = pygame.time.Clock()                                # برای کنترل FPS


# ═══════════════════════════════════════════════
# تابع کمکی: رسم متن روی صفحه
# ═══════════════════════════════════════════════
def draw_text(text, size, x, y, center=False, color=(255, 255, 255)):
    # اگه رنگ پیش‌فرض (سفید) بود، از رنگ تم بازی استفاده میکنیم
    if color == (255, 255, 255):
        color = Colors.get("text", (50, 30, 20))

    font = pygame.font.SysFont("Arial", size, bold=True)  
    img = font.render(text, True, color)                   
    rect = img.get_rect()

    if center:
        rect.center = (x, y)    # وسط‌چین: مرکز متن روی (x, y)
    else:
        rect.topleft = (x, y)   # چپ‌چین: گوشه بالا-چپ روی (x, y)

    screen.blit(img, rect)      # کشیدن متن روی صفحه


# ═══════════════════════════════════════════════
# تابع کمکی: رسم متن با خط تیره دور آن
# برای خوانایی روی هر پس‌زمینه‌ای (مثل تایمر پاورآپ)
# ═══════════════════════════════════════════════
def draw_text_outlined(text, size, x, y, center=False, color=(255, 255, 255), outline_color=(0, 0, 0)):
    font = pygame.font.SysFont("Arial", size, bold=True)

    # ۱. رسم outline: متن تیره رو در ۸ جهت اطراف (offset=2) میکشیم
    outline_img = font.render(text, True, outline_color)
    outline_rect = outline_img.get_rect()

    if center:
        outline_rect.center = (x, y)
    else:
        outline_rect.topleft = (x, y)

    for dx in (-2, 0, 2):
        for dy in (-2, 0, 2):
            if dx != 0 or dy != 0:      # مرکز رو رد میکنیم
                r = outline_rect.move(dx, dy)
                screen.blit(outline_img, r)

    # ۲. رسم متن اصلی با رنگ اصلی روی outline
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)


# ═══════════════════════════════════════════════
# تابع رسم گرید پس‌زمینه و قاب دیواری
# ═══════════════════════════════════════════════
def draw_grid_and_border(screen):
    # ۱. رسم خطوط عمودی گرید با رنگ کمرنگ
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, Colors["grid"], (x, 0), (x, hight))

    # ۲. رسم خطوط افقی گرید
    for y in range(0, hight, cell_size):
        pygame.draw.line(screen, Colors["grid"], (0, y), (width, y))

    # ۳. رسم قاب دیواری — ضخامت برابر یه خانه گرید
    border_thickness = cell_size
    pygame.draw.rect(screen, Colors["border"], (0, 0, width, border_thickness))                          # بالا
    pygame.draw.rect(screen, Colors["border"], (0, hight - border_thickness, width, border_thickness))  # پایین
    pygame.draw.rect(screen, Colors["border"], (0, 0, border_thickness, hight))                         # چپ
    pygame.draw.rect(screen, Colors["border"], (width - border_thickness, 0, border_thickness, hight))  # راست


# ═══════════════════════════════════════════════
# نمایش جدول امتیازات (Scoreboard)
# ═══════════════════════════════════════════════
def show_scoreboard():
    scores = load_scores()  
    running = True

    while running:
        screen.fill(Colors["background"])
        draw_text("Scoreboard", 40, width // 2, hight // 6, center=True)

        if not scores:
            draw_text("No scores yet.", 28, width // 2, hight // 2, center=True)
        else:
            y = hight // 4 + 40
            for i, entry in enumerate(scores):
                line = f"{i+1}. {entry['name']} - {entry['score']}"
                draw_text(line, 28, width // 2, y, center=True)
                y += 35     # هر ردیف ۳۵ پیکسل پایین‌تر از قبلی

        draw_text("Press ESC to return", 22, width // 2, hight - 50, center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False   

# ═══════════════════════════════════════════════
# انتخاب سطح سختی بازی
# ═══════════════════════════════════════════════
def select_difficulty():
    while True:
        screen.fill(Colors["background"])
        draw_text("Select Difficulty", 40, width // 2, hight // 4,      center=True)
        draw_text("1) Easy",           32, width // 2, hight // 2 - 40, center=True)
        draw_text("2) Normal",         32, width // 2, hight // 2,      center=True)
        draw_text("3) Hard",           32, width // 2, hight // 2 + 40, center=True)
        draw_text("Press 1, 2 or 3",  24, width // 2, hight - 60,      center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:   return "easy"
                elif event.key == pygame.K_2: return "normal"
                elif event.key == pygame.K_3: return "hard"


# ═══════════════════════════════════════════════
# دریافت نام بازیکن بعد از پایان بازی
# ═══════════════════════════════════════════════
def ask_player_name(score):
    name = ""
    entering = True

    while entering:
        screen.fill(Colors["background"])
        draw_text("Game Over!", 40, width // 2, hight // 4, center=True)
        draw_text(f"Your score: {score}", 30, width // 2, hight // 4 + 50, center=True)
        draw_text("Enter your name:", 28, width // 2, hight // 2 - 40, center=True)
        draw_text(name or "_", 30, width // 2, hight // 2, center=True)  
        draw_text("ENTER = save,  ESC = skip", 20, width // 2, hight - 60, center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False              
                elif event.key == pygame.K_ESCAPE:
                    return ""                       
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]                
                else:
                    # فقط کاراکترهای قابل چاپ تا حداکثر ۱۲ کاراکتر
                    if len(name) < 12 and event.unicode.isprintable():
                        name += event.unicode

    return name.strip()     # حذف فضاهای اضافه دو طرف


# ═══════════════════════════════════════════════
# نمایش صفحه برنده شدن
# ═══════════════════════════════════════════════
def show_win_screen(score):
    """
    صفحه تبریک برنده شدن رو نمایش میده.
    بازیکن میتونه با ENTER امتیازش رو ثبت کنه یا با ESC رد کنه.
    """
    alpha = 0           # برای fade-in متن
    tick = 0            # شمارنده فریم برای انیمیشن

    while True:
        screen.fill(Colors["background"])
        draw_grid_and_border(screen)

        # ── افکت درخشش پس‌زمینه (overlay طلایی کمرنگ) ──────────────────────
        overlay = pygame.Surface((width, hight), pygame.SRCALPHA)
        pulse = abs((tick % 120) - 60) / 60     # بین 0 و 1 نوسان میکنه
        overlay.fill((255, 215, 0, int(20 + pulse * 30)))  # طلایی شفاف
        screen.blit(overlay, (0, 0))

        # ── متن‌های اصلی با outline ──────────────────────────────────────────
        draw_text_outlined("YOU WIN!", 70, width // 2, hight // 4,
                           center=True,
                           color=(255, 215, 0),          # طلایی
                           outline_color=(80, 50, 0))    # قهوه‌ای تیره

        draw_text_outlined(f"Score: {score}", 36, width // 2, hight // 4 + 80,
                           center=True,
                           color=(255, 255, 200),
                           outline_color=(30, 30, 30))

        draw_text_outlined("You filled the entire board!", 26,
                           width // 2, hight // 2 - 10,
                           center=True,
                           color=(200, 255, 200),        # سبز روشن
                           outline_color=(20, 60, 20))

        draw_text_outlined("ENTER = save score", 22,
                           width // 2, hight - 80,
                           center=True,
                           color=(255, 255, 255),
                           outline_color=(30, 30, 30))

        draw_text_outlined("ESC = skip", 22,
                           width // 2, hight - 50,
                           center=True,
                           color=(200, 200, 200),
                           outline_color=(30, 30, 30))

        pygame.display.flip()
        tick += 1
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True    
                elif event.key == pygame.K_ESCAPE:
                    return False   


def run_game(difficulty):
    game = Game(difficulty)     # ساخت یه بازی جدید با سطح انتخابی
    paused = False

    while True:
        # ── پردازش رویدادها ────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # حرکت با Arrow Keys یا WASD
                if event.key in (pygame.K_UP, pygame.K_w):
                    game.snake.set_dir(0, -1)       # بالا
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game.snake.set_dir(0, 1)        # پایین
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    game.snake.set_dir(-1, 0)       # چپ
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.snake.set_dir(1, 0)        # راست
                elif event.key == pygame.K_p:
                    paused = not paused             # توقف / ادامه بازی
                elif event.key == pygame.K_m:
                    toggle_sound()                  # روشن/خاموش کردن صدا

        # ── بروزرسانی منطق بازی (فقط وقتی pause نیست) ─────────────────────
        if not paused and not game.game_over:
            game.update()

        # ── رسم گرافیک  ──────────────────────────────
        screen.fill(Colors["background"])       

        draw_grid_and_border(screen)            
        game.food.draw(screen)
        game.obstacle.draw(screen)              
        if game.power_visible:
            game.power_box.draw(screen)        
        game.snake.draw(screen)                 

        # ──  روی قاب دیوار ────────────────────────────────

        # امتیاز در سمت چپ بالا (داخل قاب)
        draw_text_outlined(f"Score: {game.score}", 22, cell_size + 10, cell_size // 4,
                  color=Colors["background"], outline_color=(30,30,30))

        # آیکون وضعیت صدا در سمت راست بالا
        if is_sound_enabled():
             sound_text = "Sound: ON [M]"
             sound_color = (100, 255, 100) 
        else:
             sound_text = "Sound: OFF [M]"
             sound_color = (255, 100, 100) 
        draw_text_outlined(sound_text, 22, width - cell_size-110 , cell_size // 4,
                           center=False,color=sound_color, outline_color=(0, 0, 0))

        # تایمر پاورآپ فعال در وسط بالا
        power_ui = {
            "invincible": ("INVINCIBLE", Colors.get("invincible", (255, 255, 255))),
            "speed":      ("SPEED BOOST", Colors.get("speed",      (255, 69,  0)))
        }
        if game.active_power in power_ui:
            t = game.power_seconds_left()
            label, timer_color = power_ui[game.active_power]
            draw_text_outlined(f"{label}: {t:.1f}s", 20, width // 2, cell_size // 2,
                               center=True, color=timer_color, outline_color=(30, 30, 30))

        # نمایش متن PAUSED در وسط صفحه
        if paused:
            draw_text("PAUSED", 50, width // 2, hight // 2,
                      center=True, color=(200, 150, 0))

        pygame.display.flip()   # بروزرسانی نمایش

        # تنظیم FPS: اگه speed_boost فعاله سرعت دو برابر میشه
        current_fps = fps * 2 if game.snake.speed_boost else fps
        clock.tick(current_fps)

        if game.game_over:
            break  

    # ── بعد از پایان بازی: برنده یا بازنده؟ ────────────────────────────────
    if game.won:
        # صفحه برنده شدن نشون میده و اگه ENTER زد نام میگیره
        want_save = show_win_screen(game.score)
        if want_save:
            name = ask_player_name(game.score)
            if name:
                save_scores(name, game.score)
    else:
        # بازی عادی تموم شده (باخت)
        name = ask_player_name(game.score)
        if name:
            save_scores(name, game.score)   # فقط اگه نام وارد شده ذخیره میکنیم


# ═══════════════════════════════════════════════
# منوی اصلی بازی
# ═══════════════════════════════════════════════
def show_main_menu():
    while True:
        screen.fill(Colors["background"])
        draw_text("SNAKE", 60, width // 2, hight // 4,        center=True, color=Colors["border"])
        draw_text("1) Start Game", 32, width // 2, hight // 2 - 30, center=True)
        draw_text("2) Scoreboard", 32, width // 2, hight // 2 + 10, center=True)
        draw_text("3) Exit",       32, width // 2, hight // 2 + 50, center=True)
        draw_text("Press 1, 2 or 3", 24, width // 2, hight - 60,   center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = select_difficulty()    # انتخاب سختی
                    run_game(difficulty)                # شروع بازی
                elif event.key == pygame.K_2:
                    show_scoreboard()                   # نمایش جدول امتیازات
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()                          # خروج از بازی


# ─────────────────────────────────────────────
# نقطه شروع برنامه
# ─────────────────────────────────────────────
if __name__ == "__main__":
    show_main_menu()