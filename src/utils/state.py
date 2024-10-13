from aiogram.fsm.state import State, StatesGroup


class Add(StatesGroup):
    id = State()

    surname = State()
    name = State()

    middlename = State()
    year_of_birth = State()
    rank = State()
    accepter = State()
