#contains the various synchronization objects
from threading import Semaphore, BoundedSemaphore
from queue import SimpleQueue

class Mutex:
    def __init__(self):
        self.sema = BoundedSemaphore(1)
    
    def lock(self, timeout=None) -> bool:
        return self.sema.acquire(timeout=timeout)
    
    def unlock(self) -> None:
        self.sema.release()
    
    #for the with context
    def __enter__(self):
        self.lock()
    
    def __exit__(self, _, __, ___):
        self.unlock()


class MultiSemaphore():
    def __init__(self):
        self.semaList = []
        self.masterSemaphore = Semaphore(0)
        self.mtx = Mutex()

    # mirrors threading.Semaphore.acquire()
    # if acquired, returns which master sema is released
    #   if none acquired, returns None
    def acquire(self, blocking=True, timeout=None) -> int:
        k = self.masterSemaphore.acquire(blocking, timeout)
        if k is False:
            # acquire failed
            return False
        
        #now need to figure out which semaphore is signaled
        with self.mtx:
            for i in range(len(self.semaList)):
                k = self.semaList[i].acquire(blocking=None)
                if k is True:
                    return i
        raise RuntimeError(f"When determining signaled semaphore, none found.")

    def newSemaphore(self, defaultValue):
        with self.mtx:
            self.semaList.append(Semaphore(defaultValue))
            return len(self.semaList) - 1

    def release(self, item):
        try:
            self.semaList[item].release()
            self.masterSemaphore.release()
        except IndexError:
            l = len(self.semaList)
            if(l == 0):
                raise IndexError(f"No registered semaphores. "
                    f"Add one with addSeamphore()")
            else:
                raise IndexError(f"No semaphore with index {item}, "
                    f"should be in range [0,{len(self.semaList)}")
    
    def __len__(self):
        return len(self.semaList)

class SignaledQueue():
    def __init__(self, multiSema):
        self.q = SimpleQueue()
        self.multiSema = multiSema
        self.key = multiSema.newSemaphore(0)

    def put(self, item):
        self.q.put(item)
        self.multiSema.release(self.key)
    
    def get(self):
        return self.q.get()


class SignaledEvent():
    def __init__(self, multiSema):
        self.multiSema = multiSema
        self.key = multiSema.newSemaphore(0)
    
    def trigger(self):
        self.multiSema.release(self.key)