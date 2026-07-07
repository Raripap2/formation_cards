from io import BytesIO

import qrcode
from PIL import Image, ImageDraw, ImageFont


def generate_qr(url: str) -> bytes:
    """Генерация Qr кода"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    byte_img = buffer.getvalue()
    return byte_img


def generate_tag(order: str, grade: str, plate_l: float, plate_w: float, plate_t: float, position: str,
                 url: str) -> BytesIO:
    """Генерация бирки бля печати
    ожидается Номер заказа; Марка стали; длина, ширина, толщина листа по карточке;
    место складирования; qr код в бинарном формате"""
    width, height = 365, 400
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    """font = ImageFont.truetype('arialmt.ttf', 30)"""
    text = [(f"{order}", 5),
            (f"{plate_l} {plate_w} {plate_t}", 35),
            (f"{grade} {position}", 65)]
    qr_photo = generate_qr(url)
    if qr_photo:
        qr_image = Image.open(BytesIO(qr_photo))
        # qr_image = qr_image.resize((100, 100))
        image.paste(qr_image, (0, 55))
    for row in text:
        draw.text((int(width * 0.1), row[1]), row[0], fill=(0, 0, 0), font=font)
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')
    image.save("image.png", "PNG")
    img_bytes.seek(0)
    return img_bytes

if __name__ == '__main__':
    generate_tag('1', '2', 1, 2,3, '1', '23')