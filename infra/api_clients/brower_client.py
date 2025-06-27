#
# from infra.http.request_handler import RequestHandler
#
#
# class BrowseClient:
#     def __init__(self, request_handler: RequestHandler):
#         self.request_handler = request_handler
#
#     def get_categories(self, locale=None, limit=None, offset=None):
#         params = {k: v for k, v in {"locale": locale, "limit": limit, "offset": offset}.items() if v is not None}
#         return self.request_handler.get("/browse/categories", params=params or None)
