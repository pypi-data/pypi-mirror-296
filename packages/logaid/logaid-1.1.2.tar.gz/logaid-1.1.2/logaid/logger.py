import logging
import logging.handlers
import inspect
import os
from time import strftime
import builtins

def add_context_info(func,level=logging.INFO,filename=False,format=False,show=True):
    def wrapper(*args, **kwargs):
        [logging.root.removeHandler(handler) or handler.close() for handler in logging.root.handlers[:]]
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        if func_name == '<module>':
            func_name = 'None'
        co_filename = frame.f_code.co_filename.split('\\')[-1]
        lineno = frame.f_lineno
        handler_list =[]
        if filename:
            handler_list.append(logging.FileHandler(filename,encoding='utf-8'))
        if show:
            handler_list.append(logging.StreamHandler())

        if format:
            logging.basicConfig(level=level,
                                format=format,handlers=handler_list)
        else:
            if filename:
                logging.basicConfig(level=level,
                                    format=f'File "{co_filename}", line {lineno}, time %(asctime)s, func {func_name}, level %(levelname)s: %(message)s',
                                    handlers=handler_list)
            else:
                logging.basicConfig(level=level,
                                    format=f'File "{co_filename}", line {lineno}, func {func_name}, level %(levelname)s: %(message)s',
                                    handlers=handler_list)
        if func.__name__ == 'debug':
            args = (' '.join([f"\033[35m{i}\033[0m" if not filename else str(i) for i in args ]),)
        elif func.__name__ == 'info':
            args = (' '.join([f"\033[36m{i}\033[0m" if not filename else str(i)  for i in args]),)
        elif func.__name__ == 'warning':
            args = (' '.join([f"\033[33m{i}\033[0m" if not filename else str(i)  for i in args]),)
        elif func.__name__ == 'error':
            args = (' '.join([f"\033[34m{i}\033[0m" if not filename else str(i)  for i in args]),)
        elif func.__name__ == 'fatal':
            args = (' '.join([f"\033[31m{i}\033[0m" if not filename else str(i)  for i in args]),)
        return func(*args, **kwargs)
    return wrapper

debug = add_context_info(logging.debug)
info = add_context_info(logging.info)
warning = add_context_info(logging.warning)
error = add_context_info(logging.error)
fatal = add_context_info(logging.fatal)


def init(level='INFO',filename=False,save=False,format=False,show=True,print_pro=False):
    global debug,info,warning,error,fatal
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
    if save:
        path = os.path.dirname(os.getcwd() + '\\logs\\')  # 判断日志目录
        if not os.path.exists(path):
            os.makedirs(path)
        filename = strftime("logs\my_log_%Y_%m_%d_%H.log")

    debug = add_context_info(logging.debug, log_level,filename,format,show)
    info = add_context_info(logging.info, log_level,filename,format,show)
    warning = add_context_info(logging.warning, log_level,filename,format,show)
    error = add_context_info(logging.error, log_level,filename,format,show)
    fatal = add_context_info(logging.fatal, log_level,filename,format,show)
    if print_pro:
        builtins.print = add_context_info(logging.info)
