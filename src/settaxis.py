from typing import Union
from datetime import datetime
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from time import time


def settaxis(
    input_nc_paths: Union[str, list],
    init_datetime: datetime,
    timestep_value: str,
    output_dir: str = "",
    pack: bool = False,
) -> list[str]:
    """Overwrite definition of time axis based on initial datetime and timestep value,
    the total number of timesteps will be the same.

    Args:
        input_nc_paths (Union[str, list]): path to netcdf file or list of paths
        init_datetime (datetime): inital datetime
        timestep_value (str): temporal value and units for the timestep (e.g. "15minutes")
        output_dir (str, optional): output directory. Defaults to "".
        pack (bool, optional): pack the output file. Defaults to False.
    """

    # cdo settaxis,Date,time,units in.nc out.nc
    # cdo settaxis,2000-01-01,00:00:00,6hour in.nc out.nc

    t0 = time()

    tmp_dir = TemporaryDirectory(dir=output_dir, prefix="tmp_")

    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    if isinstance(input_nc_paths, list) and len(input_nc_paths) == 1:
        input_nc_paths = input_nc_paths[0]

    out_paths = []
    for path in input_nc_paths:
        path = Path(path)
        response = run(
            [
                "cdo",
                f"settaxis,{init_datetime.isoformat(sep=",", timespec="seconds")},{timestep_value}",
                path,
                Path(tmp_dir.name, f"{path.stem}_settaxis.nc"),
            ],
            capture_output=True,
            check=False,
        )
        print(response.stderr.decode("utf-8"))
        outfile = Path(tmp_dir.name, f"{path.stem}_settaxis.nc")

        if pack:
            response = run(
                ["cdo", "pack", outfile, Path(tmp_dir.name, f"{outfile.stem}_packed.nc")],
                capture_output=True,
                check=False,
            )
            print(response.stderr.decode("utf-8"))
            outfile = Path(tmp_dir.name, f"{outfile.stem}_packed.nc")

        outfile.rename(Path(output_dir, f"{outfile.name}"))
        out_paths.append(str(Path(output_dir, f"{outfile.name}")))

    tmp_dir.cleanup()

    print(f"{'Elapsed time:':<15} {time() - t0:.2f} seconds\n")

    return out_paths
