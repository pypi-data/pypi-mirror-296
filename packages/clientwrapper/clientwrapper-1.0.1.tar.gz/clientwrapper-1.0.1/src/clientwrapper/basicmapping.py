from collections.abc import Mapping

from typing import Dict, Any


class BasicMapping(Mapping):
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        super().__init__()

    def __len__(self):
        return len([key for key in self.data])

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        for value in self.data.keys():
            yield value

    def __contains__(self, value):
        return value in self.data.values()

    def __repr__(self):
        return str(self.data)
