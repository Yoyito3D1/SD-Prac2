import multiprocessing
import time
import random
from typing import Dict, Union, List
import logging
import grpc
from KVStore.protos.kv_store_pb2 import *
from KVStore.protos.kv_store_pb2_grpc import KVStoreServicer, KVStoreStub
import google.protobuf.empty_pb2 as google_dot_protobuf_dot_empty__pb2
from KVStore.protos.kv_store_shardmaster_pb2 import Role
from multiprocessing import Manager

EVENTUAL_CONSISTENCY_INTERVAL: int = 2

logger = logging.getLogger("KVStore")

from typing import Dict, Optional


class KVStorageService:

    def __init__(self):
        pass

    def get(self, key: int) -> str:
        pass

    def l_pop(self, key: int) -> str:
        pass

    def r_pop(self, key: int) -> str:
        pass

    def put(self, key: int, value: str):
        pass

    def append(self, key: int, value: str):
        pass

    def redistribute(self, destination_server: str, lower_val: int, upper_val: int):
        pass

    def transfer(self, keys_values: list):
        pass


class KVStorageSimpleService(KVStorageService):
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.data: Dict[int, str] = self.manager.dict()

    def get(self, key: int) -> Union[str, None]:
        return self.data.get(key, None)  # retornamos un none si no hay key o el valor de la key

    def l_pop(self, key: int) -> Union[str, None]:
        value = self.data.get(key)
        if value is not None:  # si valor existe
            if len(value) > 0:  # si valor es mas grande que 0
                popped_char = value[0]  # cogemos el caracter de mas a la izquierda
                self.data[key] = value[1:]  # guardamos el string sin el primer caracter
                return popped_char  # retornamos el primer char
            elif len(value) == 0:
                self.data[key] = ""  # si esta vacia se guarda un empty string
                return self.data[key]
        return None

    def r_pop(self, key: int) -> Union[str, None]:
        value = self.data.get(key)
        if value is not None:
            if len(value) > 0:
                popped_char = value[-1]  # hacemos lo mismo pero ahora desde la derecha
                self.data[key] = value[:-1]
                return popped_char
            elif len(value) == 0:
                self.data[key] = ""
                return self.data[key]
        return None

    def put(self, key: int, value: str):
        self.data[key] = value  # guardamos el valor en key

    def append(self, key: int, value: str):
        current_value = self.data.get(key)
        if current_value is not None:           # si hay valor
            self.data[key] = current_value + value  #se le añade el nuevo valor al final
        else:
            self.data[key] = value

    def redistribute(self, destination_server: str, lower_val: int, upper_val: int):
        keys_to_transfer = []
        remaining_data = {}

        for key, value in self.data.items():
            if lower_val <= key <= upper_val: # si la key esta en el rango
                keys_to_transfer.append(KeyValue(key=key, value=value)) # se añade a la lista de keys a transferir
            else:
                remaining_data[key] = value

        self.data = remaining_data

        if keys_to_transfer:
            stub = KVStoreStub(grpc.insecure_channel(destination_server))
            stub.Transfer(TransferRequest(keys_values=keys_to_transfer)) # se llama a la funcion transfer del servidor destino

    def transfer(self, keys_values: List[KeyValue]):
        for key_value in keys_values: # se añaden las keys y valores a la lista de keys y valores
            self.data[key_value.key] = key_value.value


class KVStorageServicer(KVStoreServicer):

    def __init__(self, service: KVStorageService):
        self.storage_service = service

    def Get(self, request: GetRequest, context) -> GetResponse:
        response = GetResponse(value=self.storage_service.get(request.key))
        if response.value is None or response.value == "":
            response = GetResponse(value=None)
        else:
            response = GetResponse(value=response.value)

        return response

    def LPop(self, request: GetRequest, context) -> GetResponse:
        response = GetResponse(value=self.storage_service.l_pop(request.key))
        if response.value is None or response.value == "":
            response = GetResponse(value=None)
        else:
            response = GetResponse(value=response.value)

        return response

    def RPop(self, request: GetRequest, context) -> GetResponse:
        response = GetResponse(value=self.storage_service.r_pop(request.key))
        if response.value is None or response.value == "":
            response = GetResponse(value=None)
        else:
            response = GetResponse(value=response.value)
        return response

    def Put(self, request: PutRequest, context) -> google_dot_protobuf_dot_empty__pb2.Empty:
        self.storage_service.put(request.key, request.value)
        return google_dot_protobuf_dot_empty__pb2.Empty()

    def Append(self, request: AppendRequest, context) -> google_dot_protobuf_dot_empty__pb2.Empty:
        self.storage_service.append(request.key, request.value)
        return google_dot_protobuf_dot_empty__pb2.Empty()

    def Redistribute(self, request: RedistributeRequest, context) -> google_dot_protobuf_dot_empty__pb2.Empty:
        self.storage_service.redistribute(request.destination_server, request.lower_val, request.upper_val)
        return google_dot_protobuf_dot_empty__pb2.Empty()

    def Transfer(self, request: TransferRequest, context) -> google_dot_protobuf_dot_empty__pb2.Empty:
        self.storage_service.transfer(request.keys_values)
        return google_dot_protobuf_dot_empty__pb2.Empty()
