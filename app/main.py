from modules.utils.util_log import info
from modules.data_preparation import get_data

if __name__ == "__main__":
    log = info
    if log:
        log(f'blah blah blah')
    print('this is main')
    data = get_data(log)
