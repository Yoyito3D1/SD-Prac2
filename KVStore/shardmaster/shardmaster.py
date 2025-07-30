import logging
import threading

from KVStore.tests.utils import KEYS_LOWER_THRESHOLD, KEYS_UPPER_THRESHOLD
from KVStore.protos.kv_store_pb2 import RedistributeRequest, ServerRequest
from KVStore.protos.kv_store_pb2_grpc import KVStoreStub
from KVStore.protos.kv_store_shardmaster_pb2_grpc import ShardMasterServicer
from KVStore.protos.kv_store_shardmaster_pb2 import *

# from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
logger = logging.getLogger(__name__)
import google.protobuf.empty_pb2 as google_dot_protobuf_dot_empty__pb2
import grpc
from multiprocessing import Manager, Lock

from typing import Dict, Tuple


class ShardMasterService:
    def join(self, server: str):
        pass

    def leave(self, server: str):
        pass

    def query(self, key: int) -> str:
        pass


def grpc_redistribute(source_server: str, destination_server: str, keys: Tuple[int, int]):
    redistribute_request = RedistributeRequest()
    redistribute_request.destination_server = destination_server
    redistribute_request.lower_val = keys[0]
    redistribute_request.upper_val = keys[1]
    print(f"Source server: {source_server}, Destination server: {destination_server}, Keys: {keys}")
    with grpc.insecure_channel(source_server) as channel:
        stub = KVStoreStub(channel)
        stub.Redistribute(redistribute_request)

    print(f"Redistributed keys: {keys} from {source_server} to {destination_server}")


class ShardMasterSimpleService(ShardMasterService):
    def __init__(self):
        self.manager = Manager()
        self.node_dict = self.manager.dict()
        self.servers = self.manager.list()
        self.lock = Lock()
        self.storage_service = KVStoreStub(grpc.insecure_channel("localhost:50051"))

    def show_server_ranges(self):
        for server in self.servers:
            range_start, range_end = self.node_dict.get(server, (None, None))
            print(f"Server: {server}, Range: ({range_start}, {range_end})")

    def join(self, server: str):
        with self.lock:
            if server not in self.servers:
                self.show_server_ranges()
                self.servers.append(server)
                self.recalculate_shards()
                self.redistribute_all_keys()  # Redistribuir todas las claves entre los servidores
                print(f"New Join ({server}), Servers -> {self.servers}")
                print(f"Shards -> {self.node_dict}")
                self.show_server_ranges()

    def leave(self, server: str):
        if server in self.servers:
            self.lock.acquire()
            try:
                self.servers.remove(server)
                del self.node_dict[server]
                if len(self.servers) >= 1:
                    self.recalculate_shards()
                    self.redistribute_all_keys()  # Redistribuir todas las claves entre los servidores
            finally:
                self.lock.release()
            print(f"New Leave ({server}), Servers -> {self.servers}")
            print(f"Shards -> {self.node_dict}")

    def recalculate_shards(self):
        total_servers = len(self.servers)
        total_keys = 100

        if total_servers == 0:
            return

        avg_keys_per_server = total_keys // total_servers
        remaining_keys = total_keys % total_servers

        lower_val = 0
        for i, server in enumerate(self.servers):
            keys_count = avg_keys_per_server + (1 if i < remaining_keys else 0)
            upper_val = lower_val + keys_count - 1
            self.node_dict[server] = (lower_val, upper_val)
            lower_val = upper_val + 1

    def query(self, key):
        for address in self.servers:
            print(f"Key: {str(key)} Range: {str(self.node_dict.get(address))} Server: {address}")
            if self.node_dict.get(address)[0] <= key <= self.node_dict.get(address)[1]:
                return address
        return None

    def redistribute_all_keys(self):
        if len(self.servers) == 0:
            return

        total_keys = 100
        num_servers = len(self.servers)
        avg_keys_per_server = total_keys // num_servers
        remaining_keys = total_keys % num_servers

        lower_val = 0
        for i, server in enumerate(self.servers):
            keys_count = avg_keys_per_server + (1 if i < remaining_keys else 0)
            upper_val = lower_val + keys_count - 1
            self.node_dict[server] = (lower_val, upper_val)
            lower_val = upper_val + 1

        for i in range(num_servers):
            server = self.servers[i]
            keys = (self.node_dict[server][0], self.node_dict[server][1])
            destination = self.servers[(i + 1) % num_servers]
            grpc_redistribute(server, destination, keys)


class ShardMasterServicer(ShardMasterServicer):
    def __init__(self, shard_master_service: ShardMasterService):
        self.shard_master_service = shard_master_service

    def Join(self, request: JoinRequest, context) -> google_dot_protobuf_dot_empty__pb2.Empty:
        self.shard_master_service.join(request.server)
        return google_dot_protobuf_dot_empty__pb2.Empty()

    def Leave(self, request: LeaveRequest, context) -> google_dot_protobuf_dot_empty__pb2.Empty:
        self.shard_master_service.leave(request.server)
        return google_dot_protobuf_dot_empty__pb2.Empty()

    def Query(self, request: QueryRequest, context) -> QueryResponse:
        response = self.shard_master_service.query(request.key)
        toReturn: QueryResponse = QueryResponse(server=response)
        if response == "":
            return QueryResponse(server=None)
        else:
            return toReturn
