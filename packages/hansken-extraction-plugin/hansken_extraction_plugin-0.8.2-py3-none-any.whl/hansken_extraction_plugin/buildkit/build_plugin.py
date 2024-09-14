"""Contains a cmd entry point to create a plugin docker image with plugin info labels."""
from random import randint
import sys

from hansken_extraction_plugin.buildkit._build import _log, _log_error, _main, _run
from hansken_extraction_plugin.buildkit.label_plugin import label_plugin, log_labels

usage_explanation = ('Usage: {} [-h] [--help] DOCKER_FILE_DIRECTORY [DOCKER_IMAGE_NAME] [DOCKER_ARGS]\n'
                     '  DOCKER_FILE_DIRECTORY: Path to the directory containing the Dockerfile of the plugin.\n'
                     '  (Optional) [DOCKER_IMAGE_NAME]: Name of the target docker image without tag. Note that docker '
                     'image names cannot start with a period or dash.\n '
                     '                                 If it starts with a dash, it will be '
                     'interpreted as an additional docker argument (see next).\n'
                     '  (Optional) [DOCKER_ARGS]: Additional argument(s) passed to the `docker build` command, '
                     'separated by spaces.\n'
                     '\n'
                     'Example: build_plugin . image_name --build-arg https_proxy="$https_proxy"')


def _build(docker_file_path, docker_args=None, tmp_plugin_image=None) -> str:
    tmp_plugin_image = tmp_plugin_image or f'build_extraction_plugin:{randint(0, 999999)}'  # nosec
    command = ['docker', 'build', docker_file_path, '-t', tmp_plugin_image]
    command.extend(docker_args)

    _log('Building a Hansken extraction plugin image')
    _run(command)
    return tmp_plugin_image


def _build_and_label(docker_file_path, target_image_name=None, docker_args=None):
    tmp_plugin_image = _build(docker_file_path, docker_args)
    _log('The plugin image was built successfully! Now the required plugin LABELS will be added to the image.')
    try:
        result = label_plugin(tmp_plugin_image, target_image_name)
    finally:
        _log('Removing temporary build image')
        _run(['docker', 'image', 'rm', tmp_plugin_image])

    if not result:
        return
    tag_version, tag_latest = result
    log_labels(tag_version, tag_latest)  # logging *AFTER* removing temporary build image for user readability
    print(tag_latest)


def _parse_args(argv):
    if len(argv) == 0 or (argv[0] == '-h' or argv[0] == '--help'):
        if len(argv) == 0:
            _log_error('Wrong number of arguments!\n')
        print(usage_explanation)
        return None

    docker_file = argv[0]
    # oci image names cannot start with a dash, so if this arg starts with a dash
    # omit the name arg and expect it to be an extra docker arg
    omit_name = len(argv) <= 1 or argv[1].startswith('-')
    name = None if omit_name else argv[1]
    docker_args_start_pos = 1 if omit_name else 2
    docker_args = [] if len(argv) <= docker_args_start_pos else argv[docker_args_start_pos:]
    return docker_file, name, docker_args


def main():
    """Build and label an extraction plugin Docker image according to provided arguments."""
    parsed = _parse_args(sys.argv[1:])
    if not parsed:
        sys.exit(1)

    docker_file_path, target_image_name, docker_args = parsed
    try:
        _main(lambda: _build_and_label(docker_file_path, target_image_name, docker_args), 'BUILD_PLUGIN')
        sys.exit(0)
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
