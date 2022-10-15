# Для форматирования сообщений

non_register = "Команды станут доступны после регистрации"


def events_welcome(data):
    text = (f"выберите дату чтобы увидеть список мероприятий\n\n"
            f"Так же календарь мероприятий можно посмотреть в "
            f"<a href=moodle.tomtit-tomsk.ru>Moodle</a>\n\n"
            f"Сегодняшняя дата <b>{data}</b>")
    return text


def select_date_empty(data):
    pass


def select_date():
    pass



