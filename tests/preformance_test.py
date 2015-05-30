from unittest import TestCase
from source.data_objects.cl import ControllerLinks
from source.data_objects.cl import Key
from source.logic.vk2sk import Vk2Sk
import matplotlib.pyplot as pl
import time

class TestPreformance(TestCase):
    def test_link_time(self):
        c = ControllerLinks()

        times = []

        for i in range(50):
            time1 = time.clock()
            c.add_link((1, 2, 3), Key("A"))
            time2 = time.clock()
            times.append((time2 - time1) * 1000)

        pl.plot([x for x in range(50)], times, marker='o')
        pl.title("Time to add (x) links")
        pl.ylabel("Calculation Time in Milliseconds")
        pl.xlabel("Add Link")
        pl.tight_layout()

        pl.savefig("tests/Plots/Time to Add Links.png")
        pl.close()

    def test_convert_time(self):
        times = []

        for key in Vk2Sk.codes.keys():
            time1 = time.clock()
            Vk2Sk.convert(key)
            time2 = time.clock()
            times.append((time2 - time1) * 1000)

        time1 = time.clock()
        Vk2Sk.convert(0x31, True, True, True)
        time2 = time.clock()
        times.append((time2 - time1) * 1000)

        time1 = time.clock()
        Vk2Sk.convert(0x31, shift=True)
        time2 = time.clock()
        times.append((time2 - time1) * 1000)

        time1 = time.clock()
        Vk2Sk.convert(0x31, True, True, False)
        time2 = time.clock()
        times.append((time2 - time1) * 1000)

        x_vals = [x for x in Vk2Sk.codes.values()]
        x_vals.append("1 TTT")
        x_vals.append("1 FFT")
        x_vals.append("1 TTF")

        pl.xticks([x for x in range(len(Vk2Sk.codes)+3)], x_vals, rotation=90)
        pl.plot([x for x in range(len(Vk2Sk.codes) + 3)], times, marker='o')
        pl.title("Time to convert")
        pl.ylabel("Calculation Time in Milliseconds")
        pl.xlabel("Conversion")
        pl.tight_layout()

        pl.savefig("tests/Plots/Time to Convert.png")
        pl.close()


