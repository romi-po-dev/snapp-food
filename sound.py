import pygame
import os 


if not pygame.mixer.get_init():
    pygame.mixer.init()

# ─────────────────────────────────────────────
# متغیر کلی وضعیت صدا
# ─────────────────────────────────────────────
SOUND_ENABLED = True

# ═══════════════════════════════════════════════
# تولید صدای 
# ═══════════════════════════════════════════════


try:
    EAT_SOUND = pygame.mixer.Sound("snake_project/apple-eating-36127.mp3")
    POWER_SOUND = pygame.mixer.Sound("snake_project/power-5.mp3")
    GAME_OVER_SOUND = pygame.mixer.Sound("snake_project/Game-Over-Sound-Effect-3.mp3")

    # تنظیم ولوم 
    EAT_SOUND.set_volume(1.0)
    POWER_SOUND.set_volume(0.7)
    GAME_OVER_SOUND.set_volume(0.9)

except pygame.error as e:
    print(f"Error loading sounds: {e}")
    # اگر فایلی پیدا نشد، یک آبجکت خالی می‌سازیم تا بازی کرش نکند
    EAT_SOUND = POWER_SOUND = GAME_OVER_SOUND = type('obj', (object,), {'play': lambda: None})

# ═══════════════════════════════════════════════
# توابع کنترل وضعیت صدا
# ═══════════════════════════════════════════════

def toggle_sound():
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    return SOUND_ENABLED

def is_sound_enabled():
    return SOUND_ENABLED

# ═══════════════════════════════════════════════
# توابع پخش صداهای بازی
# ═══════════════════════════════════════════════

def play_eat_sound():
    if SOUND_ENABLED:
        EAT_SOUND.play()

def play_power_sound():
    if SOUND_ENABLED:
        POWER_SOUND.play()

def play_game_over_sound():
    if SOUND_ENABLED:
        GAME_OVER_SOUND.play()

