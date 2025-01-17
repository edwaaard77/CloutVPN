from aiogram.types import InlineKeyboardMarkup

from keyboards.buttons import (button_keys, button_instruction, button_payment, button_back, button_ios,
                               button_mac, button_android, button_windows, button_devices_back,
                               button_bonus, button_admin_exit, button_others, button_admin_add,
                               button_admin_notification, button_admin_skip, button_admin_skip_all)


keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[[button_keys], [button_instruction], [button_payment], [button_bonus]]
)

keyboard_back = InlineKeyboardMarkup(
    inline_keyboard=[[button_back]]
)

keyboard_devices_1st_row = [button_ios, button_android]
keyboard_devices_2nd_row = [button_mac, button_windows]
keyboard_devices = InlineKeyboardMarkup(
    inline_keyboard=[keyboard_devices_1st_row,
                     keyboard_devices_2nd_row,
                     [button_others],
                     [button_back]]
)

keyboard_devices_back = InlineKeyboardMarkup(
    inline_keyboard=[[button_devices_back]]
)

keyboard_admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[[button_admin_add],
                     [button_admin_notification],
                     [button_admin_exit]]
)

keyboard_admin_exit = InlineKeyboardMarkup(
    inline_keyboard=[[button_admin_exit]]
)

keyboard_admin_skip = InlineKeyboardMarkup(
    inline_keyboard=[[button_admin_skip],
                     [button_admin_skip_all]]
)
