from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    FIO = State()
    phone = State()


class BookingState(StatesGroup):
    owner = State()
    time = State()
    description = State()
    group = State()
    persons = State()
