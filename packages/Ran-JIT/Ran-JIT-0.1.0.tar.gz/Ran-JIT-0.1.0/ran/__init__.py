from .ran_jit import (
    apply_jit_to_all_functions, 
    optimize_system_resources, 
    setup_network_boost,
    fetch_with_session, 
    fetch_with_retry, 
    fetch_with_gzip, 
    fetch_http2, 
    # fetch_with_threading,  # Comment this out if not available
    # run_async_requests    # Comment this out if not available
)

# Automatically apply JIT to all functions in the module's global scope
apply_jit_to_all_functions(globals())

# Optimize system resources for the current process
optimize_system_resources()

# Setup network optimizations (caching, retry strategy, etc.)
setup_network_boost()

# Export the main functions for external use
__all__ = [
    'fetch_with_session', 
    'fetch_with_retry', 
    'fetch_with_gzip', 
    'fetch_http2', 
    # 'fetch_with_threading',  # Comment this out if not available
    # 'run_async_requests'    # Comment this out if not available
]
