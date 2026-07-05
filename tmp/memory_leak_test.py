import time  
data = []  
print("--- STARTING MEMORY LEAK TEST ---")  
while True:  
    data.append(" " * (1024 * 1024 * 10)) # Add 10MB each iteration  
    time.sleep(0.1) 
