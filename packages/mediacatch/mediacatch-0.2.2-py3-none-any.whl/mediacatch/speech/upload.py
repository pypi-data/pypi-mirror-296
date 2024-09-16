import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

from mediacatch import mediacatch_api_key
from mediacatch.utils import MediacatchUploadError, make_request, read_file_in_chunks

logger = logging.getLogger('mediacatch.speech.upload')


def upload(
    fpath: str | Path,
    quota: str | None = None,
    fallback_language: str | None = None,
    max_threads: int = 5,
    max_request_retries: int = 3,
    request_delay: float = 0.5,
    chunk_size=100 * 1024 * 1024,  # 100 MB
    url: str = 'https://s2t.mediacatch.io/api/v2',
    verbose: bool = True,
) -> str:
    """Uploads a file to MediaCatch Speech API.

    Args:
        fpath (str | Path): Path to the file to upload.
        quota (str | None, optional): The quota to bill transcription hours from. Can be None if the user only has one quota. Defaults to None.
        fallback_language (str | None, optional): Overrides the language to transcribe in if language identification fails. If None, uses the default language of the quota. Defaults to None.
        max_threads (int, optional): Number of maximum threads. Defaults to 5.
        max_request_retries (int, optional): Number of maximum retries for request. Defaults to 3.
        request_delay (float, optional): Delay between request retries. Defaults to 0.5.
        chunk_size (_type_, optional): Size of each chunk to upload. Defaults to 100*1024*1024.
        url (str, optional): URL of the MediaCatch Speech API. Defaults to 'https://s2t.mediacatch.io/api/v2'.
        verbose (bool, optional): Show verbose output. Defaults to True.

    Returns:
        str: File ID of the uploaded file.
    """
    if not isinstance(fpath, Path):
        fpath = Path(fpath)

    if not fpath.is_file():
        raise MediacatchUploadError(f'File {fpath} does not exist')

    if verbose:
        logger.info(f'Uploading file {fpath} to MediaCatch Speech API')

    headers = {
        'Content-type': 'application/json',
        'X-API-KEY': mediacatch_api_key,
        'X-Quota': str(quota),
    }

    # Initiate file upload
    start_upload_url = f'{url}/upload/'
    data = {
        'file_name': fpath.name,
        'file_extension': fpath.suffix,
        'quota': quota,
        'fallback_language': fallback_language,
    }
    response = make_request(
        'post',
        start_upload_url,
        headers=headers,
        max_retries=max_request_retries,
        delay=request_delay,
        json=data,
    )
    file_id = response.json()['file_id']

    # Upload file chunks
    upload_file_url = f'{url}/upload/{{file_id}}/{{part_number}}'
    etags = []

    def upload_chunk(part_number: int, chunk: bytes) -> None:
        # Get signed URL to upload chunk
        signed_url_response = make_request(
            'get',
            upload_file_url.format(file_id=file_id, part_number=part_number),
            headers=headers,
        )
        signed_url = signed_url_response.json()['url']

        # Upload chunk to storage
        reponse = requests.put(signed_url, data=chunk)
        etag = reponse.headers['ETag']
        etags.append({'e_tag': etag, 'part_number': part_number})

    with (
        ThreadPoolExecutor(max_workers=max_threads) as executor,
        fpath.open('rb') as f,
    ):
        futures = {
            executor.submit(upload_chunk, part_number, chunk): part_number
            for part_number, chunk in enumerate(
                read_file_in_chunks(file_=f, chunk_size=chunk_size), start=1
            )
        }

        for future in as_completed(futures):
            part_number = futures[future]
            try:
                future.result()
            except Exception as e:
                if verbose:
                    logger.error(f'Chunk {part_number} failed to upload due to: {e}')

    # Complete file upload
    complete_upload_url = f'{url}/upload/{file_id}/complete'
    response = make_request('post', complete_upload_url, json={'parts': etags}, headers=headers)
    estimated_processing_time = response.json()['estimated_processing_time']

    if verbose:
        logger.info(
            f'File {fpath} uploaded successfully. Estimated processing time: {estimated_processing_time}'
        )

    return file_id
