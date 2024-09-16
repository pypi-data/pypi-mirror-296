import argparse
import sys
import transmission_rpc


def _parse_arguments(args):
    argument_parser = argparse.ArgumentParser(
        description=(
            "Given a list of torrent file names (one per line, including the torrent"
            " name) on standard input, mark the files as unwanted (do not download) in"
            " the corresponding Transmission torrent."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argument_parser.add_argument(
        "--transmission-url",
        help="URL of the Transmission instance to connect to",
        default="http://127.0.0.1:9091",
    )
    return argument_parser.parse_args(args)


def _mark_unwanted(transmission_client):
    torrents = transmission_client.get_torrents(arguments=["infohash", "name", "files"])
    # Note we use torrent.fields["files"], not torrent.get_files(), to work around
    # https://github.com/trim21/transmission-rpc/issues/455
    #
    # TODO: this could be made more memory-efficient by using two levels of nested
    # dicts.
    torrent_info_hash_and_file_id_by_file_name = {
        file["name"]: (torrent.info_hash, file_id)
        for torrent in torrents
        for file_id, file in enumerate(torrent.fields["files"])
    }

    missing = False
    unwanted_file_ids_by_torrent_info_hash = {}
    for file_name in (line.rstrip("\r\n") for line in sys.stdin):
        if len(file_name) == 0:
            continue

        torrent_info_hash_and_file_id = torrent_info_hash_and_file_id_by_file_name.get(
            file_name
        )
        if torrent_info_hash_and_file_id is None:
            print(f"WARNING: file not found in torrents: {file_name}", file=sys.stderr)
            missing = True
            continue

        torrent_info_hash, file_id = torrent_info_hash_and_file_id
        unwanted_file_ids_by_torrent_info_hash.setdefault(torrent_info_hash, []).append(
            file_id
        )

    for (
        torrent_info_hash,
        unwanted_file_ids,
    ) in unwanted_file_ids_by_torrent_info_hash.items():
        transmission_client.change_torrent(
            torrent_info_hash, files_unwanted=unwanted_file_ids
        )

    return not missing


def run(args):
    args = _parse_arguments(args)
    transmission_url = args.transmission_url
    with transmission_rpc.from_url(transmission_url) as transmission_client:
        return _mark_unwanted(transmission_client)


def main():
    return 0 if run(args=None) else 1
