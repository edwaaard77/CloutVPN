import asyncio
import logging
from aiogram import Bot, types, F
from aiogram import Dispatcher
from aiogram.enums import ParseMode, ChatAction
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.states import States
from db.models import async_session
from db.models import User
from db.models import async_main
from sqlalchemy import select, or_
from keyboards.keyboards import (keyboard_main, keyboard_back, keyboard_devices, keyboard_devices_back)
from files.files import nekobox_android, nekobox_windows
from admin_handler import router as admin_router
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_routers(admin_router)


@dp.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))
        if not user:
            await message.answer(text=f"Здравствуйте! 👋\n\nКажется, вы ещё не авторизовались, "
                                      f"либо не подключили подписку CloutVPN...\n\n"
                                      f"Для авторизации пришлите один из имеющихся у вас ключей 🔑\n\n"
                                      f"Для приобретения подписки или при возникновении вопросов "
                                      f"обращайтесь к @clout_vpn ✍️")
            await state.set_state(States.log_in)
        else:
            await message.answer(text=f"Здравствуйте! 👋\n\nТеперь CloutVPN всегда под рукой 🫂",
                                 reply_markup=keyboard_main)


@dp.message(F.text, States.log_in)
async def logging_in(message: types.Message, state: FSMContext):
    key = message.text
    tg_id = message.from_user.id
    async with async_session() as session:
        user = await session.scalar(select(User).where(
            or_(
                User.nlSS_acc1 == key,
                User.nlTrojan_acc1 == key,
                User.finSS_acc1 == key,
                User.finTrojan_acc1 == key,
                User.nlSS_acc2 == key,
                User.nlTrojan_acc2 == key,
                User.finSS_acc2 == key,
                User.finTrojan_acc2 == key,
                User.nlSS_acc3 == key,
                User.nlTrojan_acc3 == key,
                User.finSS_acc3 == key,
                User.finTrojan_acc3 == key
            )
        ))
        if not user:
            await message.answer(text=f"Похоже вы до сих пор не приобрели подписку, либо я вас ещё не успел добавить в "
                                      f"систему...🧐\n\n"
                                      f"Обратитесь за помощью к @clout_vpn ✍️")
        else:
            user.tg_id = tg_id
            await session.commit()
            await message.answer(text=f"Вы успешно авторизовались ✅\n\nТеперь CloutVPN всегда под рукой 🫂",
                                 reply_markup=keyboard_main)
    await state.clear()


@dp.callback_query(F.data == "button_keys_pressed")
async def process_button_keys_press(callback: CallbackQuery):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == callback.from_user.id))
        if not user.nlSS_acc3:
            if not user.nlSS_acc2:
                await callback.message.edit_text(
                    text=f"<b>Ваши ключи:</b>\n\n"
                         f"🇳🇱 Нидерланды (Shadowsocks)\n\n🔑 <code>{user.nlSS_acc1}</code>\n\n"
                         f"🇳🇱 Нидерланды (Trojan)\n\n🔑 <code>{user.nlTrojan_acc1}</code>\n\n"
                         f"🇫🇮 Финляндия (Shadowsocks)\n\n🔑 <code>{user.finSS_acc1}</code>\n\n"
                         f"🇫🇮 Финляндия (Trojan)\n\n🔑 <code>{user.finTrojan_acc1}</code>\n\n"
                         f"* чтобы скопировать, просто нажмите на конкретный ключ.",
                    reply_markup=keyboard_back
                )
            else:
                await callback.message.edit_text(
                    text=f"<b>1-й аккаунт:</b>\n\n"
                         f"🇳🇱 Нидерланды (Shadowsocks)\n\n🔑 <code>{user.nlSS_acc1}</code>\n\n"
                         f"🇳🇱 Нидерланды (Trojan)\n\n🔑 <code>{user.nlTrojan_acc1}</code>\n\n"
                         f"🇫🇮 Финляндия (Shadowsocks)\n\n🔑 <code>{user.finSS_acc1}</code>\n\n"
                         f"🇫🇮 Финляндия (Trojan)\n\n🔑 <code>{user.finTrojan_acc1}</code>\n\n"
                         f"<b>2-й аккаунт:</b>\n\n"
                         f"🇳🇱 Нидерланды (Shadowsocks)\n\n🔑 <code>{user.nlSS_acc2}</code>\n\n"
                         f"🇳🇱 Нидерланды (Trojan)\n\n🔑 <code>{user.nlTrojan_acc2}</code>\n\n"
                         f"🇫🇮 Финляндия (Shadowsocks)\n\n🔑 <code>{user.finSS_acc2}</code>\n\n"
                         f"🇫🇮 Финляндия (Trojan)\n\n🔑 <code>{user.finTrojan_acc2}</code>\n\n"
                         f"* чтобы скопировать, просто нажмите на конкретный ключ.",
                    reply_markup=keyboard_back
                )
        else:
            await callback.message.edit_text(
                text=f"<b>1-й аккаунт:</b>\n\n"
                     f"🇳🇱 Нидерланды (Shadowsocks)\n\n🔑 <code>{user.nlSS_acc1}</code>\n\n"
                     f"🇳🇱 Нидерланды (Trojan)\n\n🔑 <code>{user.nlTrojan_acc1}</code>\n\n"
                     f"🇫🇮 Финляндия (Shadowsocks)\n\n🔑 <code>{user.finSS_acc1}</code>\n\n"
                     f"🇫🇮 Финляндия (Trojan)\n\n🔑 <code>{user.finTrojan_acc1}</code>\n\n"
                     f"<b>2-й аккаунт:</b>\n\n"
                     f"🇳🇱 Нидерланды (Shadowsocks)\n\n🔑 <code>{user.nlSS_acc2}</code>\n\n"
                     f"🇳🇱 Нидерланды (Trojan)\n\n🔑 <code>{user.nlTrojan_acc2}</code>\n\n"
                     f"🇫🇮 Финляндия (Shadowsocks)\n\n🔑 <code>{user.finSS_acc2}</code>\n\n"
                     f"🇫🇮 Финляндия (Trojan)\n\n🔑 <code>{user.finTrojan_acc2}</code>\n\n"
                     f"<b>3-й аккаунт:</b>\n\n"
                     f"🇳🇱 Нидерланды (Shadowsocks)\n\n🔑 <code>{user.nlSS_acc3}</code>\n\n"
                     f"🇳🇱 Нидерланды (Trojan)\n\n🔑 <code>{user.nlTrojan_acc3}</code>\n\n"
                     f"🇫🇮 Финляндия (Shadowsocks)\n\n🔑 <code>{user.finSS_acc3}</code>\n\n"
                     f"🇫🇮 Финляндия (Trojan)\n\n🔑 <code>{user.finTrojan_acc3}</code>\n\n"
                     f"* чтобы скопировать, просто нажмите на конкретный ключ.",
                reply_markup=keyboard_back
            )
        await callback.answer()


@dp.callback_query(F.data == "button_back_pressed")
async def process_button_back_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"<b>Главное меню</b>",
        reply_markup=keyboard_main
    )
    await callback.answer()


@dp.callback_query(F.data == "button_instruction_pressed")
async def process_button_instruction_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"<b>Выберете устройство:</b>",
        reply_markup=keyboard_devices
    )
    await callback.answer()


@dp.callback_query(F.data == "button_bonus_pressed")
async def process_button_bonus_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"На постоянной основе действует реферальная программа 🤝\n\n"
             f"Порекомендуйте своим близким мой сервис — они получат 7 дней бесплатного пробного периода, а вам добавлю "
             f"1 месяц к действующей подписке за каждого нового пользователя, кто её приобретёт 🎁",
        reply_markup=keyboard_back
    )
    await callback.answer()


@dp.callback_query(F.data == "button_devices_back_pressed")
async def process_button_devices_back_press(callback: CallbackQuery):
    await callback.message.delete()


@dp.callback_query(F.data == "button_android_pressed")
async def process_button_android_press(callback: CallbackQuery):
    await callback.message.bot.send_chat_action(
        chat_id=callback.message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    await callback.message.answer_document(
        document=nekobox_android,
        caption=f"<b>Инструкция для Android</b>\n\n"
                f"1. Скачайте и установите приложение, файл которого прикреплён к сообщению\n\n"
                f"2. Скопируйте свой ключ\n\n"
                f"3. Зайдите в приложение NekoBox —> справа в верхнем углу найдите и нажмите на ➕ —> "
                f"\"Импорт из буфера обмена\"\n\n"
                f"4. Проделайте то же самое с каждым ключом\n\n"
                f"Выберете нужный профиль и нажмите на иконку бумажного самолётика — всё готово! ✅",
        reply_markup=keyboard_devices_back
    )
    await callback.answer()


@dp.callback_query(F.data == "button_ios_pressed")
async def process_button_ios_press(callback: CallbackQuery):
    await callback.message.answer(
        text=f"<b>Инструкция для iPhone/iPad</b>\n\n"
             f"1. Установить приложение на мобильное устройство:\n\n"
             f"https://apps.apple.com/app/id6450534064\n\n"
             f"2. Скопируйте свой ключ\n\n"
             f"3. Зайдите в приложение Streisand —> справа в верхнем углу найдите и нажмите на ➕ —> \"Добавить из буфера\"\n\n"
             f"4. Проделайте то же самое с каждым ключом\n\n"
             f"Выберете нужный профиль и нажмите на кнопку включения — всё готово! ✅",
        reply_markup=keyboard_devices_back
    )
    await callback.answer()


@dp.callback_query(F.data == "button_mac_pressed")
async def process_button_macos_press(callback: CallbackQuery):
    await callback.message.answer(
        text=f"<b>Инструкция для MacOS</b>\n\n"
             f"1. Установить приложение на компьютер:\n\n"
             f"https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690\n\n"
             f"2. Скопируйте свой ключ\n\n"
             f"3. Откройте приложение V2Box —> зайдите в раздел \"Config\" —> нажмите на ➕ в правом верхнем углу —> "
             f"\"Import v2ray uri from clipboard\" — у вас должен появиться профиль VPN\n\n"
             f"4. Проделайте то же самое с каждым ключом\n\n"
             f"Вернитесь во вкладку \"Home\" и нажмите на \"Tap to connect\" — всё готово! ✅",
        reply_markup=keyboard_devices_back
    )
    await callback.answer()


@dp.callback_query(F.data == "button_windows_pressed")
async def process_button_windows_press(callback: CallbackQuery):
    await callback.message.bot.send_chat_action(
        chat_id=callback.message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    await callback.message.answer_document(
        document=nekobox_windows,
        caption=f"<b>Инструкция для Windows</b>\n\n"
                f"1. Установить приложение на компьютер, файл которого прикреплён к сообщению\n\n"
                f"2. Скопируйте свой ключ\n\n"
                f"3. Распакуйте скачанный архив —> откройте файл nekoray.exe —> выберете \"sing-box\"\n\n"
                f"4. Найдите в левом верхнем углу и нажмите на \"Программа\" —> \"Добавить профиль из буфера обмена\"\n\n"
                f"5. Проделайте то же самое с каждым ключом\n\n"
                f"Вверху найдите и поставьте галочку напротив \"Режим TUN\" —> нажмите правой кнопкой мыши на нужный "
                f"профиль VPN —> нажмите на \"Запустить\" — всё готово! ✅",
        reply_markup=keyboard_devices_back
    )
    await callback.answer()


@dp.callback_query(F.data == "button_others_pressed")
async def process_button_windows_press(callback: CallbackQuery):
    await callback.message.answer(
        text=f"Для настройки VPN на роутере или телевизоре, напишите, пожалуйста, @clout_vpn ✍️",
        reply_markup=keyboard_devices_back
    )
    await callback.answer()



@dp.callback_query(F.data == "button_payment_pressed")
async def process_button_payment_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"<b>Тарифные планы:</b>\n\n"
             f"1 месяц — 99 рублей\n"
             f"3 месяца — 249 рублей\n"
             f"6 месяцев — 479 рублей\n"
             f"1 год — 899 рублей\n\n"
             f"<b>Способы оплаты:</b>\n\n"
             f"Cбер\n<code>2202205040148691</code>\n\n"
             f"Т-Банк\n<code>2200700167905438</code>\n\n"
             f"USDT(TRC20)\n<code>TU6oWvceMDsUVqMVQ4M91MajEvtXDurmnT</code>",
        reply_markup=keyboard_back
    )


async def main():
    await async_main()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
