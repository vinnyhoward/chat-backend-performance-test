import requests
import time
import concurrent.futures
import numpy as np

def send_message(url):
    try:
        start_time = time.time()
        response = requests.post(url, json={"content": "Hello, World!"}, timeout=5)
        end_time = time.time()
        return end_time - start_time, response.status_code
    except requests.RequestException as e:
        print(f"Error - URL: {url}, Exception: {str(e)}")
        return None, 500

def run_test(url, num_requests, concurrency):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(lambda _: send_message(url), range(num_requests)))
    
    latencies = [result[0] for result in results if result[0] is not None]
    error_rate = sum(1 for result in results if result[1] not in [200, 201]) / num_requests
    
    print(f"\nSummary for {url}:")
    print(f"Successful requests: {len(latencies)}")
    print(f"Failed requests: {num_requests - len(latencies)}")
    print(f"Error rate: {error_rate:.2%}")
    
    return latencies, error_rate

def main():
    num_requests = 10000
    concurrency = 75
    
    urls = {
        "Node.js": "http://nodejs-backend:3000/message",
        "Rust": "http://rust-backend:3001/message",
        "Go": "http://go-backend:3002/message"
    }
    
    print(f"Running tests with {num_requests} requests and concurrency of {concurrency}")
    
    for name, url in urls.items():
        print(f"\nTesting {name} backend at {url}")
        latencies, error_rate = run_test(url, num_requests, concurrency)
        avg_latency = np.mean(latencies) if latencies else float('nan')
        print(f"{name} - Avg Latency: {avg_latency:.4f}s, Error Rate: {error_rate:.2%}")

if __name__ == "__main__":
    main()