from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib import TTFont

def extract_font_style(input_font_path, weight, width, output_font_path):
    # Загрузка шрифта
    font = TTFont(input_font_path)

    # Удаление таблиц 'hhea' и 'VVAR' (необязательно)
    font['head'].flags &= ~0x0002  # Устанавливаем флаг не воспринимать таблицу 'hhea'
    if 'VVAR' in font:
        del font['VVAR']

    # Определение осей
    axes = {'wght': weight, 'wdth': width}

    # Инстанцирование переменного шрифта
    inst_font = instantiateVariableFont(font, axes)
    change_font_name(inst_font, "Bahn TCC", "SemiCondensed")

    # Сохранение измененного шрифта
    inst_font.save(output_font_path)

    print(f"Шрифт успешно сохранен с весом {weight} и шириной {width}. Сохранено в {output_font_path}")


def change_font_name(font, new_family_name, new_style_name):
    name_table = font.get("name")

    for record in name_table.names:
        if record.nameID == 1:  # Family Name
            record.string = new_family_name.encode('utf-16be')
        elif record.nameID == 2:  # Subfamily Name (Style Name)
            record.string = new_style_name.encode('utf-16be')


input_font_path = "D:\\Artyom\\Проекты\\Python\\tcc-render\\test_results\\bahnschrift_0.ttf"
output_font_path = "D:\\Artyom\\Проекты\\Python\\tcc-render\\test_results\\1.ttf"
weight = 600
width = 0.85
extract_font_style(input_font_path, weight, width, output_font_path)