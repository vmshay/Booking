import shutil

file = 'calendar.ics'
folder = '/var/www/vmshay/calendar.ics'


async def send():
    shutil.copy(file, folder)

