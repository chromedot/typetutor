from typing import List, Dict, Optional
import asyncio
import json

class DataProcessor:
    def __init__(self, config: Dict[str, any]):
        self.config = config
        self._cache = {}
        self.status = "initialized"

    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        results = []
        for item in items:
            try:
                processed = await self._process_item(item)
                results.append({"status": "success", "data": processed})
            except Exception as e:
                results.append({"status": "error", "message": str(e)})
        return results

    async def _process_item(self, item: Dict) -> Optional[Dict]:
        if item['id'] in self._cache:
            return self._cache[item['id']]

        validated = self._validate(item)
        transformed = self._transform(validated)
        self._cache[item['id']] = transformed
        return transformed

    def _validate(self, data: Dict) -> Dict:
        required_fields = ['id', 'type', 'value']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        return data

    def _transform(self, data: Dict) -> Dict:
        return {
            **data,
            'timestamp': self._get_timestamp(),
            'normalized': data['value'].lower().strip()
        }

    @staticmethod
    def _get_timestamp() -> int:
        return int(time.time() * 1000)
