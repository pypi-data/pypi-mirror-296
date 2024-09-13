import logging
import inspect
def add_context_info(func):
    def wrapper(*args, **kwargs):
        [logging.root.removeHandler(handler) or handler.close() for handler in logging.root.handlers[:]]
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        if func_name == '<module>':
            func_name = 'None'
        co_filename = frame.f_code.co_filename.split('\\')[-1]
        lineno = frame.f_lineno
        logging.basicConfig(level=logging.INFO,
                            format=f'File "{co_filename}", line {lineno}, func {func_name}, level %(levelname)s: %(message)s')
        if func.__name__ == 'debug':
            args = (' '.join([f"\033[35m{i}\033[0m" for i in args]),)
        elif func.__name__ == 'info':
            args = (' '.join([f"\033[36m{i}\033[0m" for i in args]),)
        elif func.__name__ == 'warning':
            args = (' '.join([f"\033[33m{i}\033[0m" for i in args]),)
        elif func.__name__ == 'error':
            args = (' '.join([f"\033[34m{i}\033[0m" for i in args]),)
        elif func.__name__ == 'fatal':
            args = (' '.join([f"\033[31m{i}\033[0m" for i in args]),)
        return func(*args, **kwargs)
    return wrapper

debug = add_context_info(logging.debug)
info = add_context_info(logging.info)
warning = add_context_info(logging.warning)
error = add_context_info(logging.error)
fatal = add_context_info(logging.fatal)


def init(level='INFO'):
    if level == 'DEBUG':
        log_level = logging.DEBUG
    elif level == 'INFO':
        log_level = logging.INFO
    elif level == 'WARN':
        log_level = logging.WARN
    elif level == 'WARNING':
        log_level = logging.WARNING
    elif level == 'ERROR':
        log_level = logging.ERROR
    elif level == 'FATAL':
        log_level = logging.FATAL
    elif level == 'CRITICAL':
        log_level = logging.CRITICAL
    else:
        log_level = logging.INFO
    [logging.root.removeHandler(handler) or handler.close() for handler in logging.root.handlers[:]]
    frame = inspect.currentframe().f_back
    func_name = frame.f_code.co_name
    if func_name == '<module>':
        func_name = 'None'
    co_filename = frame.f_code.co_filename.split('\\')[-1]
    lineno = frame.f_lineno
    logging.basicConfig(level=log_level,format=f'File "{co_filename}", line {lineno}, func {func_name}, level %(levelname)s: %(message)s')