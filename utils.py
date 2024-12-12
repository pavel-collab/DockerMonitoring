def ns2hours(time):
    time = time * 1e-9
    time = time / 60
    # if time is less than one minute, don't take it into account
    if time < 1:
        time = None
    else:
        time = round(time, 2)
    return time

def byte2Kb(mem):
    mem = mem / 1024
    # if using memory less than 1 Kb, don't take it into account
    if mem < 1:
        mem = None
    else:
        mem = round(mem, 2)
    return mem