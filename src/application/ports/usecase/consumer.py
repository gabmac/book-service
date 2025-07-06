import json
from typing import Any, Dict


class ConsumerUsecase:
    def _convert_to_json(self, payload: bytes) -> Dict[str, Any]:
        dict_str = payload.decode("UTF-8")
        dict_json = json.loads(dict_str)
        return dict_json
