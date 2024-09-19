from uuid import uuid4 as uuid_generator
from kbrainsdk.validation.ingest import validate_ingest_status, validate_ingest_focused_chat
from kbrainsdk.apibase import APIBase

class Ingest(APIBase):

    def __init__(self, *args, **kwds):
        return super().__init__(*args, **kwds)


    def get_status(self, focused_chat_id):
        payload = {
            "focused_chat_id": focused_chat_id
        }

        validate_ingest_status(payload)

        path = f"/ingest/status/v2"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def ingest_focused_chat(
            self, 
            focused_chat_id:str,
            host:str, 
            site:str,                
            assertion_token:str|None=None,         
            client_secret:str|None=None,         
            client_id:str|None=None, 
            tenant_id:str|None=None, 
        ) -> str:

        operation_id = str(uuid_generator())

        payload = {
            "focused_chat_id": focused_chat_id,
            "host": host,
            "site": site,
            "operation_id": operation_id,
            "token": assertion_token,
            "client_secret": client_secret,
            "client_id": client_id,
            "tenant_id": tenant_id
        }

        validate_ingest_focused_chat(payload)

        path = f"/ingest/focused-chat/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response, operation_id