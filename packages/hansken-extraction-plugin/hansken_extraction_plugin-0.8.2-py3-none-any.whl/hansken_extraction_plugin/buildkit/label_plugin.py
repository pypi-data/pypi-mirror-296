"""Contains a cmd entry point to create a plugin docker image with plugin info labels."""
import argparse
import sys
from typing import Tuple, Union
import uuid

from google.protobuf import empty_pb2
import grpc

from hansken_extraction_plugin.api.plugin_info import PluginInfo
from hansken_extraction_plugin.buildkit._build import _log, _log_error, _main, _run
from hansken_extraction_plugin.buildkit.build_utils import _plugin_info_to_labels
from hansken_extraction_plugin.framework import ExtractionPluginService_pb2_grpc
from hansken_extraction_plugin.runtime import unpack
from hansken_extraction_plugin.test_framework.validator import find_free_port


description = ('This is a utility to add labels to an extraction plugin image. Labeling a plugin is required for\n'
               'Hansken to detect extraction plugins in a plugin image registry. To label a plugin, first build the\n'
               'plugin image, for example by using one of the following commands:\n'
               '    docker build . -t my_plugin\n'
               '    docker build . -t my_plugin --build-arg https_proxy=http://your_proxy:8080\n'
               'Next, run this utility to label the build plugin container:\n'
               '    label_plugin my_plugin\n'
               '\n'
               'To label a plugin, this utility will start the extraction plugin container on your host.\n'
               )


def _label_plugin_with_plugininfo(image: str, plugin_info: PluginInfo, api_version: str, target_name=None):
    dockerfile = f'FROM {image}'
    labels = _plugin_info_to_labels(plugin_info, api_version)

    name = target_name or f'extraction-plugins/{plugin_info.id}'

    tag_version = f'{name}:{plugin_info.version}'.lower()
    tag_latest = f'{name}:latest'.lower()

    command = ['docker', 'build',
               '-t', tag_version,
               '-t', tag_latest]

    for (label, value) in labels.items():
        command.append('--label')
        command.append(f'{label}={value}')

    command.append('-')  # read dockerfile from stdin (which contains only the FROM-statement)

    _log('Running docker build to add labels to the plugin')
    _run(command, dockerfile)
    return tag_version, tag_latest


def _get_plugin_info(image_name, plugin_port=None, container_name=None) -> Tuple[PluginInfo, str]:
    _log('Retrieve the plugin info from the plugin')
    _log('> Starting the extraction plugin')
    host_port = plugin_port or find_free_port()
    container_name = container_name or f'hansken_label_plugin_{uuid.uuid4()}'
    _run(['docker', 'run', '-d', '-p', f'{host_port}:8999', f'--name={container_name}', image_name])

    _log('> Connecting to the extraction plugin')
    try:
        with grpc.insecure_channel(f'localhost:{host_port}') as channel:
            # wait for ready state of channel
            grpc.channel_ready_future(channel).result()
            stub = ExtractionPluginService_pb2_grpc.ExtractionPluginServiceStub(channel)
            _log('> Request plugin info from plugin')
            rpc_plugin_info = stub.pluginInfo(empty_pb2.Empty())
            plugin_info, api_version = unpack.plugin_info(rpc_plugin_info)
            _log('> Got plugin info from plugin!')
            return plugin_info, api_version
    except Exception as e:
        _log_error(e)
        raise e
    finally:
        _log('> Stopping the plugin')
        _run(['docker', 'rm', '-f', container_name])


def label_plugin(image, target_name=None) -> Union[Tuple[str, str], None]:
    """
    Given an plugin image, label it.

    :param image: the plugin OCI image to label
    :param target_name: optional target image name that will contain the labels
    :return: tag_with_version, tag_with_latest, None if the plugin is not compatible
    """
    plugin_info, api_version = _get_plugin_info(image)

    if not plugin_info.id or not plugin_info.id.domain or not plugin_info.id.category or not plugin_info.id.name:
        _log_error('The plugin to label did not return a valid plugin id. '
                   'If the plugin was created before SDK version 0.4.0, please consider upgrading your plugin.')
        return None

    return _label_plugin_with_plugininfo(image, plugin_info, api_version, target_name)


def log_labels(tag_version, tag_latest):
    """Log the plugin image tags."""
    _log('plugin labeled!')
    _log(f'> plugin image tag: {tag_version}')
    _log(f'> plugin image tag: {tag_latest}')


def _label_plugin(image, target_name=None):
    # internal use: label plugin, print labels directly to stdout
    tag_version, tag_latest = label_plugin(image, target_name)
    log_labels(tag_version, tag_latest)
    print(tag_latest)


def _parse_arguments():
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    # required image argument
    parser.add_argument('image', help='The image to add labels to')

    # optional targetimage argument
    parser.add_argument('--target-name',
                        help='Optional target image, the original image will not be updated', required=False)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return None

    return parser.parse_args()


def main():
    """Label an extraction plugin Docker image according to provided arguments."""
    arguments = _parse_arguments()
    if not arguments:
        sys.exit(2)

    try:
        _main(lambda: _label_plugin(arguments.image, arguments.target_name), 'LABEL_PLUGIN')
        sys.exit(0)
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
