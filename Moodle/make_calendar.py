from bot import database
from bot.sql import sql_all_events


file_name = "calendar.ics"


async def make(file):
    # # Собираем мероприятия с базы
    db = database.Database()
    data = db.sql_fetchall(sql_all_events())
    event_list = []
    for i in range(0, len(data)):
        e_id = data[i]['id']
        owner = data[i]['name']
        description = data[i]['description']
        date = data[i]['e_date']
        start = data[i]['e_start']
        end = data[i]['e_end']

        start = start.replace(":", "") + "00"
        end = end.replace(":", "") + "00"
        n_start = f"{date.strftime('%Y%m%d')}T{start}"
        n_end = f"{date.strftime('%Y%m%d')}T{end}"
        event = {f"BEGIN:VEVENT\n"
                f"UID:{e_id}@moodle.tomtit-tomsk.ru\n"
                f"SUMMARY:{owner}\n"
                f"DESCRIPTION:{owner}\\n{description}\n"
                f"LOCATION:405\n"
                f"DTSTART;TZID=US-Eastern:{n_start}\n"
                f"DTEND;TZID=US-Eastern:{n_end}\n"
                f"END:VEVENT\n"}
        event_list.append(event)

    with open(file, 'w',encoding="utf-8") as f:
        f.write("START:VCALENDAR\n")
        for elem in event_list:
            f.write("".join(elem))
        f.write("END:VCALENDAR")
        f.close()
    return True
