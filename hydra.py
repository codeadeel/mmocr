#!/usr/bin/env python3

"""
OPENMMLAB's MMOCR INFERENCE SERVER
==================================

The following program is used to perform inference on the subject data
"""

# %%
# Importing Libraries
from mmocr.utils.ocr import MMOCR
import numpy as np
from PIL import Image
import json
import time
import sys
import argparse
import socket
from concurrent import futures
import grpc
import communication_pb2
import communication_pb2_grpc

# %%
# Inference Server Class
class mmocr_service(communication_pb2_grpc.mmocr_serviceServicer):
    def __init__(self, *args, **kwargs):
        """
        This method is used to initialize server class for MMOCR Model inference

        Method Input
        =============
        None

        Method Output
        ==============
        None
        """
        pass

    def __request_processor(self, inp_req):
        """
        This method is used to process input request to server

        Method Input
        =============
        inp_req : Request object generated by GRPC

        Method Output
        ==============
        Input data for inference as Numpy array along with client id
                            ( Input Numpy data, Client ID )
        """
        ret_dat = np.frombuffer(inp_req.imgs, dtype=inp_req.data_type).reshape(inp_req.batch, inp_req.width, inp_req.height, inp_req.channel)
        print(f'Input Batch Shape: {ret_dat.shape}')
        ret_dat = [i for i in ret_dat]
        return ret_dat, inp_req.client_id
    
    def __output_processor(self, inf_out):
        """
        This method is used to process output data after inference

        Method Input
        =============
        inf_out : Output Result Dictionary

        Method Output
        ==============
        Output object after inference
        """
        return communication_pb2.server_output(
            results_dictionary = json.dumps(inf_out).encode()
        )
    
    def inference(self, request, context):
        """
        This method is used to handle requests & inference outputs

        Method Input
        =============
        request : GPRC generated input request object
        context : GRPC generated API context

        Method Output
        ==============
        None
        """
        inp_data, client_id = self.__request_processor(request)
        print(f'Client ID: {client_id}')
        st = time.time()
        out_simple, out_dict, res_img = seg_ocr.readtext(inp_data, print_result=False, imshow=True)
        print('Output: ', out_simple)
        """
        out_simple -> Simplified Output Dictionary
        out_dict -> Comprehensive Output Dictionary
        res_img -> Generated Infered Image from MMOCR
        """
        ed = time.time() - st
        print(f'Inference Time: {ed}')
        print('---------------------------------------------\n')
        return self.__output_processor(out_dict)

# %%
# Server Execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'OpenMMLab\'s MMOCR Inference Server.')
    parser.add_argument('-ip', '--server_ip', type = str, help = 'IP Address to Start GRPC Server', default = '[::]:4321')
    parser.add_argument('-msg', '--msg_len', type = int, help = 'Message Length Subject to Communication by GRPC', default = 1000000000)
    parser.add_argument('-wrk', '--workers', type = int, help = 'Number of Workers to Used by GRPC', default = 1)
    args = vars(parser.parse_args())
    print("""
    ===================================================
    | OpenMMLab's MMOCR Inference GRPC Server Details |
    ===================================================
    """)
    seg_ocr = MMOCR('PANet_IC15')
    duip, msle, wrke = args['server_ip'], args['msg_len'], args['workers']
    print(f'Inference IP: {duip}')
    print(f'Server IP: {socket.gethostbyname(socket.gethostname())}')
    print(f'Maximum Server Communication Message Length: {msle}')
    print(f'Number of Worker Allowed for GRPC Server: {wrke}')
    print('---------------------------------------------')
    print('>>>>> Press Ctrl+C To Shutdown Server')
    print("""
    =============================================
    |              Inference Logs               |
    =============================================
    """)
    server_opts = [('grpc.max_send_message_length', args['msg_len']), ('grpc.max_receive_message_length', args['msg_len'])]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = args['workers']), options = server_opts)
    communication_pb2_grpc.add_mmocr_serviceServicer_to_server(mmocr_service(), server)
    server.add_insecure_port(args['server_ip'])
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("""
    =============================================
    |               Shutting Down               |
    =============================================
    """)
        sys.exit(0)
        