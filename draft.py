import intervaltree

it = intervaltree.IntervalTree()
it.addi('08:00', '11:00')
it.addi('16:40', '17:50')
it.addi('14:00', '16:30')

print(f"Одно значение: {it.overlaps('10:01', '14:00')}")
print(f"Перекрытие интервала: {it.overlaps('07:00', '12:00')}")
print(f"Внутри интервала: {it.overlaps('15:00', '15:30')}")
print(f"Пересекает: {it.overlaps('12:00', '13:00')}")

