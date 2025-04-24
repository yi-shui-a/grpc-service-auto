from enum import Enum, unique


@unique
class FileEnum(Enum):
    ATOM_SERIVCE_JSON = "atom_service_json"
    CPP = "cpp"
    HPP = "hpp"
    CPP_CMAKE = "cpp_cmake"

    SERVER_JSON = "server_json"

    GRPC_SERVER = "grpc_server"
    GRPC_CLIENT = "grpc_client"
    GRPC_ATOM_SERVICE = "grpc_atom_service"
    DDS = "dds"
    IDL = "idl"
    DDS_SERVER = "dds_server"
    DDS_CLIENT = "dds_client"
    DDS_ATOM_SERVICE = "dds_atom_service"
    # DDS_TOPIC = "dds_topic"
    # DDS_TOPIC_H = "dds_topic_h"
