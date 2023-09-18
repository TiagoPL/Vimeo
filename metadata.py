#!/usr/bin/env python3

import io
import argparse
from datetime import datetime
from flask import jsonify

import vimeo

import formatters

import json

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'
HEADERS = ('data_upload', 'arquivo', 'duracao', 'uploader')


def fetch_metadata(vimeo, folder_id, formatter: formatters.Formatter, recursive: bool):
    project = vimeo.get(f'/me/projects/{folder_id}')
    # import json
    # j = json.dumps(indent=4, obj=project.json())#['data'][0])
    # print(j)
    # return


    with io.StringIO() as string_io:
        print(formatter.format_header(), file=string_io)
        process_folder(vimeo, '', project.json(), formatter, recursive, string_io)
        string_io.flush()
        content = string_io.getvalue()

    return content


def seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def video_list_iterator(vimeo, videos_uri):
    videos_data = vimeo.get(videos_uri).json()
    yield from videos_data['data']

    while videos_data['paging']['next'] is not None:
        videos_data = vimeo.get(videos_data['paging']['next']).json()
        yield from videos_data['data']


def process_folder(vimeo, path, folder, formatter, recursive, io_dest):

    if 'type' in folder.keys():
        if folder['type'] == 'folder':
            path = f'{path}{folder["folder"]["name"]}/'
            created_at = folder["folder"]['created_time']
            duration = 0

            videos = folder["folder"]['metadata']['connections']['videos']
            subfolders = folder["folder"]['metadata']['connections']['folders']

        elif folder['type'] == 'video':
            path = f'{path}{folder["video"]["name"]}/'
            created_at = folder["video"]['created_time']
            duration = 0

            videos = folder["video"]['parent_folder']['metadata']['connections']['videos']
            subfolders = folder["video"]['parent_folder']['metadata']['connections']['folders']

    else:
        path = f'{path}{folder["name"]}/'
        created_at = folder['created_time']
        duration = 0

        videos = folder['metadata']['connections']['videos']
        subfolders = folder['metadata']['connections']['folders']

    # if recursive and subfolders['total'] > 0:
    #     sf_data = vimeo.get(subfolders['uri'])

    #     for sf in sf_data.json()['data']:
    #         duration += process_folder(vimeo, path, sf, formatter, recursive, io_dest)

    if videos['total'] > 0:
        for v in video_list_iterator(vimeo, videos['uri']):
            duration += process_video(vimeo, path, v, formatter, io_dest)

    if 'type' in folder.keys():
        data = (created_at, path, seconds_to_time(duration), folder['folder']['user']['name'])
        print(formatter.format_row(data), file=io_dest)
    else:
        data = (created_at, path, seconds_to_time(duration), folder['user']['name'])
        print(formatter.format_row(data), file=io_dest)

    return duration


def process_video(vimeo, path, video, formatter, io_dest):
    path = f'{path}{video["name"]}'
    created_at = video['created_time']
    duration = video['duration']

    uploader_uri = video['uploader']['pictures']['uri']

    if uploader_uri is not None:
        uploader_data = vimeo.get(uploader_uri.partition('/pictures')[0]).json()
        uploader = uploader_data['name']

    else:
        uploader = None

    data = (created_at, path, seconds_to_time(duration), uploader or '')
    print(formatter.format_row(data), file=io_dest)

    return duration


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    vimeo_group = parser.add_argument_group('Vimeo')
    vimeo_group.add_argument('--token', '-t', required=True, help='Vimeo token')
    vimeo_group.add_argument('--client-id', '-c', required=True, help='Vimeo Client ID')
    vimeo_group.add_argument('--secret', '-s', required=True, help='Vimeo secret')
    vimeo_group.add_argument('--format', '-f', choices=('csv', 'json'),
                             default='csv', help='Default: csv')
    vimeo_group.add_argument('--csv-delimiter', default=';', help='Default: `;`')
    vimeo_group.add_argument('--recursive', '-R', action='store_true',
                             help='Recurse into subfolders')
    vimeo_group.add_argument('folder', metavar='FOLDER_ID', help='Folder ID to get videos from')
    args = parser.parse_args()

    fmt: formatters.Formatter = {
        'csv': formatters.CSVFormatter,
        'json': formatters.JSONFormatter}[args.format](HEADERS)

    if isinstance(fmt, formatters.CSVFormatter):
        fmt.delimiter = args.csv_delimiter

    content = fetch_metadata(
        vimeo.VimeoClient(
            token=args.token, key=args.client_id, secret=args.secret),
        args.folder,
        fmt,
        args.recursive)

    print(content)
