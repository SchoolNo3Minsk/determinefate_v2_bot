from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, ReplyKeyboardRemove, \
    InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from src.database import Queries
from src.utils.state import Add
from src.utils.keyboards import cancel_keyboard
from src.utils.others import check_canceled, get_phrase

from src.utils.parser import api


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
    uid: int | None
    surname: str | None
    name: str | None
    middlename: str | None
    year_of_birth: str | int | None
    rank: str | None
    accepter: str | None


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
        await message.reply(f'🎖️ {get_phrase(locale, "input_rank")}:',
                            reply_markup=keyboard)
        await state.update_data(year_of_birth=0)
        return await state.set_state(Add.rank)

    if not message.text.isdigit():
        await message.reply(f'⛔ {get_phrase(locale, "error_year")}')
        return await state.set_state(Add.year_of_birth)

    await message.reply(f'🎖️ {get_phrase(locale, "input_rank")}:', reply_markup=keyboard)

    await state.update_data(year_of_birth=int(message.text))
    await state.set_state(Add.rank)


@router.message(StateFilter(Add.rank))
async def rank(message: Message, state: FSMContext, locale: str):
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb2(await get_user_language(message.from_id)), resize_keyboard=True)

    await state.update_data(rank=message.text, accepter="False")

    data = await state.get_data()

    for key, value in data.items():
        if value == '➡️Пропустить' or value == "➡️Прапусціць":
            data[key] = ""

        form = CreatedForm(**data)

    keyboard = ReplyKeyboardMarkup(keyboard=kb3(locale), resize_keyboard=True)

    await message.reply(f"""
<b>{get_phrase(locale, "check_inputed_info")}:</b>\n\n
<b>{get_phrase(locale, "name")}: </b> {form.name}
<b>{get_phrase(locale, "surname")}: </b> {form.surname}
<b>{get_phrase(locale, "middlename")}: </b> {form.middlename}
<b>{get_phrase(locale, "year_of_birth")}: </b> {form.year_of_birth if form.year_of_birth != 0 else ""}
<b>{get_phrase(locale, "rank")}: </b> {form.rank}
""", reply_markup=keyboard)

    await state.set_state(Add.accepter)


@router.message(StateFilter(Add.accepter))
async def rank(message: Message, state: FSMContext, locale: str):
    accepter = message.text

    if accepter == f"❌ {get_phrase(locale, 'cancel')}":
        return

    if accepter == "➡️Да":
        data = await state.get_data()
        form = CreatedForm(**data)

        parse = await api.get_partizans_query(form.surname, form.name, form.middlename, form.year_of_birth, form.rank)
        if not parse:
            await message.reply("Ничего не найдено!")
            await message.delete_reply_markup()
            return

        buttons = InlineKeyboardBuilder()

        number = 0
        text = "<b>На клавиатуре с кнопками выберите нужного человека по номеру:\n</b>"

        for user in parse.root:
            number += 1
            text += f"{number} | {user.full_name} [ID: {user.id}] | {user.date_of_birth} | {user.date_of_die}\n"

            buttons.add(
                InlineKeyboardButton(
                    text=f"{number}. {user.full_name} [ID: {user.id}] | {user.date_of_birth} | {user.date_of_die}",
                    callback_data=f"find:{user.id}"
                )
            )

        buttons.adjust(*[2, 2])

        await message.reply(text, reply_markup=buttons.as_markup())
        await message.delete_reply_markup()


@router.callback_query(lambda c: c.data.startswith('find:'))
async def process_callback_button(callback_query: CallbackQuery):
    id = callback_query.data.split(':')[1]

    partizan = await api.get_partizan(id)
    if partizan is None:
        return await callback_query.answer("Произошла ошибка.")

    text = (
        f"<b>Информация из донесения о безвозвратных потерях:</b>\n\n"
        f"ID: {id}\n\n"
        f"Фамилия: {partizan.surname}\n"
        f"Имя: {partizan.name}\n"
        f"Отчество: {partizan.middlename}\n"
        f"Дата рождения: {partizan.date_of_birth}\n"
        f"Место рождения: {partizan.place_of_birth}\n"
        f"Дата и место призыва: {partizan.call_place}\n"
        f"Последнее место службы: {partizan.last_call_place}\n"
        f"Воинское звание: {partizan.rank}\n"
        f"Причина выбытия: {partizan.reason_of_leave}\n"
        f"Дата выбытия: {partizan.date_of_leave}\n"
        f"Место выбытия: {partizan.place_of_leave}\n"
        f"Название источника донесения: {partizan.issue}\n"
    )

    await callback_query.message.reply(text)
