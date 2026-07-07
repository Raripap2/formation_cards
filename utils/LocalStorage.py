import threading

_local_storage = threading.local()

def set_user_id(user_id):
    _local_storage.user_id = user_id

def get_user_id():
    return getattr(_local_storage, "user_id", None)