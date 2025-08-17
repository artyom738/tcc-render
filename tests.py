import moviepy.editor as mp
# print(mp.TextClip.list('font'))
from model.repository.chart_repository import ChartRepository
# from previews.preview_factory import PreviewFactory

# if __name__ == '__main__':
	# chart = ChartRepository().get_chart_by_id(268)
	# PreviewFactory().create(chart)

	# chart = ChartRepository().get_chart_by_id(267)
	# PreviewFactory().create(chart)


# from PIL import Image, ImageDraw, ImageFilter
import math

WIDTH, HEIGHT = 1920, 1080
BASE_COLOR = (70, 130, 180)
COLOR_VARIATION = 30
ANGLE_DEG = 45
angle_rad = math.radians(ANGLE_DEG)

def clamp(x, minimum=0, maximum=255):
    return max(minimum, min(x, maximum))

def color_variation(base_color, variation, factor=0):
    return tuple(
        clamp(int(c + variation * (factor - 0.5) * 2))
        for c in base_color
    )

def draw_polygon_with_shadow(img, points, fill_color, shadow_offset=(8,8), shadow_radius=10):
    # Создаём слой для тени
    shadow_layer = Image.new('RGBA', img.size, (0,0,0,0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_color = (0, 0, 0, 120)  # полупрозрачная тень

    shifted_points = [(x + shadow_offset[0], y + shadow_offset[1]) for x, y in points]
    shadow_draw.polygon(shifted_points, fill=shadow_color)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_radius))

    # Накладываем тень на изображение через paste с маской
    img.paste(shadow_layer, (0,0), shadow_layer)

    # Рисуем саму фигуру
    draw = ImageDraw.Draw(img)
    draw.polygon(points, fill=fill_color)

def generate_wallpaper():
    bg_color = (240, 240, 245, 255)
    img = Image.new('RGBA', (WIDTH, HEIGHT), bg_color)

    cx, cy = WIDTH // 2, HEIGHT // 2
    offset = 150

    vx = math.cos(angle_rad)
    vy = math.sin(angle_rad)
    perp_angle_rad = angle_rad + math.pi / 2
    px = math.cos(perp_angle_rad)
    py = math.sin(perp_angle_rad)

    length = max(WIDTH, HEIGHT) * 2

    line1_start = (cx - vx * length, cy - vy * length)
    line1_end = (cx + vx * length, cy + vy * length)

    line2_start = (line1_start[0] + px * offset, line1_start[1] + py * offset)
    line2_end = (line1_end[0] + px * offset, line1_end[1] + py * offset)

    offset2 = offset * 2
    line3_start = (line1_start[0] + px * offset2, line1_start[1] + py * offset2)
    line3_end = (line1_end[0] + px * offset2, line1_end[1] + py * offset2)

    perp_len = length / 2

    p1 = line1_start
    p2 = (line1_start[0] + px * perp_len, line1_start[1] + py * perp_len)
    p3 = line2_start
    p4 = (line2_start[0] + px * perp_len, line2_start[1] + py * perp_len)
    quad1 = [p1, p2, p4, p3]

    p5 = line1_end
    p6 = (line1_end[0] + px * perp_len, line1_end[1] + py * perp_len)
    p7 = line2_end
    p8 = (line2_end[0] + px * perp_len, line2_end[1] + py * perp_len)
    quad2 = [p5, p6, p8, p7]

    p9 = line3_start
    p10 = (line3_start[0] + px * perp_len, line3_start[1] + py * perp_len)
    p11 = line2_start
    p12 = (line2_start[0] + px * perp_len, line2_start[1] + py * perp_len)
    quad3 = [p9, p10, p12, p11]

    quads = [quad1, quad2, quad3]

    for i, quad in enumerate(quads):
        factor = i / (len(quads) - 1) if len(quads) > 1 else 0
        fill = color_variation(BASE_COLOR, COLOR_VARIATION, factor)
        draw_polygon_with_shadow(img, quad, fill)

    img = img.convert("RGB")
    img.save('vector_geometry_line_composition_fixed.png')
    print("Обои сохранены как vector_geometry_line_composition_fixed.png")

if __name__ == '__main__':
    # generate_wallpaper()
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='tcc_render',
        port=3306
    )

    print(conn.open)
    conn.close()


