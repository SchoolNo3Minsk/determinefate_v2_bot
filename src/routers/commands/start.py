from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from src.database.models.users import Users
from src.utils.keyboards import get_language_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply("<b>⚙️ Выберите язык/Абярыце мову</b>", reply_markup=get_language_keyboard().as_markup())


@router.callback_query(F.data.startswith("language"))
async def choose_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    user = await Users.filter(uid=callback.from_user.id).first()

    if user:
        user.language = lang
        await user.save()

        return await callback.message.reply("Вы выбрали язык: ") #  LANGUAGES[lang]

    await Users.create(uid=callback.from_user.id, language=lang)
    await callback.message.reply("Вы выбрали язык: ") #  LANGUAGES[lang]
