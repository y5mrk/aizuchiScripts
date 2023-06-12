import asyncio
import time

def func(sec: int):
    print("start")
    time.sleep(sec)  # 重い処理の代わり
    print("finish")

for i in range(10):
    print(i)
    if i == 3:
        asyncio.new_event_loop().run_in_executor(None, func, 3)
    time.sleep(1)