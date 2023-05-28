from datetime import date, datetime
from bson import ObjectId


def json_serialize_date(obj):
    if isinstance(obj, (date, datetime)):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    raise TypeError("The type %s not serializable." % type(obj))


def json_serialize_oid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("The type %s not serializable." % type(obj))