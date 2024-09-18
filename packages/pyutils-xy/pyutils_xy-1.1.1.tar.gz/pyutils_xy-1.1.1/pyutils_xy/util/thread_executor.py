# @Coding: UTF-8
# @Time: 2024/9/17 16:48
# @Author: xieyang_ls
# @Filename: thread_executor.py

from threading import Thread

from pyutils_xy.util.queue import Queue, BlockingQueue

from pyutils_xy.util.lock import ReentryLock


class ThreadExecutor:
    __lock: ReentryLock = None

    __executor_count: int = None

    __timeout: int = None

    __task_queue_capacity: int = None

    __task_queue: Queue[callable] = None

    __executors: set[Thread] = None

    def __init__(self, executor_count: int = 5, timeout=2, task_queue_capacity: int = 10):
        self.__lock = ReentryLock()
        self.__executor_count = executor_count
        self.__timeout = timeout
        self.__task_queue_capacity = task_queue_capacity
        self.__task_queue = BlockingQueue(max_capacity=self.__task_queue_capacity, block_time=self.__timeout)
        self.__executors = set()

    def execute(self, task: callable) -> None:
        self.__lock.try_lock()
        try:
            if len(self.__executors) < self.__executor_count:
                executor = ThreadExecutor.__Executor(task, self.__task_queue, self.__lock, self.__executors)
                self.__executors.add(executor)
                executor.start()
                return None
        finally:
            self.__lock.release()
        self.__task_queue.addTail(task)

    class __Executor(Thread):
        __task: callable = None

        __task_queue: Queue[callable] = None

        __lock: ReentryLock = None

        __executors: set[Thread] = None

        def __init__(self, task: callable, task_queue: Queue[callable], lock: ReentryLock, executors: set):
            super().__init__()
            self.__task = task
            self.__task_queue = task_queue
            self.__lock = lock
            self.__executors = executors

        def run(self) -> None:
            while self.__task is not None:
                self.__task()
                self.__task = self.__task_queue.removeHead()
            self.__lock.try_lock()
            try:
                self.__executors.remove(self)
            finally:
                self.__lock.release()
