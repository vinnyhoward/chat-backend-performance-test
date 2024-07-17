import requests
import time
import concurrent.futures
import numpy as np
import psutil
import matplotlib.pyplot as plt
from collections import defaultdict

def send_message(url, payload_size='small'):
    payloads = {
        'small': {'content': 'Hello, World!'},
        'medium': {'content': 'A' * 1000},
        'large': {'content': 'A' * 10000}
    }
    try:
        start_time = time.time()
        response = requests.post(url, json=payloads[payload_size], timeout=5)
        end_time = time.time()
        return end_time - start_time, response.status_code
    except requests.RequestException as e:
        print(f"Error - URL: {url}, Exception: {str(e)}")
        return None, 500

def run_test(url, num_requests, concurrency, payload_size='small'):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(lambda _: send_message(url, payload_size), range(num_requests)))
    
    latencies = [result[0] for result in results if result[0] is not None]
    error_rate = sum(1 for result in results if result[1] not in [200, 201]) / num_requests
    
    return latencies, error_rate

def run_scalability_test(url, max_concurrency=1000, step=50, requests_per_step=1000):
    concurrences = list(range(step, max_concurrency + step, step))
    avg_latencies = []
    error_rates = []
    
    for concurrency in concurrences:
        print(f"Testing with concurrency: {concurrency}")
        latencies, error_rate = run_test(url, requests_per_step, concurrency)
        avg_latencies.append(np.mean(latencies))
        error_rates.append(error_rate)
    
    return concurrences, avg_latencies, error_rates

def run_throughput_test(url, duration=60, concurrency=100):
    start_time = time.time()
    request_count = 0
    latencies = []
    
    while time.time() - start_time < duration:
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            batch_results = list(executor.map(lambda _: send_message(url), range(concurrency)))
        
        request_count += concurrency
        latencies.extend([result[0] for result in batch_results if result[0] is not None])
    
    throughput = request_count / duration
    avg_latency = np.mean(latencies)
    return throughput, avg_latency

def monitor_resources(duration=60):
    start_time = time.time()
    cpu_percents = []
    mem_percents = []
    
    while time.time() - start_time < duration:
        cpu_percents.append(psutil.cpu_percent())
        mem_percents.append(psutil.virtual_memory().percent)
        time.sleep(1)
    
    return np.mean(cpu_percents), np.mean(mem_percents)

def main():
    urls = {
        "Node.js": "http://nodejs-backend:3000/message",
        "Rust": "http://rust-backend:3001/message",
        "Go": "http://go-backend:3002/message"
    }
    
    # Scalability Test
    scalability_results = defaultdict(list)
    for name, url in urls.items():
        print(f"\nRunning scalability test for {name}")
        concurrencies, avg_latencies, error_rates = run_scalability_test(url)
        scalability_results[name] = (concurrencies, avg_latencies, error_rates)
    
    # Throughput Test
    print("\nRunning throughput test")
    throughput_results = {}
    for name, url in urls.items():
        print(f"Testing {name}")
        throughput, avg_latency = run_throughput_test(url)
        throughput_results[name] = (throughput, avg_latency)
    
    # Resource Utilization Test
    print("\nRunning resource utilization test")
    resource_results = {}
    for name, url in urls.items():
        print(f"Testing {name}")
        cpu_percent, mem_percent = monitor_resources()
        resource_results[name] = (cpu_percent, mem_percent)
    
    # Plot results
    plot_scalability_results(scalability_results)
    plot_throughput_results(throughput_results)
    plot_resource_results(resource_results)

def plot_scalability_results(results):
    plt.figure(figsize=(10, 6))
    for name, (concurrencies, avg_latencies, error_rates) in results.items():
        plt.plot(concurrencies, avg_latencies, label=f"{name} Latency")
    plt.xlabel('Concurrency')
    plt.ylabel('Average Latency (s)')
    plt.title('Scalability Test: Latency vs Concurrency')
    plt.legend()
    plt.savefig('scalability_test.png')
    plt.close()

def plot_throughput_results(results):
    names = list(results.keys())
    throughputs = [result[0] for result in results.values()]
    latencies = [result[1] for result in results.values()]
    
    x = np.arange(len(names))
    width = 0.35
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    
    rects1 = ax1.bar(x - width/2, throughputs, width, label='Throughput', color='b')
    rects2 = ax2.bar(x + width/2, latencies, width, label='Latency', color='r')
    
    ax1.set_xlabel('Backend')
    ax1.set_ylabel('Throughput (requests/s)')
    ax2.set_ylabel('Average Latency (s)')
    plt.title('Throughput Test: Throughput and Latency')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names)
    
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('throughput_test.png')
    plt.close()

def plot_resource_results(results):
    names = list(results.keys())
    cpu_percentages = [result[0] for result in results.values()]
    mem_percentages = [result[1] for result in results.values()]
    
    x = np.arange(len(names))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, cpu_percentages, width, label='CPU Usage', color='g')
    rects2 = ax.bar(x + width/2, mem_percentages, width, label='Memory Usage', color='y')
    
    ax.set_ylabel('Usage (%)')
    ax.set_title('Resource Utilization')
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('resource_utilization.png')
    plt.close()

if __name__ == "__main__":
    main()