import sys
import io
import asyncio
import time
import random

# Đảm bảo Encoding UTF-8 trên Windows CMD
if sys.platform == "win32":
    try:
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, io.UnsupportedOperation):
        pass
from typing import List, Callable, Any

class DripFeedWorker:
    """
    🌊 BỘ ĐIỀU PHỐI HỎA LỰC (Drip-Feed Worker)
    Nhiệm vụ: Băm nhỏ các request nặng, chống tràn RAM/CPU.
    Công nghệ: asyncio.Semaphore(10) + Throttling.
    """
    def __init__(self, concurrency_limit: int = 10, delay_between_batches: float = 2.0):
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.delay = delay_between_batches
        self.results = []

    async def _throttled_task(self, task_func: Callable, *args, **kwargs) -> Any:
        """Thực thi task với Semaphore khống chế."""
        async with self.semaphore:
            try:
                # Giả lập thời gian xử lý và tránh dồn dập
                await asyncio.sleep(random.uniform(0.5, self.delay))
                
                # Thực thi task thực tế (nếu là sync thì wrap bằng run_in_executor)
                if asyncio.iscoroutinefunction(task_func):
                    result = await task_func(*args, **kwargs)
                else:
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(None, task_func, *args, **kwargs)
                
                return result
            except Exception as e:
                print(f"⚠️ [DripFeed] Task thất bại: {e}")
                return None

    async def process_batch(self, tasks: List[dict]):
        """
        Xử lý một danh sách các task theo kiểu nhỏ giọt (Drip-feed).
        tasks format: [{"func": callable, "args": [], "kwargs": {}}]
        """
        print(f"(Launch) [DripFeed] Khoi chay hoa luc cho {len(tasks)} tasks (Concurrency: {self.semaphore._value})")
        
        async_tasks = [
            self._throttled_task(t["func"], *t.get("args", []), **t.get("kwargs", {}))
            for t in tasks
        ]
        
        self.results = await asyncio.gather(*async_tasks)
        print(f"(Success) [DripFeed] Da hoan tat xu ly {len(tasks)} tasks.")
        return self.results

# Singleton instance
drip_feeder = DripFeedWorker()

# --- Example Usage (Test) ---
async def mock_scraping_task(item_id: int):
    # print(f"Cào dữ liệu cho item {item_id}...")
    await asyncio.sleep(1)
    return {"id": item_id, "status": "success"}

async def test():
    tasks = [{"func": mock_scraping_task, "args": [i]} for i in range(50)]
    worker = DripFeedWorker(concurrency_limit=5)
    start = time.time()
    await worker.process_batch(tasks)
    print(f"Time taken: {time.time() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(test())
