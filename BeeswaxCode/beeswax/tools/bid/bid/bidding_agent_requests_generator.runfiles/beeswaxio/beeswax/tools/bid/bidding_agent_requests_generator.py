# Copyright 2017, BeeswaxIO Corporation

'''
Beeswax Bid Requests Generator.

Generate Beeswax bid http requests to a designated endpoint
with headers used in the biddding service and body generated from
the specified input file. Output the http responses to a file
if specified.
'''

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
import sys

from google.protobuf import text_format
from google.protobuf.message import DecodeError
from google.protobuf.text_format import ParseError
import requests

from beeswax.bid.request_pb2 import BidAgentRequest, BidAgentResponse


logger = logging.getLogger('beeswax.bid_request_generator')


ITEM_DELIMITER = '==='


_HTTP_TIMEOUT_S = 500.1


_LOG_LEVEL_NAMES = ['error', 'info', 'debug']


def parse_command_line():
    parser = ArgumentParser('Beeswax Bid Agent Requests Generator', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('path_to_requests_file',
                        help='Path to bid requests input ASCII format file.')
    parser.add_argument('bid_endpoint', help='Bid endpoint.')
    parser.add_argument('--path-to-responses-file',
                        help='Path to bid responses output file. '
                        'will skip writing response if not present')
    parser.add_argument('--header-secret', help='Authentication secret in request header')
    parser.add_argument('--log-level', default='info', choices=_LOG_LEVEL_NAMES)
    return parser.parse_args()


def _request_text_generator(requests_input_file):

    '''Generate bid requests in ASCII from input file'''

    while True:
        request_text_buffer = []
        for line in requests_input_file:
            if line.startswith(ITEM_DELIMITER):
                break
            request_text_buffer.append(line)
        if not request_text_buffer:
            break
        yield ''.join(request_text_buffer)


def _write_response(responses_output_file, response_message):

    '''Write response_info to responses_output_file if responses_output_file is not None'''

    if responses_output_file:
        responses_output_file.write('{}\n'.format(response_message))
        responses_output_file.write('{}\n'.format(ITEM_DELIMITER))


def _get_response_message(response):

    '''Return response info from http response'''

    response_msg = '''<Status> [{}] {}
<Response headers>
{}
'''.format(response.status_code, response.reason, response.headers)

    if response.status_code != 200:
        return response_msg

    try:
        bid_response = BidAgentResponse.FromString(response.content)
    except DecodeError:
        # re-raise to caller (main())
        raise

    return '{}\n<Bid Agent Response>\n{}'.format(response_msg, bid_response)


def main():
    opts = parse_command_line()
    # logger.setLevel(logging._levelNames[opts.log_level.upper()])
    logger.addHandler(logging.StreamHandler())

    logger.info('Endpoint: {}'.format(opts.bid_endpoint))

    headers = {
        'Content-type': 'application/x-protobuf',
    }
    if opts.header_secret:
        headers['beeswax-auth-secret'] = opts.header_secret

    try:
        input_request_file = open(opts.path_to_requests_file, 'r')
    except (IOError, OSError) as exc:
        logger.error('Could not open bid agent requests input file: {}'.format(exc))
        return -1

    output_file = None
    if opts.path_to_responses_file:
        try:
            output_file = open(opts.path_to_responses_file, 'w')
        except (IOError, OSError) as exc:
            logger.error('Could not open bid agent responses output file: {}'.format(exc))
            return -1

    try:
        session = requests.Session()
        session.headers.update(headers)

        success_count = 0
        failure_count = 0

        for request_text in _request_text_generator(input_request_file):
            request_proto = BidAgentRequest()

            try:
                text_format.Parse(request_text, request_proto)
            except ParseError as exc:
                msg = 'Could not parse bid agent request: {}. \nRequest: {}'.format(exc, request_text)
                logger.error(msg)
                # Intentionally write errors into output file so that (1) responses (errors) will
                # be aligned with requests and (2) user can do analysis in the output file.
                _write_response(output_file, msg)
                failure_count += 1
                continue

            try:
                logger.debug('Sending request: {}'.format(request_proto))
                response = session.post(opts.bid_endpoint,
                                        data=request_proto.SerializeToString(),
                                        timeout=_HTTP_TIMEOUT_S)
            except Exception as exc:
                msg = 'Error in sending http request: {}'.format(exc)
                logger.error(msg)
                # Intentionally write errors into output file.
                _write_response(output_file, msg)
                failure_count += 1
                continue

            try:
                response_message = _get_response_message(response)
            except DecodeError as exc:
                msg = 'Failed to deserialize response body: {}'.format(exc)
                logger.error(msg)
                # Intentionally write errors into output file.
                _write_response(output_file, msg)
                failure_count += 1
                continue

            _write_response(output_file, response_message)
            success_count += 1
            logger.debug('Successfully processed request: {}'.format(request_proto))

        input_request_file.close()
    finally:
        if output_file:
            output_file.close()

        logger.info('Finished processing all requests. Success count: {}, failure count: {}'
                    .format(success_count, failure_count))

    return 0


if __name__ == '__main__':
    sys.exit(main())
