#!/usr/bin/env python


class RetType:
    SUC = 0
    FAIL = 1
    NO = 2


def retry(retry_num, interval=5, check_ret=RetType.NO, ret_value_list=[True, ]):
    """
    A decorator which retry run a function util it run successfully.
    No exception raised means success if check_ret == RetType.NO.
    No exception raised and the return value in ret_value_list means success,
    if check_ret == RetType.SUC.
    No exception raised and the return value not in ret_value_list means success,
    if check_ret == RetType.FAIL.
    if the func return, it will return the origin func ret.
    """
    def _retry(func):
        def new_func(*args, **argkw):
            cur_num = 0
            while cur_num <= retry_num:
                cur_num += 1
                try:
                    ret = func(*args, **argkw)
                    if check_ret == RetType.SUC:
                        if ret in ret_value_list:
                            break
                    elif check_ret == RetType.FAIL:
                        if not ret in ret_value_list:
                            break
                    else:
                        break
                    time.sleep(interval)
                except Exception, e:
                    if cur_num > retry_num:
                        raise
                    else:
                        time.sleep(interval)
                        continue
            return ret
        return new_func
    return _retry
