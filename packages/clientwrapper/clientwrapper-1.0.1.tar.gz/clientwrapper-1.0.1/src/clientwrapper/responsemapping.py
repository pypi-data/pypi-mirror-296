from typing import Dict, Any, List, Optional

from requests import Response

from .basicmapping import BasicMapping


class ResultMapping(BasicMapping):
    def __init__(self, data: Dict[str, Any], filter_keys: List[str] = None):
        data = data if (filter_keys is None or len(filter_keys) == 0) else {key: data.get(key, '') for key in
                                                                            filter_keys}
        super().__init__(data)


class ResponseMapping:

    def __init__(self, response: Response, nested_key: Optional[str] = None, filter_keys: Optional[List[str]] = None):
        self.response = response
        self.results: List[ResultMapping] = []
        response_json = response.json()
        if nested_key is None:
            self.results += [ResultMapping(response_json, filter_keys)]
        else:
            response_data = response_json[nested_key]
            if isinstance(response_data, dict):
                self.results += [ResultMapping(response_data, filter_keys)]
            elif isinstance(response_data, list):
                for result in response_data:
                    self.results += [ResultMapping(result, filter_keys)]
