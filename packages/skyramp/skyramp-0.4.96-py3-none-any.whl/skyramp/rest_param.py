"""
Contains helpers for interacting with Skyramp rest param.
"""
class _RestParam:
    def __init__(self, name: str, in_: str, value=None, type_=None, filepath=None):
        self.name = name
        self.in_ = in_
        self.type_ = type_
        self.value = value
        self.filepath = filepath

    def to_json(self):
        """
        Convert the object to a JSON string.
        """
        ret = {
            "name": self.name,
            "in": self.in_,
        }

        if self.value is not None:
            ret["value"] = self.value
        if self.filepath is not None and self.filepath != "":
            ret["filepath"] = self.filepath

        return ret
