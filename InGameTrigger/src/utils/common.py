from multiprocessing import Process
import time


def get_now(as_path=False):
    if as_path:
        return time.strftime("%Y-%m-%dT%H-%M-%S")
    return time.strftime("%Y-%m-%d %H:%M:%S")


def parse_duration(duration: int | float):
    duration_minutes = duration // 60
    duration_seconds = duration % 60
    return f"{duration_minutes}:{int(duration_seconds)}"


# TODO: Implement the following functions
# def assert_udp(func, *args, **kwargs):
#     def decorated_func(*args, **kwargs):
#         try:
#             listen_udp("test", 0.1, dialogue_box=False)
#         except Exception as ex:
#             raise Exception(
#                 "UDP data acquisition failed, Make sure the UDP server is running."
#             )
#         finally:
#             os.remove(f"test.csv")
#         return func(*args, **kwargs)

#     return decorated_func


class AbstractTrigger(Process):
    def run(self): ...
