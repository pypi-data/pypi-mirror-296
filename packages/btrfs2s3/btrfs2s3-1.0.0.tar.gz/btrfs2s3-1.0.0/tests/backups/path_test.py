from __future__ import annotations

import itertools
import random
import re
from typing import TYPE_CHECKING
from uuid import UUID

import arrow
from btrfs2s3._internal.backups import BackupInfo
import pytest

if TYPE_CHECKING:
    from typing import Sequence
    from typing import TypeVar

    _T = TypeVar("_T")


def test_get_path_suffixes_with_real_timezone() -> None:
    info = BackupInfo(
        uuid=UUID("3fd11d8e-8110-4cd0-b85c-bae3dda86a3d").bytes,
        parent_uuid=UUID("9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e").bytes,
        ctransid=12345,
        ctime=arrow.get("2006-01-01", tzinfo="US/Pacific").timestamp(),
        send_parent_uuid=UUID("3ae01eae-d50d-4187-b67f-cef0ef973e1f").bytes,
    )
    got = info.get_path_suffixes(tzinfo="US/Pacific")
    expected = [
        ".ctim2006-01-01T00:00:00-08:00",
        ".ctid12345",
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d",
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f",
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e",
        ".mdvn1",
        ".seqn0",
    ]
    assert got == expected

    round_trip = BackupInfo.from_path(f"name{''.join(got)}.gz")
    assert round_trip == info


def test_get_path_suffixes_default_to_utc() -> None:
    info = BackupInfo(
        uuid=UUID("3fd11d8e-8110-4cd0-b85c-bae3dda86a3d").bytes,
        parent_uuid=UUID("9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e").bytes,
        ctransid=12345,
        ctime=arrow.get("2006-01-01").timestamp(),
        send_parent_uuid=UUID("3ae01eae-d50d-4187-b67f-cef0ef973e1f").bytes,
    )
    got = info.get_path_suffixes()
    expected = [
        ".ctim2006-01-01T00:00:00+00:00",
        ".ctid12345",
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d",
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f",
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e",
        ".mdvn1",
        ".seqn0",
    ]
    assert got == expected

    round_trip = BackupInfo.from_path(f"name{''.join(got)}.gz")
    assert round_trip == info


def test_get_path_suffixes_with_full_backup() -> None:
    info = BackupInfo(
        uuid=UUID("3fd11d8e-8110-4cd0-b85c-bae3dda86a3d").bytes,
        parent_uuid=UUID("9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e").bytes,
        ctransid=12345,
        ctime=arrow.get("2006-01-01").timestamp(),
        send_parent_uuid=None,
    )
    got = info.get_path_suffixes()
    expected = [
        ".ctim2006-01-01T00:00:00+00:00",
        ".ctid12345",
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d",
        ".sndp00000000-0000-0000-0000-000000000000",
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e",
        ".mdvn1",
        ".seqn0",
    ]
    assert got == expected

    round_trip = BackupInfo.from_path(f"name{''.join(got)}.gz")
    assert round_trip == info


def _fixed_choices(population: Sequence[_T], seed: int, k: int) -> list[_T]:
    state = random.getstate()
    random.seed(seed)
    result = random.choices(population, k=k)
    random.setstate(state)
    return result


@pytest.mark.parametrize(
    "suffixes",
    _fixed_choices(
        list(
            itertools.permutations(
                [
                    ".ctim2006-01-01T00:00:00-08:00",
                    ".ctid12345",
                    ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d",
                    ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f",
                    ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e",
                    ".mdvn1",
                    ".seqn0",
                    ".gz",
                ]
            )
        ),
        0,
        1000,
    ),
)
def test_from_path_with_suffixes_in_any_order(suffixes: Sequence[str]) -> None:
    path = f"my-backup{''.join(suffixes)}"
    got = BackupInfo.from_path(path)
    expected = BackupInfo(
        uuid=UUID("3fd11d8e-8110-4cd0-b85c-bae3dda86a3d").bytes,
        parent_uuid=UUID("9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e").bytes,
        ctransid=12345,
        ctime=arrow.get("2006-01-01", tzinfo="US/Pacific").timestamp(),
        send_parent_uuid=UUID("3ae01eae-d50d-4187-b67f-cef0ef973e1f").bytes,
    )
    assert got == expected


@pytest.mark.parametrize(
    "bad_path",
    [
        ".ctim20O6-01-01T00:00:00-08:00"
        ".ctid12345"
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
        ".mdvn1"
        ".seqn0",
        ".ctim2006-01-01T00:00:00-08:00"
        ".ctid12345"
        ".uuid3fd11d8e-811O-4cd0-b85c-bae3dda86a3d"
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
        ".mdvn1"
        ".seqn0",
        ".ctim2006-01-01T00:00:00-08:00"
        ".ctidl2345.u3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
        ".mdvn1"
        ".seqn0",
        ".ctim2006-01-01T00:00:00-08:00"
        ".ctid12345"
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
        ".mdvn1"
        ".seqn0",
        ".ctim2006-01-01T00:00:00-08:00"
        ".ctid12345"
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
        ".prnt9d9d3gcb-4b62-46a3-b6e2-678eeb24f54e"
        ".mdvn1"
        ".seqn0",
    ],
)
def test_bad_paths(bad_path: str) -> None:
    with pytest.raises(
        ValueError, match="missing or incomplete parameters for backup name"
    ):
        BackupInfo.from_path(bad_path)


@pytest.mark.parametrize(
    "bad_path",
    [
        "bad-path-no-suffixes",
        "bad.path.with.suffixes",
        ".ctim2006-01-01T00:00:00-08:00"
        ".ctid12345"
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
        ".seqn0",
        ".ctim2006-01-01T00:00:00-08:00"
        ".ctid12345"
        ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
        ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
        ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
        ".mdvnI"
        ".seqn0",
    ],
)
def test_no_version(bad_path: str) -> None:
    with pytest.raises(
        ValueError,
        match=re.escape("backup name metadata version missing (not a backup?)"),
    ):
        BackupInfo.from_path(bad_path)


def test_bad_version() -> None:
    with pytest.raises(ValueError, match="unsupported backup name metadata version"):
        BackupInfo.from_path(
            ".ctim2006-01-01T00:00:00-08:00"
            ".ctid12345"
            ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
            ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
            ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
            ".mdvn1000"
            ".seqn0"
        )


def test_bad_sequence_number() -> None:
    with pytest.raises(ValueError, match="unsupported sequence number"):
        BackupInfo.from_path(
            ".ctim2006-01-01T00:00:00-08:00"
            ".ctid12345"
            ".uuid3fd11d8e-8110-4cd0-b85c-bae3dda86a3d"
            ".sndp3ae01eae-d50d-4187-b67f-cef0ef973e1f"
            ".prnt9d9d3bcb-4b62-46a3-b6e2-678eeb24f54e"
            ".mdvn1"
            ".seqn1"
        )
