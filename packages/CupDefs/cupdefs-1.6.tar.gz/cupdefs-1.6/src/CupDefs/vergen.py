import datetime
import os
import hashlib
from . import vars
from . import utils

_TODAY: None | datetime.datetime = None
_DAYS = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 303, 334, 365]
_FILES: None | list[str] = None


def init_vergen() -> bool:
    global _TODAY, _FILES
    if _TODAY is None:
        _TODAY = datetime.datetime.now(datetime.timezone.utc)
        _FILES = []
        count = 0
        for root, dirs, files in os.walk(vars.VERGEN_HASH_PATH):
            for file in files:
                _FILES.append(os.path.join(root, file))
                count += 1
                if count >= vars.VERGEN_FILE_LIMIT:
                    return False
    return True


def generate() -> str | None:
    if _TODAY:
        num = 365 * (_TODAY.year - 2020) - 31 + _DAYS[(_TODAY.month - 1)] + _TODAY.day
        h = b''
        for path in _FILES:
            with open(path, 'rb') as buf:
                h += hashlib.md5(buf.read()).digest()
        return str(num) + hashlib.shake_256(h).hexdigest(vars.VERGEN_HASH_SIZE)
    else:
        if vars.PRINT_CUPDEFS_ERROR:
            utils.perror('Генератор номера не инициализирован')
