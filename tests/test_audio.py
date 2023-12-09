import glob
import io
import os
from http import HTTPStatus

import pytest
from pydub import AudioSegment

from api.routes.audio import FERNET
from config import settings

FILE_NAME = "test_file.mp3"


@pytest.fixture(scope="module", autouse=True)
def clean_up():
    yield
    for f in glob.glob(os.path.join(settings.STORAGE_PATH, "*")):
        os.remove(os.path.join(settings.STORAGE_PATH, f))


@pytest.mark.dependency()
def test_audio_upload(client):
    with open("./tests/resources/test_file.mp3", "rb") as f:
        file = f.read()
    response = client.post(
        url="/audio/upload",
        files={"file": (FILE_NAME, file, "audio/*")},
        headers={"x-api-key": "TEST_KEY"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert os.path.exists(os.path.join(settings.STORAGE_PATH, FILE_NAME))


@pytest.mark.parametrize(
    "body, expected_exception",
    [
        ({"file": None}, HTTPStatus.BAD_REQUEST),
        ({"file": ("test_name", None, "audio/*")}, HTTPStatus.BAD_REQUEST),
        (
            {
                "file": (
                    "test_name",
                    io.BytesIO(
                        b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01"
                    ),
                    "video/*",
                )
            },
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        ),
    ],
)
def test_audio_upload_empty(client, body, expected_exception):
    response = client.post(
        url="/audio/upload",
        files=body,
        headers={"x-api-key": "TEST_KEY"},
    )

    assert response.status_code == expected_exception
    assert not os.path.exists(os.path.join(settings.STORAGE_PATH, "test_name"))


@pytest.mark.dependency(depends=["test_audio_upload"])
def test_audio_download(client):
    response = client.get(
        url=f"/audio/{FILE_NAME}/download", headers={"x-api-key": "TEST_KEY"}
    )
    assert response.status_code == HTTPStatus.OK

    with open("./tests/resources/test_file.mp3", "rb") as f:
        file_content = f.read()
        assert response.content == file_content


@pytest.mark.parametrize("filename", [None, "", "Not_existing", 1231])
def test_audio_download_bad_file_name(client, filename):
    response = client.get(
        url=f"/audio/{filename}/download", headers={"x-api-key": "TEST_KEY"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.dependency(depends=["test_audio_upload"])
def test_audio_volume_increase(client):
    filename = "test_file.mp3"

    file_path = os.path.join(settings.STORAGE_PATH, filename)
    with open(file_path, "rb") as f:
        encrypted_file = f.read()

    decrypted_file = FERNET.decrypt(encrypted_file)
    audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(decrypted_file))
    old_dbfs = audio.dBFS

    # Increase volume request
    response = client.put(
        url=f"/audio/{filename}/adjust_volume",
        headers={"x-api-key": "TEST_KEY"},
        json={"volume_increase": 1},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    with open(file_path, "rb") as f:
        encrypted_file = f.read()

    decrypted_file = FERNET.decrypt(encrypted_file)
    audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(decrypted_file))
    assert old_dbfs < audio.dBFS


@pytest.mark.dependency(depends=["test_audio_upload"])
def test_audio_volume_decrease(client):
    filename = "test_file.mp3"

    file_path = os.path.join(settings.STORAGE_PATH, filename)
    with open(file_path, "rb") as f:
        encrypted_file = f.read()

    decrypted_file = FERNET.decrypt(encrypted_file)
    audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(decrypted_file))
    old_dbfs = audio.dBFS

    # Increase volume request
    response = client.put(
        url=f"/audio/{filename}/adjust_volume",
        headers={"x-api-key": "TEST_KEY"},
        json={"volume_increase": -1},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    with open(file_path, "rb") as f:
        encrypted_file = f.read()

    decrypted_file = FERNET.decrypt(encrypted_file)
    audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(decrypted_file))
    assert old_dbfs > audio.dBFS


@pytest.mark.parametrize("filename", [None, "", "Not_existing", 1231])
def test_audio_volume_modification_bad_file(client, filename):
    response = client.put(
        url=f"/audio/{filename}/adjust_volume",
        headers={"x-api-key": "TEST_KEY"},
        json={"volume_increase": 1},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
