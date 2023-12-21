    while not crashed:
        for i in event.get():
            if i.type == KEYDOWN:
                if i.unicode == "q":
                    crashed = True
            if crashed:
                exit()
