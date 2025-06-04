import os
import logging
from typing import Optional, Dict, Any, List

import requests
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from pydantic import Field

logger = logging.getLogger(__name__)


class ZhipuWebSearch(BaseTool):
    """Tool that queries Zhipu WebSearch API."""

    name: str = "web_search"
    description: str = "Use Zhipu's WebSearch API to search the internet."
    max_results: int = Field(5, description="maximum number of search results")
    api_key: str = Field(default_factory=lambda: os.getenv("ZHIPU_WEBSEARCH_API_KEY", ""))
    api_url: str = Field(default_factory=lambda: os.getenv(
        "ZHIPU_WEBSEARCH_API_URL",
        "https://open.bigmodel.cn/api/paas/v3/model-api/web_search",
    ))

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> List[Dict[str, Any]]:
        logger.info(f"Zhipu WebSearch query: {query}")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"query": query, "top_k": self.max_results}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # The API returns a 'data' field with search results
        return data.get("data", data)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> List[Dict[str, Any]]:
        return self._run(query)
