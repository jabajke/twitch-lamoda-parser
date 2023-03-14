from datetime import datetime


def add_created_at(var):
    if isinstance(var, list):
        var = [dict(item, created_at=datetime.utcnow()) for item in var]
    else:
        var.update(dict(created_at=datetime.utcnow()))
    return var
