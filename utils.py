def bymonth(anylist: list):
    for i in range(0, len(anylist), 12):
        yield anylist[i:i + 12]