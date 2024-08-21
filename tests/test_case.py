import pytest
# import shutil
from src.settaxis import settaxis
from pathlib import Path
from datetime import datetime


@pytest.fixture
def tmp_path():
    tmp_path = "tmp"
    return tmp_path


@pytest.fixture
def setup_teardown(tmp_path):
    Path(tmp_path).mkdir(parents=True)
    yield
    # shutil.rmtree(tmp_path)


def test_spezia(tmp_path, setup_teardown):

    flow_db = "/mnt/p/99_PROMPT/02_Forcings/04_Spezia/currents_netcdf"
    flow_files = [str(path) for path in Path(flow_db).glob("*.nc")]
    flow_files.sort()

    wind_db = "/mnt/p/99_PROMPT/02_Forcings/04_Spezia/winds_netcdf"
    wind_files = [str(path) for path in Path(wind_db).glob("*.nc")]
    wind_files.sort()

    flow_folder = Path(tmp_path, "FLOW")
    flow_folder.mkdir(parents=True)

    wind_folder = Path(tmp_path, "WIND")
    wind_folder.mkdir(parents=True)

    new_flow_paths = settaxis(
        input_nc_paths=flow_files,
        init_datetime=datetime(2018, 11, 1, 0, 0, 0),
        timestep_value="hours",
        output_dir=flow_folder,
        pack=True,
    )
    new_flow_paths.sort()

    for i, path in enumerate(new_flow_paths):
        Path(path).rename(Path(flow_folder, f"spezia_Flow_rec_{i+1:02d}.nc"))

    new_wind_paths = settaxis(
        input_nc_paths=wind_files,
        init_datetime=datetime(2018, 11, 1, 0, 0, 0),
        timestep_value="hours",
        output_dir=wind_folder,
        pack=True,
    )

    for i, path in enumerate(new_wind_paths):
        Path(path).rename(Path(wind_folder, f"spezia_Wind_rec_{i+1:02d}.nc"))

    assert len(new_flow_paths) == len(new_wind_paths)
