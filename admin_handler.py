from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
import os

from states.states import States
from keyboards.keyboards import keyboard_admin_panel, keyboard_main, keyboard_admin_exit, keyboard_admin_skip
from db.models import async_session
from db.models import User

from sqlalchemy import select

load_dotenv()

router = Router(name=__name__)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@router.message(F.text == ADMIN_PASSWORD)
async def secret_admin_message(message: types.Message):
    await message.answer(
        text="Привет, отец! Что делаем?",
        reply_markup=keyboard_admin_panel
    )


@router.callback_query(F.data == "button_admin_notification_pressed")
async def notification_sender(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.admin_notification)
    await callback.message.edit_text("Что желаете отправить?")


@router.message(States.admin_notification)
async def notification_sender(message: types.Message):
    # await message.send_copy(chat_id=290560857)
    async with async_session() as session:
        async with session.begin():
            # Получаем все tg_id из таблицы users
            result = await session.execute(select(User.tg_id))
            user_ids = result.scalars().all()

            # Отправляем сообщение каждому пользователю
            for tg_id in user_ids:
                try:
                    await message.send_copy(chat_id=tg_id)
                except Exception as e:
                    print(f"Не удалось отправить сообщение пользователю с id {tg_id}: {e}")
    await message.answer(text="Ваше послание уже у получателей!",
                         reply_markup=keyboard_admin_exit)


@router.callback_query(F.data == "button_admin_add_pressed")
async def process_button_admin_add_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.admin_username)
    await callback.message.edit_text(
        text="Введите username"
    )
    await callback.answer()


@router.message(F.text, States.admin_username)
async def add_username(message: types.Message, state: FSMContext):
    await state.get_state()
    username = message.text
    async with async_session() as session:
        user = User(username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    await state.update_data(user_id=user.id)
    await message.answer(text=f"Username:\n\n<i>{username}</i>\n\n"
                              f"Введите telegram_id",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_tg_id)


@router.message(F.text, States.admin_tg_id)
async def add_tg_id(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_tg_id = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.tg_id = new_tg_id
        await session.commit()
    await message.answer(text=f"Telegram_id:\n\n<i>{new_tg_id}</i>\n\n"
                              f"Введите nlSS_acc1",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_nlSS_acc1)


@router.message(F.text, States.admin_nlSS_acc1)
async def add_nlSS_acc1(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_nlSS_acc1 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.nlSS_acc1 = new_nlSS_acc1
        await session.commit()
    await message.answer(text=f"nlSS_acc1:\n\n<i>{new_nlSS_acc1}</i>\n\n"
                              f"Введите nlTrojan_acc1",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_nlTrojan_acc1)


@router.message(F.text, States.admin_nlTrojan_acc1)
async def add_nlTrojan_acc1(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_nlTrojan_acc1 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.nlTrojan_acc1 = new_nlTrojan_acc1
        await session.commit()
    await message.answer(text=f"nlTrojan_acc1:\n\n<i>{new_nlTrojan_acc1}</i>\n\n"
                              f"Введите finSS_acc1",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_finSS_acc1)


@router.message(F.text, States.admin_finSS_acc1)
async def add_finSS_acc1(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_finSS_acc1 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.finSS_acc1 = new_finSS_acc1
        await session.commit()
    await message.answer(text=f"finSS_acc1:\n\n<i>{new_finSS_acc1}</i>\n\n"
                              f"Введите finTrojan_acc1",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_finTrojan_acc1)


@router.message(F.text, States.admin_finTrojan_acc1)
async def add_finTrojan_acc1(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_finTrojan_acc1 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.finTrojan_acc1 = new_finTrojan_acc1
        await session.commit()
    await message.answer(text=f"finTrojan_acc1:\n\n<i>{new_finTrojan_acc1}</i>\n\n"
                              f"Введите rusSS_acc1",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_rusSS_acc1)


@router.message(F.text, States.admin_rusSS_acc1)
async def add_rusSS_acc1(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_rusSS_acc1 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.rusSS_acc1 = new_rusSS_acc1
        await session.commit()
    await message.answer(text=f"rusSS_acc1:\n\n<i>{new_rusSS_acc1}</i>\n\n"
                              f"Введите rusTrojan_acc1",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_rusTrojan_acc1)


@router.message(F.text, States.admin_rusTrojan_acc1)
async def add_rusTrojan_acc1(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_rusTrojan_acc1 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.rusTrojan_acc1 = new_rusTrojan_acc1
        await session.commit()
    await message.answer(text=f"rusTrojan_acc1:\n\n<i>{new_rusTrojan_acc1}</i>\n\n"
                              f"Введите nlSS_acc2",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_nlSS_acc2)


@router.message(F.text, States.admin_nlSS_acc2)
async def add_nlSS_acc2(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_nlSS_acc2 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.nlSS_acc2 = new_nlSS_acc2
        await session.commit()
    await message.answer(text=f"nlSS_acc2:\n\n<i>{new_nlSS_acc2}</i>\n\n"
                              f"Введите nlTrojan_acc2",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_nlTrojan_acc2)


@router.message(F.text, States.admin_nlTrojan_acc2)
async def add_nlTrojan_acc2(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_nlTrojan_acc2 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.nlTrojan_acc2 = new_nlTrojan_acc2
        await session.commit()
    await message.answer(text=f"nlTrojan_acc2:\n\n<i>{new_nlTrojan_acc2}</i>\n\n"
                              f"Введите finSS_acc2",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_finSS_acc2)


@router.message(F.text, States.admin_finSS_acc2)
async def add_finSS_acc2(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_finSS_acc2 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.finSS_acc2 = new_finSS_acc2
        await session.commit()
    await message.answer(text=f"finSS_acc2:\n\n<i>{new_finSS_acc2}</i>\n\n"
                              f"Введите finTrojan_acc2",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_finTrojan_acc2)


@router.message(F.text, States.admin_finTrojan_acc2)
async def add_finTrojan_acc2(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_finTrojan_acc2 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.finTrojan_acc2 = new_finTrojan_acc2
        await session.commit()
    await message.answer(text=f"finTrojan_acc2:\n\n<i>{new_finTrojan_acc2}</i>\n\n"
                              f"Введите rusSS_acc2",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_rusSS_acc2)


@router.message(F.text, States.admin_rusSS_acc2)
async def add_rusSS_acc2(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_rusSS_acc2 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.rusSS_acc2 = new_rusSS_acc2
        await session.commit()
    await message.answer(text=f"rusSS_acc2:\n\n<i>{new_rusSS_acc2}</i>\n\n"
                              f"Введите rusTrojan_acc2",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_rusTrojan_acc2)


@router.message(F.text, States.admin_rusTrojan_acc2)
async def add_rusTrojan_acc2(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_rusTrojan_acc2 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.rusTrojan_acc2 = new_rusTrojan_acc2
        await session.commit()
    await message.answer(text=f"rusTrojan_acc2:\n\n<i>{new_rusTrojan_acc2}</i>\n\n"
                              f"Введите nlSS_acc3",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_nlSS_acc3)


@router.message(F.text, States.admin_nlSS_acc3)
async def add_nlSS_acc3(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_nlSS_acc3 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.nlSS_acc3 = new_nlSS_acc3
        await session.commit()
    await message.answer(text=f"nlSS_acc3:\n\n<i>{new_nlSS_acc3}</i>\n\n"
                              f"Введите nlTrojan_acc3",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_nlTrojan_acc3)


@router.message(F.text, States.admin_nlTrojan_acc3)
async def add_nlTrojan_acc3(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_nlTrojan_acc3 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.nlTrojan_acc3 = new_nlTrojan_acc3
        await session.commit()
    await message.answer(text=f"nlTrojan_acc3:\n\n<i>{new_nlTrojan_acc3}</i>\n\n"
                              f"Введите finSS_acc3",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_finSS_acc3)


@router.message(F.text, States.admin_finSS_acc3)
async def add_finSS_acc3(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_finSS_acc3 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.finSS_acc3 = new_finSS_acc3
        await session.commit()
    await message.answer(text=f"finSS_acc3:\n\n<i>{new_finSS_acc3}</i>\n\n"
                              f"Введите finTrojan_acc3",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_finTrojan_acc3)


@router.message(F.text, States.admin_finTrojan_acc3)
async def add_finTrojan_acc3(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_finTrojan_acc3 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.finTrojan_acc3 = new_finTrojan_acc3
        await session.commit()
    await message.answer(text=f"finTrojan_acc3:\n\n<i>{new_finTrojan_acc3}</i>\n\n"
                              f"Введите rusSS_acc3",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_rusSS_acc3)

@router.message(F.text, States.admin_rusSS_acc3)
async def add_rusSS_acc3(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_rusSS_acc3 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.rusSS_acc3 = new_rusSS_acc3
        await session.commit()
    await message.answer(text=f"rusSS_acc3:\n\n<i>{new_rusSS_acc3}</i>\n\n"
                              f"Введите rusTrojan_acc3",
                         reply_markup=keyboard_admin_skip
                         )
    await state.set_state(States.admin_rusTrojan_acc3)


@router.message(F.text, States.admin_rusTrojan_acc3)
async def add_rusTrojan_acc3(message: types.Message, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    new_rusTrojan_acc3 = message.text
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.rusTrojan_acc3 = new_rusTrojan_acc3
        await session.commit()
    await message.answer(text=f"rusTrojan_acc3:\n\n<i>{new_rusTrojan_acc3}</i>\n\n"
                              f"Пользователь добавлен\n\n"
                              f"{user.id}\n\n"
                              f"{user.username}\n\n"
                              f"{user.tg_id}\n\n"
                              f"{user.nlSS_acc1}\n\n"
                              f"{user.nlTrojan_acc1}\n\n"
                              f"{user.finSS_acc1}\n\n"
                              f"{user.finTrojan_acc1}\n\n"
                              f"{user.rusSS_acc1}\n\n"
                              f"{user.rusTrojan_acc1}\n\n"
                              f"{user.nlSS_acc2}\n\n"
                              f"{user.nlTrojan_acc2}\n\n"
                              f"{user.finSS_acc2}\n\n"
                              f"{user.finTrojan_acc2}\n\n"
                              f"{user.rusSS_acc2}\n\n"
                              f"{user.rusTrojan_acc2}\n\n"
                              f"{user.nlSS_acc3}\n\n"
                              f"{user.nlTrojan_acc3}\n\n"
                              f"{user.finSS_acc3}\n\n"
                              f"{user.finTrojan_acc3}\n\n"
                              f"{user.rusSS_acc3}\n\n"
                              f"{user.rusTrojan_acc3}\n\n",
                         reply_markup=keyboard_admin_exit
                         )


@router.callback_query(F.data == "button_admin_exit_pressed")
async def process_button_admin_exit_press(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="<b>Главное меню</b>",
        reply_markup=keyboard_main
    )
    await callback.answer()


@router.callback_query(F.data == "button_admin_skip_pressed")
async def process_button_admin_skip_press(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == States.admin_tg_id:
        await callback.message.answer("Введите nlSS_acc1:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_nlSS_acc1)

    elif current_state == States.admin_nlSS_acc1:
        await callback.message.answer("Введите nlTrojan_acc1:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_nlTrojan_acc1)
    elif current_state == States.admin_nlTrojan_acc1:
        await callback.message.answer("Введите finSS_acc1:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_finSS_acc1)
    elif current_state == States.admin_finSS_acc1:
        await callback.message.answer("Введите finTrojan_acc1:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_finTrojan_acc1)
    elif current_state == States.admin_finTrojan_acc1:
        await callback.message.answer("Введите rusSS_acc1:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_rusSS_acc1)
    elif current_state == States.admin_rusSS_acc1:
        await callback.message.answer("Введите rusTrojan_acc1:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_rusTrojan_acc1)
    elif current_state == States.admin_rusTrojan_acc1:
        await callback.message.answer("Введите nlSS_acc2:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_nlSS_acc2)

    elif current_state == States.admin_nlSS_acc2:
        await callback.message.answer("Введите nlTrojan_acc2:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_nlTrojan_acc2)
    elif current_state == States.admin_nlTrojan_acc2:
        await callback.message.answer("Введите finSS_acc2:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_finSS_acc2)
    elif current_state == States.admin_finSS_acc2:
        await callback.message.answer("Введите finTrojan_acc2:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_finTrojan_acc2)
    elif current_state == States.admin_finTrojan_acc2:
        await callback.message.answer("Введите nlSS_acc3:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_nlSS_acc3)
    elif current_state == States.admin_rusSS_acc2:
        await callback.message.answer("Введите rusTrojan_acc2:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_rusTrojan_acc2)
    elif current_state == States.admin_rusTrojan_acc2:
        await callback.message.answer("Введите nlSS_acc3:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_nlSS_acc3)

    elif current_state == States.admin_nlSS_acc3:
        await callback.message.answer("Введите nlTrojan_acc3:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_nlTrojan_acc3)
    elif current_state == States.admin_nlTrojan_acc3:
        await callback.message.answer("Введите finSS_acc3:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_finSS_acc3)
    elif current_state == States.admin_finSS_acc3:
        await callback.message.answer("Введите finTrojan_acc3:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_finTrojan_acc3)
    elif current_state == States.admin_finTrojan_acc3:
        await callback.message.answer("Введите rusSS_acc3:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_rusSS_acc3)
    elif current_state == States.admin_rusSS_acc3:
        await callback.message.answer("Введите rusTrojan_acc3:", reply_markup=keyboard_admin_skip)
        await state.set_state(States.admin_rusTrojan_acc3)
    elif current_state == States.admin_rusTrojan_acc3:
        data = await state.get_data()
        user_id = data.get("user_id")
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.id == user_id))
        await callback.message.answer(text=f"Пользователь добавлен\n\n"
                                           f"{user.id}\n\n"
                                           f"{user.username}\n\n"
                                           f"{user.tg_id}\n\n"
                                           f"{user.nlSS_acc1}\n\n"
                                           f"{user.nlTrojan_acc1}\n\n"
                                           f"{user.finSS_acc1}\n\n"
                                           f"{user.finTrojan_acc1}\n\n"
                                           f"{user.rusSS_acc1}\n\n"
                                           f"{user.rusTrojan_acc1}\n\n"
                                           f"{user.nlSS_acc2}\n\n"
                                           f"{user.nlTrojan_acc2}\n\n"
                                           f"{user.finSS_acc2}\n\n"
                                           f"{user.finTrojan_acc2}\n\n"
                                           f"{user.rusSS_acc2}\n\n"
                                           f"{user.rusTrojan_acc2}\n\n"
                                           f"{user.nlSS_acc3}\n\n"
                                           f"{user.nlTrojan_acc3}\n\n"
                                           f"{user.finSS_acc3}\n\n"
                                           f"{user.finTrojan_acc3}\n\n"
                                           f"{user.rusSS_acc3}\n\n"
                                           f"{user.rusTrojan_acc3}\n\n",
                                      reply_markup=keyboard_admin_exit)
    await callback.answer()


@router.callback_query(F.data == "button_admin_skip_all_pressed")
async def process_button_admin_skip_press(callback: CallbackQuery, state: FSMContext):
    await state.get_state()
    data = await state.get_data()
    user_id = data.get("user_id")
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
    await callback.message.answer(text=f"Пользователь добавлен\n\n"
                                       f"{user.id}\n\n"
                                       f"{user.username}\n\n"
                                       f"{user.tg_id}\n\n"
                                       f"{user.nlSS_acc1}\n\n"
                                       f"{user.nlTrojan_acc1}\n\n"
                                       f"{user.finSS_acc1}\n\n"
                                       f"{user.finTrojan_acc1}\n\n"
                                       f"{user.rusSS_acc1}\n\n"
                                       f"{user.rusTrojan_acc1}\n\n"
                                       f"{user.nlSS_acc2}\n\n"
                                       f"{user.nlTrojan_acc2}\n\n"
                                       f"{user.finSS_acc2}\n\n"
                                       f"{user.finTrojan_acc2}\n\n"
                                       f"{user.rusSS_acc2}\n\n"
                                       f"{user.rusTrojan_acc2}\n\n"
                                       f"{user.nlSS_acc3}\n\n"
                                       f"{user.nlTrojan_acc3}\n\n"
                                       f"{user.finSS_acc3}\n\n"
                                       f"{user.finTrojan_acc3}\n\n"
                                       f"{user.rusSS_acc3}\n\n"
                                       f"{user.rusTrojan_acc3}\n\n",
                                  reply_markup=keyboard_admin_exit)
    await callback.answer()


@router.callback_query(F.data == "button_admin_exit_pressed")
async def process_button_admin_exit_press(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="<b>Главное меню</b>",
        reply_markup=keyboard_main
    )
    await callback.answer()
