# infra/api_clients/search_client.py
from infra.http.request_handler import RequestHandler


class SearchClient:
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler

    def search(self, q: str, types: list[str], market: str | None = None,
               limit: int | None = None, offset: int | None = None,
               include_external: str | None = None):
        params = {"q": q, "type": ",".join(types)}
        if market: params["market"] = market
        if limit is not None: params["limit"] = limit
        if offset is not None: params["offset"] = offset
        if include_external: params["include_external"] = include_external

        return self.request_handler.get("/search", params=params)
