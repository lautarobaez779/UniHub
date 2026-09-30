"""
Generador de iconos para PWA y Apple Touch Icon de UniHub
"""
import os
from PIL import Image, ImageDraw

def create_icon(size: int, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Crear imagen RGBA
    img = Image.new("RGBA", (size, size), (11, 15, 25, 255))
    draw = ImageDraw.Draw(img)

    # Dibujar fondo con esquinas redondeadas
    padding = int(size * 0.08)
    radius = int(size * 0.22)
    rect = [padding, padding, size - padding, size - padding]
    
    # Gradiente sutil simulado / color de marca índigo vibrante
    draw.rounded_rectangle(rect, radius=radius, fill=(99, 102, 241, 255))
    
    # Capa interior para efecto de profundidad
    inner_padding = padding + int(size * 0.03)
    inner_radius = radius - int(size * 0.02)
    inner_rect = [inner_padding, inner_padding, size - inner_padding, size - inner_padding]
    draw.rounded_rectangle(inner_rect, radius=inner_radius, fill=(79, 70, 229, 255))

    # Dibujar birrete de graduación geométrico en el centro
    center_x = size // 2
    center_y = int(size * 0.48)
    w = int(size * 0.28)
    h = int(size * 0.12)

    # Rombo superior del birrete (Cap)
    points = [
        (center_x, center_y - h),          # Arriba
        (center_x + w, center_y),          # Derecha
        (center_x, center_y + h),          # Abajo
        (center_x - w, center_y)           # Izquierda
    ]
    draw.polygon(points, fill=(255, 255, 255, 255))

    # Base del birrete
    base_w = int(w * 0.55)
    base_h = int(h * 0.9)
    base_top = center_y + int(h * 0.3)
    base_points = [
        (center_x - base_w, base_top),
        (center_x + base_w, base_top),
        (center_x + base_w, base_top + base_h),
        (center_x, base_top + base_h + int(base_h * 0.4)),
        (center_x - base_w, base_top + base_h)
    ]
    draw.polygon(base_points, fill=(224, 231, 255, 255))

    # Borla / Tassel
    tassel_x = center_x + int(w * 0.8)
    tassel_y = center_y + int(h * 1.3)
    draw.line([(center_x, center_y), (tassel_x, tassel_y - int(h * 0.4))], fill=(251, 191, 36, 255), width=max(2, int(size * 0.025)))
    draw.ellipse([tassel_x - int(size * 0.03), tassel_y - int(size * 0.03), tassel_x + int(size * 0.03), tassel_y + int(size * 0.03)], fill=(251, 191, 36, 255))

    img.save(output_path, "PNG")
    print(f"Icono generado: {output_path} ({size}x{size})")

if __name__ == "__main__":
    create_icon(180, "app/static/icons/apple-touch-icon.png")
    create_icon(192, "app/static/icons/icon-192.png")
    create_icon(512, "app/static/icons/icon-512.png")
