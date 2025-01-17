from aiogram.types import InlineKeyboardButton


button_keys = InlineKeyboardButton(
    text="🔑 Ключи",
    callback_data="button_keys_pressed"
)
button_instruction = InlineKeyboardButton(
    text="📄 Инструкция",
    callback_data="button_instruction_pressed"
)
button_payment = InlineKeyboardButton(
    text="💸 Оплата",
    callback_data="button_payment_pressed"
)
button_bonus = InlineKeyboardButton(
    text="🎁 Бонусы",
    callback_data="button_bonus_pressed"
)
button_back = InlineKeyboardButton(
    text="⬅️ Назад",
    callback_data="button_back_pressed"
)
button_ios = InlineKeyboardButton(
    text="iPhone/iPad",
    callback_data="button_ios_pressed"
)
button_android = InlineKeyboardButton(
    text="Android",
    callback_data="button_android_pressed"
)
button_mac = InlineKeyboardButton(
    text="MacOS",
    callback_data="button_mac_pressed"
)
button_windows = InlineKeyboardButton(
    text="Windows",
    callback_data="button_windows_pressed"
)
button_others = InlineKeyboardButton(
    text="Роутер/ТВ",
    callback_data="button_others_pressed"
)
button_devices_back = InlineKeyboardButton(
    text="⬅️ Назад",
    callback_data="button_devices_back_pressed"
)
button_admin_notification = InlineKeyboardButton(
    text="Оповещение",
    callback_data="button_admin_notification_pressed"
)
button_admin_add = InlineKeyboardButton(
    text="Добавить польз-ля",
    callback_data="button_admin_add_pressed"
)
button_admin_exit = InlineKeyboardButton(
    text="🚪 Выйти из админки",
    callback_data="button_admin_exit_pressed"
)
button_admin_skip = InlineKeyboardButton(
    text="▶️ Пропустить",
    callback_data="button_admin_skip_pressed"
)
button_admin_skip_all = InlineKeyboardButton(
    text="⏩ Пропустить всё",
    callback_data="button_admin_skip_all_pressed"
)
