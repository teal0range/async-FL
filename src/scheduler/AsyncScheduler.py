import time

from scheduler import BaseScheduler


class AsyncScheduler(BaseScheduler.BaseScheduler):
    def __init__(self, server_thread_lock, config):
        BaseScheduler.BaseScheduler.__init__(self, server_thread_lock, config)
        self.schedule_interval = config["schedule_interval"]
        self.schedule_delay = config["schedule_delay"]

    def run(self):
        last_s_time = -1
        while self.current_t.get_time() <= self.T:
            current_time = self.current_t.get_time() - 1
            schedule_time = self.schedule_t.get_time()
            # 每隔一段时间进行一次schedule
            if current_time % self.schedule_interval == 0 and current_time != last_s_time:
                self.print_lock.acquire()
                print("| current_time |", current_time % self.schedule_interval, "= 0", current_time, "!=", last_s_time)
                print("| queue.size |", self.queue_manager.size(), "<= ", self.schedule_delay)
                self.print_lock.release()
                # 如果server已收到且未使用的client更新数小于schedule delay，则进行schedule
                if self.queue_manager.size() <= self.schedule_delay:
                    last_s_time = current_time
                    self.print_lock.acquire()
                    print("Begin client select")
                    self.print_lock.release()
                    selected_client_threads = self.client_select()
                    self.print_lock.acquire()
                    print("\nSchedulerThread select(", len(selected_client_threads), "clients):")
                    for s_client_thread in selected_client_threads:
                        print(s_client_thread.get_client_id(), end=" | ")
                        # 将server的模型参数和时间戳发给client
                        s_client_thread.set_client_weight(self.server_weights)
                        s_client_thread.set_time_stamp(current_time)
                        s_client_thread.set_schedule_time_stamp(schedule_time)
                        # 启动一次client线程
                        s_client_thread.set_event()
                    print("\n-----------------------------------------------------------------Schedule complete")
                    self.print_lock.release()
                    self.schedule_t.time_add()
                else:
                    self.print_lock.acquire()
                    print("\n-----------------------------------------------------------------No Schedule")
                    self.print_lock.release()
                time.sleep(0.01)
            else:
                time.sleep(0.01)
