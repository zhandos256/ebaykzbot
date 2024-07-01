from aiogram.fsm.state import State, StatesGroup


class CalcState(StatesGroup):
    geo = State()
    logistic_type = State()
    category = State()
    weight = State()
    item_price = State()
