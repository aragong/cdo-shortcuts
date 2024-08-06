import os
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from time import time
from typing import Union


def cdo_mergetime(
    input_nc_paths: list[str],
    output_nc_path: str,
    variables: Union[list[str], None] = None,
    pack: bool = False,
):
    """stack netcdf files in time dimension and delete duplicate timesteps

    Args:
        input_nc_paths (list[str]): list to netcdf files (files should be sorted by time, most recent first)
        output_nc_path (str): path to output netcdf file
        variables (Union[list[str], None]): if defined, only these variables will be kept in the output file. Defaults to None.
        pack (bool, optional): if True, output file will be packed (reduce size of the output file). Defaults to False.
    """

    t0 = time()
    tmp_dir = TemporaryDirectory(dir=".")
    output_nc_path = Path(output_nc_path)

    if variables:
        for path in input_nc_paths:
            path = Path(path)
            response = run(
                [
                    "cdo",
                    f"selvar,{','.join(variables)}",
                    path,
                    Path(tmp_dir.name, path.stem + "_subset.nc"),
                ],
                capture_output=True,
                check=False,
            )
            print(response.stderr.decode("utf-8"))

        nc_paths = [str(path) for path in Path(tmp_dir.name).glob("*_subset.nc")]
    else:
        nc_paths = input_nc_paths

    response = run(
        [
            "cdo",
            "mergetime",
            " ".join(nc_paths),
            Path(tmp_dir.name, "merged.nc"),
        ],
        env=dict(os.environ, SKIP_SAME_TIME="1"),
        capture_output=True,
        check=False,
    )
    print(response.stderr.decode("utf-8"))
    outfile = Path(tmp_dir.name, "merged.nc")

    if pack:
        response = run(
            [
                "cdo",
                "pack",
                Path(tmp_dir.name, "merged.nc"),
                Path(tmp_dir.name, "packed.nc"),
            ],
            capture_output=True,
            check=False,
        )
        print(response.stderr.decode("utf-8"))
        outfile = Path(tmp_dir.name, "packed.nc")

    outfile.rename(output_nc_path)

    tmp_dir.cleanup()
    print("done!\n")
    print(f"{'Output file:':<15} {output_nc_path.resolve()}")
    print(f"{'File size:':<15} {output_nc_path.stat().st_size / 1e6:.2f} MB")
    print(f"{'Elapsed time:':<15} {time() - t0:.2f} seconds\n")


if __name__ == "__main__":

    paths = [str(path) for path in Path("data").glob("*.nc")]
    paths.sort()

    cdo_mergetime(
        input_nc_paths=paths,
        output_nc_path="merged.nc",
        variables=["u", "v", "mslp", "visibility", "wind_gust"],
        pack=True,
    )
    assert Path("merged.nc").exists(), "something went wrong!"
    Path("merged.nc").unlink()
