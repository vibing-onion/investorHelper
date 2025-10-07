from multiprocessing import Pool, Manager, cpu_count
import time

def worker(feed):
    with feed["lock"]:
        if feed["cur_count"].value >= feed["max_count"].value:
            if time.time() - feed["last_runtime"].value < 1:
                time.sleep(1 - (time.time() - feed["last_runtime"].value))
            feed["cur_count"].value = 0
            feed["last_runtime"].value = time.time()
        feed["cur_count"].value += 1
    
    return feed["func"](feed["func_feed"])

def rate_limited_multiprocessing(func, func_feed, rate_limit_per_second=1):
    max_cpu = cpu_count()
    manager = Manager()
    
    max_count = manager.Value('i', rate_limit_per_second)
    cur_count = manager.Value('i', 0)
    last_runtime = manager.Value('f', time.time())
    lock = manager.Lock()
    
    with Pool(processes=max_cpu) as pool:
        results = pool.map(worker, [ {"max_count": max_count, "cur_count": cur_count, "last_runtime": last_runtime, "lock": lock, "func": func, "func_feed": f}  for f in func_feed])
    return results