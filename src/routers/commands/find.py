from aiogram import Router
from typing import List
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from pydantic import BaseModel

from src.utils.state import Add
from src.utils.keyboards import cancel_keyboard
from src.utils.others import check_canceled, get_phrase


router = Router()

def kb(language: str) -> List[List[KeyboardButton]]:
    return [
        [KeyboardButton(text=f'❌{get_phrase(language, "cancel")}')]
    ]


def kb2(language: str) -> List[List[KeyboardButton]]:
    return [
        [KeyboardButton(text=f'➡️{get_phrase(language, "skip")}')],
        [KeyboardButton(text=f'❌{get_phrase(language, "cancel")}')]
    ]


def kb3(language: str) -> List[List[KeyboardButton]]:
    return [
        [KeyboardButton(text=f'➡️Да')],
        [KeyboardButton(text=f'❌{get_phrase(language, "cancel")}')]
    ]


class CreatedForm(BaseModel):
    uid: int
    surname: str
    name: str
    middlename: str
    year_of_birth: int
    rank: str
    accepter: str


@router.message(Command("find"))
@check_canceled
async def find(message: Message, state: FSMContext, locale: str):
    if await state.get_state():
        return await message.reply(f"🚥 {get_phrase(locale, 'already_state')}")

    await state.update_data(uid=message.from_user.id)
    keyboard = ReplyKeyboardMarkup(keyboard=cancel_keyboard(locale), resize_keyboard=True)

    await state.set_state(Add.name)
    await message.reply(f'🧍 {get_phrase(locale, "input_name")}:', reply_markup=keyboard)


@router.message(StateFilter(Add.name))
@check_canceled
async def add_surname(message: Message, state: FSMContext, locale: str):
    keyboard = ReplyKeyboardMarkup(keyboard=kb(locale), resize_keyboard=True)

    await message.reply(f'🧍 {get_phrase(locale, "input_surname")}:',
                        reply_markup=keyboard)
    await state.update_data(name=message.text)
    await state.set_state(Add.surname)


@router.message(StateFilter(Add.surname))
@check_canceled
async def add_middlename(message: Message, state: FSMContext, locale: str):
    keyboard = ReplyKeyboardMarkup(keyboard=kb2(locale), resize_keyboard=True)
    await message.reply(f'🧑‍🦳 {get_phrase(locale, "input_middlename")}:',
                        reply_markup=keyboard)
    await state.update_data(surname=message.text)
    await state.set_state(Add.middlename)


@router.message(StateFilter(Add.middlename))
@check_canceled
async def add_date(message: Message, state: FSMContext, locale: str):
    keyboard = ReplyKeyboardMarkup(keyboard=kb2(locale), resize_keyboard=True)
    await message.reply(f'🎂 {get_phrase(locale, "input_year_of_birth")}:',
                        reply_markup=keyboard)
    await state.update_data(middlename=message.text)
    await state.set_state(Add.year_of_birth)


@router.message(StateFilter(Add.year_of_birth))
@check_canceled
async def add_rank(message: Message, state: FSMContext, locale: str):
    keyboard = ReplyKeyboardMarkup(keyboard=kb2(locale), resize_keyboard=True)

    if message.text == "➡️Пропустить" or message.text == "➡️Прапусціць":
        await message.reply(f'🎖️ {get_phrase(locale, "input_year_of_birth")}:',
                            reply_markup=keyboard)
        await state.update_data(year_of_birth=0)
        return await Add.rank.set()

    if not message.text.isdigit():
        await message.reply(f'⛔ {get_phrase(locale, "error_year")}')
        return await Add.year_of_birth.set()

    await message.reply(f'🎖️ {get_phrase(locale, "input_rank")}:', reply_markup=keyboard)

    await state.update_data(year_of_birth=int(message.text))
    await state.set_state(Add.rank)


@router.message(StateFilter(Add.rank))
async def rank(message: Message, state: FSMContext, locale: str):
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb2(await get_user_language(message.from_id)), resize_keyboard=True)

    await state.update_data(rank=message.text, accepter="False")

    async with state.get_data() as data:
        for key, value in data.items():
            if value == '➡️Пропустить' or value == "➡️Прапусціць":
                data[key] = ""

        form = CreatedForm(**data)

    keyboard = ReplyKeyboardMarkup(keyboard=kb3(locale), resize_keyboard=True)

    await message.reply(f"""
<b>{get_phrase(locale, "check_inputed_info")}:</b>
<b>{get_phrase(locale, "name")}: </b> {form.name}
<b>{get_phrase(locale, "surnamesurname")}: </b> {form.surname}
<b>{get_phrase(locale, "middlename")}: </b> {form.middlename}
<b>{get_phrase(locale, "year_of_birth")}: </b> {form.year_of_birth}
<b>{get_phrase(locale, "rank")}: </b> {form.rank}
""", reply_markup=keyboard)

    await state.set_state(Add.accepter)


# @router.message(state=Add.accepter)
# async def rank(message: Message, state: FSMContext, locale: str):
#     accepter = message.text
#
#     if accepter == f"❌ {get_phrase(locale, 'cancel')}":
#         return
#
#     if accepter == "➡️Да":
#         async with state.proxy() as data:
#             form = CreatedForm(**data)
#         await state.finish()
#
#         query = await Queries.create(uid=message.from_id, name=form.name, surname=form.surname,
#                                      middlename=form.middlename, year_of_birth=form.year_of_birth,
#                                      rank=form.rank)
#
#         parse = await get_partizans(form.surname, form.name, form.middlename, form.year_of_birth, form.rank)
#         if not parse:
#             return await message.reply("Ничего не найдено!")
#
#         buttons = InlineKeyboardMarkup(row_width=2)
#         number = 0
#         text = "<b>На клавиатуре с кнопками выберите нужного человека по номеру:\n</b>"
#
#         for i in parse:
#             number = number + 1
#             text += f"{number}. {parse[i]['full_name']} [ID: {i}] | {parse[i]['date_of_birth']} | {parse[i]['date_of_die']}\n"
#             buttons.add(
#                 InlineKeyboardButton(text=f"{number}. {parse[i]['full_name']} [ID: {i}]", callback_data=f"find:{i}"))
#
#         text += f"\nСсылка на результат: https://t.me/determinefateBot?start=search_{query.id}"
#
#         await message.reply(text, reply_markup=buttons)


# @router.callback_query(lambda c: c.data.startswith('find:'))
# async def process_callback_button(callback_query: CallbackQuery, locale: str):
#     id = callback_query.data.split(':')[1]
#
#     partizan = await get_partizan_by_id(id)
#     if partizan is None:
#         return await callback_query.answer("Произошла ошибка.")
#
#     text = f"""
# <b>Информация из донесения о безвозвратных потерях:</b>
#
# ID: {id}
#
# Фамилия: {partizan["surname"]}
# Имя: {partizan["name"]}
# Отчество: {partizan["middlename"]}
# Дата рождения: {partizan["date_of_bitrh"]}
# Место рождения: {partizan["place_of_birth"]}
# Дата и место призыва: {partizan["call_place"]}
# Последнее место службы: {partizan["last_call_place"]}
# Воинское звание: {partizan["rank"]}
# Причина выбытия: {partizan["reason_of_leave"]}
# Дата выбытия: {partizan["date_of_leave"]}
# Место выбытия: {partizan["place_of_leave"]}
# Название источника донесения: {partizan["issue"]}
#
# Ссылка на результат: https://t.me/determinefateBot?start=id_{id}
# Информация была взята с сайта https://obd-memorial.ru/
# """
#
#     await callback_query.message.reply(text)
