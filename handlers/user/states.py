from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    FIO = State()
    phone = State()


class BookingState(StatesGroup):
    start = State()
    time = State()
    description = State()


