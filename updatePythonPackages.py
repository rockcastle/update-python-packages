#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import time
from subprocess import call
import threading

thread_count = 20
filename = "outdate_packages.txt"
pip_name = "pip3"
packList = []
thrds = []
start = time.time()
def get_package_list():
    try:
        call(pip_name + " list --outdated >>" + filename, shell=True)
        with open(filename, "r") as file:
            for s, f in enumerate(file.readlines()):
                if s > 1:
                    pack_name = f.split(" ")[0]
                    if re.search("\w+", pack_name):
                        packList.append(pack_name)
                        # print(s, pack_name)
    except Exception as ex:
        print("Packages list exception: ", ex)


class Update_Packs(threading.Thread):
    def __init__(self, which_thread, *args):
        threading.Thread.__init__(self)

        self.w_thread = which_thread
        self.prev_endloop = 0
        self.plist = packList

    def get_update(self, *arg):
        try:
            self.start_loop = int(round(len(self.plist) / thread_count)) * self.w_thread
            if (self.w_thread == thread_count - 1):
                self.end_loop = len(self.plist)
            else:
                self.end_loop = self.start_loop + int(round(len(self.plist) / thread_count))
                print(self.end_loop)
                print(self.prev_endloop)

                if ((not self.prev_endloop == 0) and (not self.prev_endloop == self.end_loop)):
                    self.end_loop = self.prev_endloop + 1
                self.prev_endloop += self.end_loop + 1
            print("starting loop at: " + str(self.start_loop) + " ending loop at: " + str(self.end_loop))
            for i in range(self.start_loop, self.end_loop):
                call(pip_name + " install -U " + self.plist[i], shell=True)
            print(" :X-------------Y: Thread " + str(self.w_thread) + " is done. :Y-------------X:" + " Time left: " + str(
                time.time() - start))
            os.system("sync")
        except Exception as ex:
            print("Update err: ", ex)

    def run(self):
        self.get_update()


def main():
    print("Staring ...")
    get_package_list()
    print("Package list is done")
    time.sleep(1)
    print("Starting threads..")
    for s, i in enumerate(range(thread_count)):
        t = Update_Packs(s)
        print("Starting: --- " + str(s) + " --- from main")
        t.setDaemon(True)
        thrds.append(t)
        t.start()
        # time.sleep(3)
    # time.sleep(1)
    for t in thrds:
        t.join()


if __name__ == "__main__":
    main()

