import datetime

__all__ = [
        "tprint",
        ]

def tprint(text = ""):
    print("%s: " % (datetime.datetime.now().isoformat()) + str(text))

tprint("Please revise this package in Nash (10.20.17.52).")

