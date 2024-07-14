import requests
import time
import concurrent.futures
import matplotlib.pyplot as plt
import numpy as np

# Define the URLs for each backend
NODE_URL = "http://nodejs-backend:3000/message"
RUST_URL = "http://rust-backend:3001/message"
GO_URL = "http://go-backend:3002/message"

def send_message(url):
    """Send a POST request to the specified URL and return the response time"""
    start_time = time.time()
    response = requests.post(url, json={"content": "Hello, World!"})
    end_time = time.time()
    return end_time - start_time, response.status_code

def run_test(url, num_requests, concurrency):
    """Run a test with the specified number of requests and concurrency level"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(send_message, url) for _ in range(num_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    latencies = [result[0] for result in results if result[1] == 200]
    error_rate = sum(1 for result in results if result[1] != 200) / num_requests
    
    return latencies, error_rate

def plot_results(node_latencies, rust_latencies, go_latencies):
    """Plot the latency distribution for each backend"""
    plt.figure(figsize=(10, 6))
    plt.boxplot([node_latencies, rust_latencies, go_latencies], labels=['Node.js', 'Rust', 'Go'])
    plt.title('Latency Comparison')
    plt.ylabel('Latency (seconds)')
    plt.savefig('latency_comparison.png')

def main():
    num_requests = 1000
    concurrency = 50

    print(f"Running tests with {num_requests} requests and concurrency of {concurrency}")

    node_latencies, node_error_rate = run_test(NODE_URL, num_requests, concurrency)
    rust_latencies, rust_error_rate = run_test(RUST_URL, num_requests, concurrency)
    go_latencies, go_error_rate = run_test(GO_URL, num_requests, concurrency)

    print(f"Node.js - Avg Latency: {np.mean(node_latencies):.4f}s, Error Rate: {node_error_rate:.2%}")
    print(f"Rust - Avg Latency: {np.mean(rust_latencies):.4f}s, Error Rate: {rust_error_rate:.2%}")
    print(f"Go - Avg Latency: {np.mean(go_latencies):.4f}s, Error Rate: {go_error_rate:.2%}")

    plot_results(node_latencies, rust_latencies, go_latencies)

if __name__ == "__main__":
    main()