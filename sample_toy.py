from timer import Timer


def func(step):
    a = 0
    for s in range(step):
        a += s


timer = Timer()

func(1000)
timer.lap("func(1000)")
func(1000)
timer.lap("func(1000)")

func(10000)
timer.lap("func(10000)")
func(100000)
timer.lap("func(100000)")
func(1000000)
timer.lap("func(1000000)")
func(10000000)
timer.lap("func(10000000)")


timer.split("end")

print(timer.laps)
print(timer.splits)
print(timer.report())
print(timer.report(sort_key=True))
