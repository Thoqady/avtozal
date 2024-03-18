import tkinter as tk
from tkinter import filedialog
import xlsxwriter
import qrcode


def create_excel_A6(entries):
    # Получаем тексты из полей ввода
    row, place, type_subsystem, mnemonic_ne, project, department, responsible, leader, shift_contact, shift_contact2, shift_contact3,opl_group, text_A2, text_A1 = [entry.get() for entry in entries]

    # Создаем объект QR-кода
    qr_data = f"Ряд {row} Место {place}\n" \
              f"Тип/подсистема - {type_subsystem}\n" \
              f"Мнемоника / NE - {mnemonic_ne}\n" \
              f"Проект - {project}\n" \
              f"Подразделение - {department}\n" \
              f"Отв.лицо - {responsible} тел. {leader}\n" \
              f"Руководитель - {shift_contact} тел. {shift_contact2}\n" \
              f"Контакт деж. Смены - {shift_contact3}\n" \
              f"Группа OPL - {opl_group}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Открываем диалоговое окно для выбора пути сохранения файла
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

    if save_path:
        # Создаем новый Excel-документ с xlsxwriter
        workbook = xlsxwriter.Workbook(save_path)
        worksheet = workbook.add_worksheet()
        worksheet.set_landscape()

        # Устанавливаем размеры ячеек внутри Excel
        col_width_mm = 31
        row_height_mm = 291.5

        # Устанавливаем высоту строки
        worksheet.set_default_row(row_height_mm)

        # Устанавливаем ширину столбцов
        worksheet.set_column('A:A', 39.33)
        worksheet.set_column('B:B', 34.33)

        # Устанавливаем высоту столбцов
        worksheet.set_row(0, 131.7)
        worksheet.set_row(1, 56.6)

        # Получаем объект format для настройки стилей ячеек
        cell_format_text = workbook.add_format({
            'font_size': 86,   # размер шрифта
            'align': 'center',  # выравнивание по центру
            'valign': 'vcenter',  # выравнивание по вертикали по центру
        })

        cell_format_text.set_bold()
        worksheet.merge_range('A2:B2', 'Merged Range', cell_format_text)

        cell_format_A2 = workbook.add_format({
            'font_size': 17.5,   # размер шрифта
            'valign': 'top',  # выравнивание по вертикали сверху
            'align': 'center',  # выравнивание по центру
        })

        # Вставляем текст из ячейки A1
        worksheet.write('A1', text_A2, cell_format_text)
        worksheet.write('A2', text_A1, cell_format_A2)

        # Переводим размеры QR-кода в пиксели (примерно 1 см = 37.795276 пикселя)
        qr_width_pixels = int(8 * 37.795276)
        qr_height_pixels = int(8 * 37.795276)

        # Сохраняем QR-код как изображение
        qr_img = qr_img.resize((qr_width_pixels, qr_height_pixels))
        qr_img.save('qr_code.png')

        # Вставляем изображение QR-кода в ячейку B1 посередине
        worksheet.insert_image('B1', 'qr_code.png', {'x_offset': 10, 'y_offset': 10, 'x_scale': 0.5, 'y_scale': 0.5})

        # Закрываем Excel-документ
        workbook.close()


# Создаем основное окно Tkinter
root = tk.Tk()
root.title("Создание Qr-code")

# Устанавливаем начальные размеры окна
root.geometry("400x550")

# Создаем Frame для размещения виджетов
frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

# Создаем метки и поля ввода для каждого поля
labels = ["Ряд - ", "Место - ", "Тип/подсистема - ", "Мнемоника / NE - ", "Проект - ",
          "Подразделение - ", "Отв.лицо - ", 'тел. ', "Руководитель - ", 'тел.',"Контакт деж. Смены - ", "Группа OPL - "]

entries = []

for i, label_text in enumerate(labels):
    entry_label = tk.Label(frame, text=label_text)
    entry_label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

    entry = tk.Entry(frame)
    entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry)

# Метка и поле ввода для текста в ячейку A1 и А2
entry_label_A1 = tk.Label(frame, text="Номер стойки - ")
entry_label_A1.grid(row=len(labels), column=0, sticky="e", padx=5, pady=5)

entry_A1 = tk.Entry(frame)
entry_A1.grid(row=len(labels), column=1, sticky="w", padx=5, pady=5)
entries.append(entry_A1)

entry_label_A2 = tk.Label(frame, text="Отв. - ")
entry_label_A2.grid(row=len(labels) + 1, column=0, sticky="e", padx=5, pady=5)

entry_A2 = tk.Entry(frame)
entry_A2.grid(row=len(labels) + 1, column=1, sticky="w", padx=5, pady=5)
entries.append(entry_A2)

# Создаем кнопку
button_A6 = tk.Button(frame, text="Формат 150 мм на 67 мм", command=lambda: create_excel_A6(entries))
button_A6.grid(row=len(labels) + 3, column=0, columnspan=2, pady=20)
button_A6.place(relx=0.32, rely=0.8)

# Запускаем главный цикл Tkinter
root.mainloop()
