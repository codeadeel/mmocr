# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import communication_pb2 as communication__pb2


class mmocr_serviceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.inference = channel.unary_unary(
                '/mmocr_service/inference',
                request_serializer=communication__pb2.server_input.SerializeToString,
                response_deserializer=communication__pb2.server_output.FromString,
                )


class mmocr_serviceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def inference(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_mmocr_serviceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'inference': grpc.unary_unary_rpc_method_handler(
                    servicer.inference,
                    request_deserializer=communication__pb2.server_input.FromString,
                    response_serializer=communication__pb2.server_output.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mmocr_service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class mmocr_service(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def inference(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mmocr_service/inference',
            communication__pb2.server_input.SerializeToString,
            communication__pb2.server_output.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
