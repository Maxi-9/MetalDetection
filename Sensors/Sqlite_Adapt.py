import queue
import sqlite3
import threading
import time
from collections import defaultdict


class Store_Type:
    def __init__(self):
        raise NotImplementedError("Don't create from base class.")

    def _table_def(self):
        raise NotImplementedError()


# Custom Row featcher
class Rows:
    def __init__(self, c: sqlite3.Cursor, query: str, by: int):
        self.hasRows = True
        self.cur = c
        self.by = by

        self.cur.execute(query)

    def getNext(self):
        rows = self.cur.fetchmany(self.by)
        if rows is None or len(rows) == 0:
            self.hasRows = False
            return []
        return rows


class sqliteManager:
    def get_fps(self) -> defaultdict:
        return self.FPS_now

    def __init__(self, dbname):
        self.dbname = dbname
        self.data_queue = queue.Queue()
        self.lock = threading.Lock()

        # Add a flag to indicate whether the worker thread should stop
        self.stop_requested = threading.Event()

        self.FPS_start = None
        self.FPS_count = defaultdict(int)
        self.FPS_now = defaultdict(float)
        self.created_set = set(str)

        self.FPS_start = float(time.perf_counter())

        # Start a daemon thread to handle database commits
        self.db_thread = threading.Thread(
            target=self._db_worker, args=(dbname,), daemon=True
        )
        self.db_thread.start()

    def countPacket(self, table: str):
        self.FPS_count[str(table)] += 1

        time_now = float(time.perf_counter())

        if self.FPS_start + 1 < time_now:
            for device in self.FPS_now:
                self.FPS_now[device] = 0
            for device in self.FPS_count:
                self.FPS_now[device] = round(
                    self.FPS_count[device] / (time_now - self.FPS_start), 2
                )
                self.FPS_count[device] = 0

            self.FPS_start = float(time.perf_counter())

    def write_data(self, data, cur_table):
        # Add data to the queue from multiple threads
        self.data_queue.put((data, cur_table))
        self.countPacket(cur_table)

    def execute(self, c: sqlite3.Cursor, query: str):
        c.execute(query)

    def _db_worker(self, dbname):
        conn = sqlite3.connect(dbname)
        conn.isolation_level = None
        cur = conn.cursor()
        cur.execute("BEGIN")

        start_time = time.perf_counter()
        while not self.data_queue.empty() or not self.stop_requested.is_set():
            # Get the next data struct from the queue
            try:
                data, cur_table = self.data_queue.get(timeout=1)
            except queue.Empty:
                continue

            # Lock the thread while writing to the database to ensure thread safety
            with self.lock:
                if cur_table not in self.created_set:
                    self.execute(cur, data.create_str(cur_table))
                self.execute(cur, data.add_str(cur_table))

                # Commit every 3 seconds or if count reaches 200
                if time.perf_counter() - start_time > 3:
                    print("Commit")
                    conn.commit()
                    cur.execute("BEGIN")
                    start_time = time.perf_counter()

            # Mark the task as done
            self.data_queue.task_done()

        # Commit any remaining transactions and close the connection
        conn.commit()
        conn.close()

    # Stops and waits for last of rows to be written
    def stop(self):
        # Set the stop flag
        self.stop_requested.set()

        # Wait for the worker thread to stop
        self.db_thread.join()
