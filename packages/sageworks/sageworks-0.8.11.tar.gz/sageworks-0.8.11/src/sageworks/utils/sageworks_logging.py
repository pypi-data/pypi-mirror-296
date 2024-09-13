import os
import sys
from collections import defaultdict
import time
import logging
import traceback
from contextlib import contextmanager

# Import the CloudWatchHandler
from sageworks.utils.cloudwatch_handler import CloudWatchHandler


class ThrottlingFilter(logging.Filter):
    def __init__(self, rate_seconds=60):
        super().__init__()
        self.rate_seconds = rate_seconds
        self.last_log_times = defaultdict(lambda: 0)

    def filter(self, record):
        # Get the message and last log time for this message
        message = str(record.msg)
        last_log_time = self.last_log_times[message]

        # Return True if this message should be logged (i.e. it's been long enough since the last time)
        current_time = time.time()
        if current_time - last_log_time > self.rate_seconds:
            self.last_log_times[message] = current_time
            return True

        # Filter out this message
        return False


# Define TRACE level
# Note: see https://docs.python.org/3/library/logging.html#logging-levels
TRACE_LEVEL_NUM = 15  # Between DEBUG and INFO
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


# Define IMPORTANT level
# Note: see https://docs.python.org/3/library/logging.html#logging-levels
IMPORTANT_LEVEL_NUM = 25  # Between INFO and WARNING
logging.addLevelName(IMPORTANT_LEVEL_NUM, "IMPORTANT")


def important(self, message, *args, **kws):
    if self.isEnabledFor(IMPORTANT_LEVEL_NUM):
        self._log(IMPORTANT_LEVEL_NUM, message, args, **kws)


# Define MONITOR level
# Note: see https://docs.python.org/3/library/logging.html#logging-levels
MONITOR_LEVEL_NUM = 35  # Between WARNING and ERROR
logging.addLevelName(MONITOR_LEVEL_NUM, "MONITOR")


def monitor(self, message, *args, **kws):
    if self.isEnabledFor(MONITOR_LEVEL_NUM):
        self._log(MONITOR_LEVEL_NUM, message, args, **kws)


# Add the trace, important, and monitor level to the logger
logging.Logger.trace = trace
logging.Logger.important = important
logging.Logger.monitor = monitor


# Define a ColoredFormatter
class ColoredFormatter(logging.Formatter):
    COLORS_DARK_THEME = {
        "DEBUG": "\x1b[38;5;60m",  # "DarkGrey"
        "TRACE": "\x1b[38;5;141m",  # LightPurple
        "INFO": "\x1b[38;5;69m",  # LightBlue
        "IMPORTANT": "\x1b[38;5;113m",  # LightGreen
        "WARNING": "\x1b[38;5;190m",  # DarkYellow
        "MONITOR": "\x1b[38;5;220m",  # LightPurple
        "ERROR": "\x1b[38;5;208m",  # Orange
        "CRITICAL": "\x1b[38;5;198m",  # Hot Pink
    }
    COLORS_LIGHT_THEME = {
        "DEBUG": "\x1b[38;5;21m",  # Blue
        "TRACE": "\x1b[38;5;91m",  # Purple
        "INFO": "\x1b[38;5;22m",  # Green
        "IMPORTANT": "\x1b[38;5;178m",  # Lime
        "WARNING": "\x1b[38;5;94m",  # DarkYellow
        "MONITOR": "\x1b[38;5;91m",  # Purple
        "ERROR": "\x1b[38;5;166m",  # Orange
        "CRITICAL": "\x1b[38;5;124m",  # Red
    }
    COLORS = COLORS_DARK_THEME

    RESET = "\x1b[0m"

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.RESET)}{log_message}{self.RESET}"


def logging_setup(color_logs=True):
    """Set up the logging for the application."""

    log = logging.getLogger("sageworks")

    # Check if logging is already set up
    if getattr(log, "_is_setup", False):
        return

    # Mark the logging setup as done
    log._is_setup = True

    # Turn off propagation to root logger
    log.propagate = False

    # Remove any existing handlers
    while log.handlers:
        log.removeHandler(log.handlers[0])

    # Setup new stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = (
        ColoredFormatter(
            "%(asctime)s (%(filename)s:%(lineno)d) %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        if color_logs
        else logging.Formatter(
            "%(asctime)s (%(filename)s:%(lineno)d) %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    # Setup logging level
    debug_env = os.getenv("SAGEWORKS_DEBUG", "False")
    if debug_env.lower() == "true":
        log.setLevel(logging.DEBUG)
        log.debug("Debugging enabled via SAGEWORKS_DEBUG environment variable.")
    else:
        log.setLevel(logging.INFO)
        # Note: Not using the ThrottlingFilter for now
        # throttle_filter = ThrottlingFilter(rate_seconds=5)
        # handler.addFilter(throttle_filter)

    # Suppress specific logger
    logging.getLogger("sagemaker.config").setLevel(logging.WARNING)

    # Add a CloudWatch handler
    try:
        cloudwatch = CloudWatchHandler()
        log.important("Adding CloudWatch logging handler...")
        log.important(f"Log Stream Name: {cloudwatch.log_stream_name}")
        cloudwatch.add_cloudwatch_handler(log)
        log.info("SageWorks Logging Setup Complete...")
    except Exception as e:
        log.error("Failed to add CloudWatch logging handler....")
        log.monitor("Failed to add CloudWatch logging handler....")
        log.exception(f"Exception details: {e}")


@contextmanager
def exception_log_forward(call_on_exception=None):
    """Context manager to log exceptions and optionally call a function on exception."""
    log = logging.getLogger("sageworks")
    try:
        yield
    except Exception as e:
        # Capture the stack trace as a list of frames
        tb = e.__traceback__
        # Convert the stack trace into a list of formatted strings
        stack_trace = traceback.format_exception(e.__class__, e, tb)
        # Find the frame where the context manager was entered
        cm_frame = traceback.extract_tb(tb)[0]
        # Filter out the context manager frame
        filtered_stack_trace = []
        for frame in traceback.extract_tb(tb):
            if frame != cm_frame:
                filtered_stack_trace.append(frame)
        # Format the filtered stack trace
        formatted_stack_trace = "".join(traceback.format_list(filtered_stack_trace))
        log_message = f"Exception:\n{formatted_stack_trace}{stack_trace[-1]}"
        log.critical(log_message)

        # Flush all handlers to ensure the exception messages are sent
        log.important("Flushing all log handlers...")
        for handler in log.handlers:
            handler.flush()

        # Call the provided function if it exists
        if callable(call_on_exception):
            return call_on_exception(e)
        else:
            # Raise the exception if no function was provided
            raise

    # Ensure all log handlers are flushed
    finally:
        log.important("Finally: Flushing all log handlers...")
        for handler in log.handlers:
            if hasattr(handler, "flush"):
                handler.flush()
        time.sleep(2)  # Give the logs a chance to flush


if __name__ == "__main__":
    # Uncomment to test the SAGEWORKS_DEBUG env variable
    # os.environ["SAGEWORKS_DEBUG"] = "True"

    logging_setup()
    my_log = logging.getLogger("sageworks")
    my_log.info("You should see me")
    my_log.debug("You should see me only if SAGEWORKS_DEBUG is True")
    logging.getLogger("sageworks").setLevel(logging.WARNING)
    my_log.info("You should NOT see me")
    my_log.warning("You should see this warning")

    # Test out ALL the colors
    logging.getLogger("sageworks").setLevel(logging.DEBUG)
    my_log.debug("This should be a muted color")
    my_log.trace("Trace color should stand out from debug")
    my_log.info("This should be a nice color")
    my_log.important("Important color should stand out from info")
    my_log.warning("This should be a color that attracts attention")
    my_log.monitor("This is a monitor message")
    my_log.error("This should be a bright color")
    my_log.critical("This should be an alert color")

    # Test the exception handler
    with exception_log_forward():
        raise ValueError("Testing the exception handler")
