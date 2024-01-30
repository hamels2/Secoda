from multiprocessing import Process
from worker import worker



def run():
    procs = []
    while True:
        for i in range(4):
            proc = Process(target=worker)
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()

if __name__ == "__main__":
    run()