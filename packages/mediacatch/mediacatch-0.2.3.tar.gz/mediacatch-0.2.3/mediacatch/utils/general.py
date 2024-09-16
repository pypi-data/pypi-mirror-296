import json
import logging
import os
import time
from importlib.resources import files
from io import BufferedReader
from typing import Generator

import requests

logger = logging.getLogger('mediacatch.utils.general')


def get_data_from_url(url: str) -> dict:
    """Get data from a URL.

    Args:
        url (str): The URL to get data from.

    Returns:
        dict: Data dictionary from url.
    """
    logger.info(f'Getting data from {url}')
    response = requests.get(url)
    assert response.status_code == 200, f'Failed to get data from {url}: {response}'
    return response.json()


def load_data_from_json(json_file: str) -> dict:
    """Load data from a JSON file.

    Args:
        json_file (str): JSON file with data.

    Returns:
        dict: Data dictionary from JSON file.
    """
    logger.info(f'Loading data from {json_file}')
    assert os.path.isfile(json_file), f'File {json_file} does not exist'
    with open(json_file, 'r') as f:
        result = json.load(f)
    return result


def get_assets_data(fname: str) -> str:
    data_file = files('mediacatch').joinpath(f'assets/{fname}')
    assert data_file.is_file(), f'File {fname} does not exist in mediacatch/assets folder'
    return data_file


def make_request(
    method: str,
    url: str,
    headers: dict[str, str],
    max_retries: int = 3,
    delay: float = 0.5,
    **kwargs,
) -> requests.Response:
    """Makes a request to the given URL.

    Args:
        method (str): Request method.
        url (str): The URL to make the request to.
        headers (dict[str, str]): Headers to include in the request.
        max_retries (int, optional): Maximum retries. Defaults to 3.
        delay (float, optional): Delay between retries. Defaults to 0.5.

    Raises:
        RuntimeError: If method is post and response status code is equal or greater than 400.
        RuntimeError: If maximum retries limit is reached.

    Returns:
        requests.Response: Response object.
    """
    for _ in range(max_retries):
        response = getattr(requests, method)(url, headers=headers, **kwargs)
        if 200 <= response.status_code < 300:
            return response

        if method == 'post' and response.status_code >= 400:
            raise RuntimeError(f'Error during request to {url}', response.json()['detail'])

        time.sleep(delay)

    raise RuntimeError('Maximum retry limit reached for request', None)


def read_file_in_chunks(
    file_: BufferedReader, chunk_size: int = 100 * 1024 * 1024
) -> Generator[bytes, None, None]:
    """Reads a file in chunks.

    Args:
        file_ (BufferedReader): File to read.
        chunk_size (int, optional): Size . Defaults to 100*1024*1024.

    Yields:
        Generator[bytes, None, None]: Chunk of the file.
    """
    while chunk := file_.read(chunk_size):
        yield chunk
