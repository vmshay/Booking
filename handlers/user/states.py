from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    FIO = State()
    phone = State()


class BookingState(StatesGroup):
    start = State()
    time = State()
    description = State()


class SendBugState(StatesGroup):
    send_bug = State()


class MessageToAll(StatesGroup):
    send_message = State()