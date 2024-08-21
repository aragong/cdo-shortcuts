# cdo-shortcuts
Simple functions to manage NetCDF-files based on CDO library


## :gear: Functionalities (functions)
- `mergetime:` stacks netcdfs by time, subset variables if needed.
- `settaxis:` redefine time axis based initial datetime and timestep value. 
- `regrid:` re-interpolate NetCDF to a new grid defined by the user. (*To be implemented)
- `subset:` subset NetCDF coordinates (lon, lat, time) and variables. (*To be implemented)


----

## :package: Key dependencies
1. [CDO library](https://code.mpimet.mpg.de/projects/cdo/wiki) installed in your SO


## :rocket: Deployment requirements
- Install CDO
    - for some simple operations pre-compiled version is enough:
    ```bash
    sudo apt install cdo
    ```
    - for some complex operations you should compile CDO in your system with all the desired dependencies (check [Installation and Supported Platforms](https://code.mpimet.mpg.de/projects/cdo/wiki#Installation-and-Supported-Platforms))

## :copyright: Credits
Developed and maintained by :man_technologist: [German Aragon](https://github.com/aragong)
