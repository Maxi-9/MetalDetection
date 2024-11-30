import queue
import sqlite3
import threading
import time
from collections import defaultdict





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

    def _execute(self, c: sqlite3.Cursor, query: str):
        c.execute(query)

    def _db_worker(self, dbname):
        conn = sqlite3.connect(dbname, isolation_level=None)
        # Connect to the SQLite database with the specified optimizations

        # These may increase chance of corruption if loss of power occurs during access
        conn.execute("PRAGMA journal_mode=MEMORY")
        conn.execute("PRAGMA synchronous=OFF")

        # Set the locking mode to exclusive
        conn.execute("PRAGMA locking_mode=EXCLUSIVE")

        conn.isolation_level = None
        cur = conn.cursor()
        cur.execute("BEGIN")

        start_time = time.perf_counter()
        while not self.data_queue.empty() or not self.stop_requested.is_set():
            # Get the next data struct from the queue
            got_data = False
            try:
                data, cur_table = self.data_queue.get(timeout=1)
                got_data = True
            except queue.Empty:
                continue

            # Lock the thread while writing to the database
            with self.lock:
                # print(data)
                self._execute(cur, data)

                # Commit every 3 seconds or if count reaches 200
                if time.perf_counter() - start_time > 3 and got_data:
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
