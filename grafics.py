# renderer.py  –  موتور رندر پیشرفته بازی مار
# گرید محو، دیوار آجری، مار با گرادیان، غذای چرخان، پاورآپ‌های درخشان

import pygame
import math
from settings import cell_size, grid_size, width, hight, Colors

# ──────────────────────────────────────────────
#  ثابت‌های رندر
# ──────────────────────────────────────────────
WALL_THICKNESS = cell_size          # ضخامت دیوار آجری (یک سلول)
PLAY_OFFSET    = WALL_THICKNESS     # محل شروع ناحیه بازی

# رنگ‌های آجر
BRICK_DARK   = (80,  45,  20)
BRICK_LIGHT  = (140, 75,  35)
BRICK_MORTAR = (55,  35,  15)

# رنگ‌های گرادیان مار
SNAKE_HEAD_COLOR = (0, 230, 80)
SNAKE_BODY_COLOR = (0, 160, 50)
SNAKE_TAIL_COLOR = (0, 100, 30)

# رنگ‌های چشم مار
EYE_WHITE = (240, 240, 240)
EYE_PUPIL = (20,  20,  20)

# رنگ غذا
FOOD_COLOR_OUTER = (255, 60,  60)
FOOD_COLOR_INNER = (255, 180, 100)
FOOD_SHINE       = (255, 240, 200)

# ──────────────────────────────────────────────
#  کلاس اصلی رندر
# ──────────────────────────────────────────────
class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.tick   = 0            # برای انیمیشن‌های زمان‌بندی‌شده

        # Surface کش‌شده برای دیوار و گرید (فقط یک‌بار ساخته می‌شه)
        self._wall_surf  = self._build_wall_surface()
        self._grid_surf  = self._build_grid_surface()

    # ══════════════════════════════════════════
    #  ساخت Surface‌های ثابت
    # ══════════════════════════════════════════

    def _build_grid_surface(self) -> pygame.Surface:
        """گرید محو فقط روی ناحیه بازی (درون دیوارها)"""
        from settings import PLAY_MIN, PLAY_MAX
        surf = pygame.Surface((width, hight), pygame.SRCALPHA)
        grid_color = (255, 255, 255, 12)

        play_start_px = PLAY_MIN * cell_size
        play_end_px   = PLAY_MAX * cell_size
        play_size     = PLAY_MAX - PLAY_MIN

        for col in range(play_size + 1):
            x = play_start_px + col * cell_size
            pygame.draw.line(surf, grid_color,
                             (x, play_start_px), (x, play_end_px))

        for row in range(play_size + 1):
            y = play_start_px + row * cell_size
            pygame.draw.line(surf, grid_color,
                             (play_start_px, y), (play_end_px, y))

        return surf

    def _build_wall_surface(self) -> pygame.Surface:
        """دیوار آجری دور صفحه"""
        surf = pygame.Surface((width, hight), pygame.SRCALPHA)
        t = WALL_THICKNESS
        w, h = width, hight

        # چهار نوار کنار صفحه
        rects = [
            pygame.Rect(0,     0,     w,  t),   # بالا
            pygame.Rect(0,     h-t,   w,  t),   # پایین
            pygame.Rect(0,     0,     t,  h),   # چپ
            pygame.Rect(w-t,   0,     t,  h),   # راست
        ]
        for r in rects:
            pygame.draw.rect(surf, BRICK_MORTAR, r)

        # رسم آجرها روی نوارها
        brick_w = cell_size * 2
        brick_h = cell_size
        for band in rects:
            bx, by, bw, bh = band
            # سطرها
            rows_n = max(1, bh // brick_h)
            cols_n = max(1, bw // brick_w) + 2
            for row in range(rows_n):
                offset = (brick_w // 2) if row % 2 else 0
                for col in range(-1, cols_n + 1):
                    rx = bx + col * brick_w - offset
                    ry = by + row * brick_h
                    br = pygame.Rect(rx + 1, ry + 1, brick_w - 2, brick_h - 2)
                    # کلیپ درون نوار
                    br = br.clip(band)
                    if br.width > 4 and br.height > 4:
                        # بدنه آجر
                        pygame.draw.rect(surf, BRICK_LIGHT, br)
                        # سایه پایین/راست برای حجم
                        shadow = pygame.Rect(br.x, br.bottom - 3, br.width, 3)
                        shadow_r = pygame.Rect(br.right - 3, br.y, 3, br.height)
                        pygame.draw.rect(surf, BRICK_DARK, shadow)
                        pygame.draw.rect(surf, BRICK_DARK, shadow_r)
                        # های‌لایت بالا/چپ
                        highlight_color = (180, 110, 55)
                        pygame.draw.line(surf, highlight_color, br.topleft, br.topright)
                        pygame.draw.line(surf, highlight_color, br.topleft, br.bottomleft)

        # خط درخشان داخلی روی لبه دیوار
        glow_color = (200, 130, 60, 120)
        glow_surf  = pygame.Surface((w, h), pygame.SRCALPHA)
        inner = pygame.Rect(t, t, w - 2*t, h - 2*t)
        pygame.draw.rect(glow_surf, glow_color, inner, 3)
        surf.blit(glow_surf, (0, 0))

        return surf

    # ══════════════════════════════════════════
    #  رندر هر فریم
    # ══════════════════════════════════════════

    def begin_frame(self):
        """پاک کردن صفحه + گرید + دیوار"""
        self.tick += 1
        self.screen.fill(Colors["background"])
        self.screen.blit(self._grid_surf, (0, 0))
        self.screen.blit(self._wall_surf, (0, 0))

    # ──────────────────────────────────────────
    #  تبدیل مختصات سلول → پیکسل
    #  سلول 0 = دیوار چپ/بالا، سلول 1 = اولین سلول بازی
    #  پس gx * cell_size مستقیماً پیکسل درستیه
    # ──────────────────────────────────────────
    def _cell_px(self, gx: int, gy: int):
        return (gx * cell_size, gy * cell_size)

    # ══════════════════════════════════════════
    #  رسم مار پیشرفته
    # ══════════════════════════════════════════

    def draw_snake(self, snake):
        body = snake.body
        n    = len(body)
        if n == 0:
            return

        # انتخاب پالت رنگ بر اساس وضعیت
        if snake.invincible:
            hue_shift = self.tick * 4
            head_c = self._hue_color(hue_shift)
            body_c = self._hue_color(hue_shift + 60)
            tail_c = self._hue_color(hue_shift + 120)
        elif snake.speed_boost:
            head_c = (255, 120, 0)
            body_c = (220, 80,  0)
            tail_c = (160, 50,  0)
        else:
            head_c = SNAKE_HEAD_COLOR
            body_c = SNAKE_BODY_COLOR
            tail_c = SNAKE_TAIL_COLOR

        # ── رسم بدن (از دم به سر، سر آخر رسم بشه) ──
        for i in range(n - 1, -1, -1):
            gx, gy = body[i]
            px, py = self._cell_px(gx, gy)
            t      = i / max(n - 1, 1)   # 0=سر، 1=دم
            color  = self._lerp_color(head_c, tail_c, t)

            margin = 2
            rect   = pygame.Rect(px + margin, py + margin,
                                 cell_size - margin*2, cell_size - margin*2)

            # بدنه گرد
            pygame.draw.rect(self.screen, color, rect, border_radius=6)

            # های‌لایت بالا (برق)
            shine_rect = pygame.Rect(rect.x + 2, rect.y + 2,
                                     rect.width - 4, rect.height // 3)
            shine_color = self._lighten(color, 60)
            shine_surf  = pygame.Surface(shine_rect.size, pygame.SRCALPHA)
            shine_surf.fill((*shine_color, 80))
            self.screen.blit(shine_surf, shine_rect)

        # ── چشم‌ها روی سر ──
        self._draw_eyes(snake)

    def _draw_eyes(self, snake):
        if not snake.body:
            return
        gx, gy = snake.body[0]
        px, py = self._cell_px(gx, gy)
        dx, dy = snake.dir

        cx = px + cell_size // 2
        cy = py + cell_size // 2
        eye_r    = max(2, cell_size // 6)
        pupil_r  = max(1, eye_r - 1)

        # موقعیت دو چشم عمود بر جهت حرکت
        if dx != 0:   # حرکت افقی → چشم‌ها بالا/پایین
            e1 = (cx + dx * cell_size // 4, cy - cell_size // 4)
            e2 = (cx + dx * cell_size // 4, cy + cell_size // 4)
        else:          # حرکت عمودی → چشم‌ها چپ/راست
            e1 = (cx - cell_size // 4, cy + dy * cell_size // 4)
            e2 = (cx + cell_size // 4, cy + dy * cell_size // 4)

        for ex, ey in (e1, e2):
            pygame.draw.circle(self.screen, EYE_WHITE,  (ex, ey), eye_r)
            pygame.draw.circle(self.screen, EYE_PUPIL,  (ex + dx, ey + dy), pupil_r)

    # ══════════════════════════════════════════
    #  رسم غذا پیشرفته (سیب شبیه‌سازی‌شده)
    # ══════════════════════════════════════════

    def draw_food(self, food):
        gx, gy = food.position
        px, py = self._cell_px(gx,gy)
        cx = px + cell_size // 2
        cy = py + cell_size // 2
        r  = cell_size // 2 - 2

        # ضربان (pulse) با sin
        pulse = math.sin(self.tick * 0.12) * 1.5
        r_anim = int(r + pulse)

        # سایه
        shadow_surf = pygame.Surface((cell_size * 2, cell_size * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60),
                            (cell_size//2 - r_anim, cell_size//2 + r_anim - 4,
                             r_anim * 2, r_anim // 2))
        self.screen.blit(shadow_surf, (cx - cell_size, cy - cell_size))

        # بدنه قرمز
        pygame.draw.circle(self.screen, FOOD_COLOR_OUTER, (cx, cy), r_anim)

        # گرادیان داخلی روشن‌تر (دایره کوچکتر)
        inner_r = r_anim * 2 // 3
        pygame.draw.circle(self.screen, FOOD_COLOR_INNER,
                           (cx - r_anim//5, cy - r_anim//5), inner_r)

        # های‌لایت سفید (برق)
        shine_surf = pygame.Surface((r_anim*2, r_anim*2), pygame.SRCALPHA)
        pygame.draw.ellipse(shine_surf, (*FOOD_SHINE, 160),
                            (r_anim//4, r_anim//8, r_anim//2, r_anim//3))
        self.screen.blit(shine_surf,
                         (cx - r_anim//2, cy - r_anim * 3//4))

        # ساقه
        stem_x = cx
        stem_top = cy - r_anim - 4
        pygame.draw.line(self.screen, (80, 160, 40),
                         (stem_x, cy - r_anim + 1),
                         (stem_x + 2, stem_top), 2)
        # برگ کوچک
        leaf = [
            (stem_x + 2, stem_top),
            (stem_x + 8, stem_top - 3),
            (stem_x + 5, stem_top + 2),
        ]
        pygame.draw.polygon(self.screen, (60, 180, 40), leaf)

    # ══════════════════════════════════════════
    #  رسم موانع (سنگ سه‌بعدی)
    # ══════════════════════════════════════════

    def draw_obstacles(self, obstacle):
        for gx, gy in obstacle.position:
            px, py = self._cell_px(gx, gy)
            rect = pygame.Rect(px + 1, py + 1, cell_size - 2, cell_size - 2)

            # بدنه سنگ
            pygame.draw.rect(self.screen, (120, 80, 45), rect, border_radius=3)

            # بافت: دو خط مورب کم‌رنگ
            dark = (80, 50, 25)
            light = (160, 110, 65)
            pygame.draw.line(self.screen, dark,
                             (rect.x + 3, rect.y + rect.height // 2),
                             (rect.x + rect.width - 3, rect.y + rect.height // 2))
            pygame.draw.line(self.screen, dark,
                             (rect.x + rect.width // 2, rect.y + 3),
                             (rect.x + rect.width // 2, rect.y + rect.height - 3))

            # های‌لایت بالا-چپ
            pygame.draw.line(self.screen, light, rect.topleft,
                             (rect.right, rect.top), 2)
            pygame.draw.line(self.screen, light, rect.topleft,
                             (rect.left, rect.bottom), 2)

            # سایه پایین-راست
            pygame.draw.line(self.screen, dark,
                             (rect.left, rect.bottom),
                             rect.bottomright, 2)
            pygame.draw.line(self.screen, dark,
                             rect.bottomright,
                             (rect.right, rect.top), 2)

    # ══════════════════════════════════════════
    #  رسم پاورباکس (درخشان و چرخان)
    # ══════════════════════════════════════════

    def draw_power_box(self, power_box, visible: bool):
        if not visible:
            return
        gx, gy = power_box.position
        px, py = self._cell_px(gx, gy)
        cx = px + cell_size // 2
        cy = py + cell_size // 2
        r  = cell_size // 2 - 3

        # چرخش ستاره با زمان
        angle = self.tick * 3   # درجه در هر فریم

        # هاله درخشان (glow)
        glow_r = r + 5 + int(math.sin(self.tick * 0.15) * 3)
        glow_surf = pygame.Surface((glow_r*4, glow_r*4), pygame.SRCALPHA)
        for layer in range(4):
            alpha = 40 - layer * 9
            lr    = glow_r - layer * 2
            if lr > 0 and alpha > 0:
                pygame.draw.circle(glow_surf, (0, 120, 255, alpha),(glow_r*2, glow_r*2), lr)
        self.screen.blit(glow_surf, (cx - glow_r*2, cy - glow_r*2))

        # ستاره ۸ پر
        self._draw_star(cx, cy, r, 8, angle, (0, 160, 255), (0, 80, 180))

        # علامت ⚡ یا P در وسط
        font = pygame.font.SysFont("Arial", cell_size - 6, bold=True)
        txt  = font.render("P", True, (255, 255, 255))
        trect = txt.get_rect(center=(cx, cy))
        self.screen.blit(txt, trect)

    # ══════════════════════════════════════════
    #  ابزارهای کمکی
    # ══════════════════════════════════════════

    def _draw_star(self, cx, cy, r_outer, points, angle_deg,
                   color_outer, color_inner):
        r_inner = r_outer * 0.45
        verts = []
        for i in range(points * 2):
            a = math.radians(angle_deg + i * 180 / points)
            ri = r_outer if i % 2 == 0 else r_inner
            verts.append((cx + ri * math.cos(a), cy + ri * math.sin(a)))
        if len(verts) >= 3:
            pygame.draw.polygon(self.screen, color_outer, verts)
            # هسته روشن‌تر
            inner_verts = []
            for i in range(points * 2):
                a = math.radians(angle_deg + i * 180 / points)
                ri = (r_outer * 0.3) if i % 2 == 0 else (r_inner * 0.3)
                inner_verts.append((cx + ri * math.cos(a), cy + ri * math.sin(a)))
            pygame.draw.polygon(self.screen, color_inner, inner_verts)

    @staticmethod
    def _lerp_color(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    @staticmethod
    def _lighten(color, amount):
        return tuple(min(255, c + amount) for c in color)

    @staticmethod
    def _hue_color(hue_deg: int):
        """تبدیل ساده hue به RGB (اشباع=100%, روشنایی=60%)"""
        h = hue_deg % 360
        s, v = 1.0, 0.9
        hi = h // 60
        f  = (h % 60) / 60
        p  = int(v * (1 - s) * 255)
        q  = int(v * (1 - s * f) * 255)
        t  = int(v * (1 - s * (1 - f)) * 255)
        vi = int(v * 255)
        table = [
            (vi, t,  p),
            (q,  vi, p),
            (p,  vi, t),
            (p,  q,  vi),
            (t,  p,  vi),
            (vi, p,  q),
        ]
        return table[hi % 6]