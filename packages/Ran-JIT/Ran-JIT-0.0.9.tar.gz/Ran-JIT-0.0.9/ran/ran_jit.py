import numba
import numpy as np
import inspect
import os
import psutil
import platform
import requests
import requests_cache
import httpx
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Cache for storing results of process_chunk
cache = {}

# Create a session for connection pooling
session = requests.Session()

@numba.njit
def chunk_data(data, chunk_size):
    """
    Splits data into chunks of specified size.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def process_chunk(chunk):
    """
    Process a chunk of data. This function should contain the actual computation logic.
    Uses manual caching to avoid reprocessing the same chunk multiple times.
    """
    # Convert chunk to a tuple so it can be used as a key in the cache
    chunk_key = tuple(chunk)
    if chunk_key in cache:
        return cache[chunk_key]
    
    result = sum(chunk)  # Example operation
    
    # Store the result in the cache
    cache[chunk_key] = result
    return result

def threaded_processing(data, chunk_size=100, max_workers=4):
    """
    Process data in parallel using threads, by splitting the data into chunks.
    """
    data = np.asarray(data)  # Ensure data is a NumPy array
    chunks = list(chunk_data(data, chunk_size))  # JIT-compiled function
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_chunk, chunks))
    return results

### Network Boost Functionality ###

def setup_network_boost():
    """
    Set up various techniques for boosting API request performance.
    """
    setup_requests_cache()
    setup_retry_strategy()
    print("RAN LIB : Network boost setup complete.")

### Technique 1: Connection Pooling with requests.Session
def fetch_with_session(url):
    """
    Fetch data using connection pooling for faster repeated requests.
    """
    response = session.get(url)
    return response.text

### Technique 2: HTTP/2 Support with httpx
def fetch_http2(url):
    """
    Fetch data using HTTP/2 for faster multiplexed connections.
    """
    with httpx.Client(http2=True) as client:
        response = client.get(url)
        return response.text

### Technique 3: Caching API Responses (requests_cache)
def setup_requests_cache():
    """
    Set up caching of API responses to avoid redundant requests.
    """
    requests_cache.install_cache('api_cache', expire_after=300)  # Cache for 5 minutes
    print("RAN LIB : API response caching enabled.")

def fetch_with_cache(url):
    """
    Fetch data using the cache if available.
    """
    response = session.get(url)
    return response.text

### Technique 4: Retry with Exponential Backoff
def setup_retry_strategy():
    """
    Set up a retry strategy with exponential backoff for failed API requests.
    """
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    print("RAN LIB : Retry strategy with exponential backoff enabled.")

def fetch_with_retry(url):
    """
    Fetch data with retries for better reliability.
    """
    response = session.get(url)
    return response.text

### Technique 5: GZIP Compression
def fetch_with_gzip(url):
    """
    Fetch data with GZIP compression enabled for faster response times.
    """
    headers = {'Accept-Encoding': 'gzip'}
    response = session.get(url, headers=headers)
    return response.content


### JIT Application and Optimization ###

def apply_jit_to_all_functions(module_globals):
    """
    Apply JIT compilation to user-defined functions selectively, only if they benefit from JIT.
    """
    for name, obj in module_globals.items():
        if inspect.isfunction(obj) and name != 'apply_jit_to_all_functions':
            if name in ['optimize_system_resources', 'threaded_processing', 'setup_network_boost']:
                print(f"RAN LIB : Skipping JIT for {name} as it uses unsupported constructs.")
                continue

            try:
                source_code = inspect.getsource(obj)
                num_loops = source_code.count('for ') + source_code.count('while ')
                
                # Apply JIT if the function has loops or numpy operations
                if num_loops > 0 or 'np.' in source_code:
                    print(f"RAN LIB : JIT applied to {name}.")
                    module_globals[name] = numba.njit(obj, cache=True)
                else:
                    print(f"RAN LIB : Skipping JIT for {name} due to low complexity.")
            except Exception as e:
                print(f"RAN LIB : Skipping JIT for {name}: {e}")

### System Resource Optimization ###

def optimize_system_resources():
    """
    Adjusts system resources to give the process more priority, 
    potentially improving performance for CPU-bound tasks.
    """
    p = psutil.Process(os.getpid())
    system_platform = platform.system()

    try:
        if system_platform == "Windows":
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            print("RAN LIB : Process priority set to high (Windows).")
        else:
            p.nice(-10)  # Unix systems: -20 is highest priority, 19 is lowest
            print("RAN LIB : Process priority increased (Unix).")
    except AttributeError:
        print("RAN LIB : Unable to set high priority, feature not supported.")
    except psutil.AccessDenied:
        print("RAN LIB : Permission denied. Unable to change process priority. Try running as an administrator.")
    except Exception as e:
        print(f"RAN LIB : Failed to optimize system resources: {e}")

### Main function to trigger JIT application, resource optimization, and network boost ###
def ran():
    """
    Function to trigger JIT application, system resource optimization, and network boost.
    """
    apply_jit_to_all_functions(globals())
    optimize_system_resources()
    setup_network_boost()  # Automatically boost network performance
