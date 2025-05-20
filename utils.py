import contextlib
import os

@contextlib.contextmanager
def silence_c_stderr():
    """Context manager to silence stderr at the file descriptor level, works for C extensions too."""
    # Save original stderr fd
    original_stderr_fd = os.dup(2)
    # Create a null device and redirect stderr to it
    null_fd = os.open(os.devnull, os.O_RDWR)
    os.dup2(null_fd, 2)
    try:
        yield  # Allow code to run with stderr redirected
    finally:
        # Restore original stderr
        os.dup2(original_stderr_fd, 2)
        os.close(null_fd)
        os.close(original_stderr_fd)