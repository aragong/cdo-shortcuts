import pytest
import shutil
from pathlib import Path
from src.mergetime import mergetime
from src.settaxis import settaxis
from datetime import datetime


@pytest.fixture
def tmp_path():
    tmp_path = "tmp"
    return tmp_path


@pytest.fixture
def setup_teardown(tmp_path):
    Path(tmp_path).mkdir(parents=True)
    yield
    shutil.rmtree(tmp_path)


def test_mergetime(tmp_path, setup_teardown):
    paths = [str(path) for path in Path("data").glob("*.nc")]
    paths.sort()

    mergetime(
        input_nc_paths=paths,
        output_nc_path=str(Path(tmp_path, "my_merged_netcdf.nc")),
        variables=["u", "v", "mslp", "visibility", "wind_gust"],
        pack=True,
    )
    assert Path(tmp_path, "my_merged_netcdf.nc").exists()


def test_set_reftime(tmp_path, setup_teardown):
    paths = [str(path) for path in Path("data").glob("*.nc")]

    out_paths = settaxis(
        input_nc_paths=paths,
        init_datetime=datetime(2024, 7, 27, 0, 0, 0),
        timestep_value="minutes",
        output_dir=tmp_path,
        pack=True,
    )

    for path in out_paths:
        assert Path(path).exists()
