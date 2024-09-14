
# Spio

## Description

Spio is a Python package that provides functionalities for reading and writing data to a SharePoint.
It can also handle various types of spatial and non-spatial data formats such as GeoTIFF, GeoPackage, NetCDF, CSV, Excel, and more.

## Installation

To install the package, you can use the following command:

```bash
    pip config set global.extra-index-url https://repo.vito.be/artifactory/api/pypi/marvin-projects-pypi-local/simple
    pip install spio 
```

If you want to install the package with all the dependencies, you can use the following command:

```bash
    pip install spio[full]
```

## Building from Source

To build the package from source you can use the following commands:

```bash
    git clone https://git.vito.be/projects/MARVIN/repos/sharepoint_tools
    cd sharepoint_tools
    conda create -f conda_env.yml
    conda activate spio 
    poetry install
```

## Configuration

Before using the package, you need to configure the settings to match your environment. 
The configuration is managed through a `settings` module which should include all the necessary configurations.

### **Settings Configuration**:
   Ensure you have a `settings` file (e.g., `.secrets.yaml` or `settings.yaml`) that provides the necessary configuration options. Example:

```python
    from dynaconf import Dynaconf

    settings = Dynaconf(
        settings_files=['settings.yaml', '.secrets.yaml']
    )
```
   
   The settings file should include the following configurations:
    
```yaml
    user_account: your.name@vito.be
```

### **Initialize Spio with Settings**:
   You need to initialize Spio with your settings before using any functionalities.

```python
    from config import settings
    from marvin.tools import spio

    spio.init_spio(settings)
```

## Usage

Here are some example usages of the package:

### Reading Data

- **Read GeoTIFF using Rasterio**:

```python
    from marvin.tools.spio import read_geotiff_rasterio

    geotiff_data = read_geotiff_rasterio('path/to/your/geotiff/file.tif')
```

- **Read GeoPackage**:

```python
    from marvin.tools.spio import read_geopackage

    geopackage_data = read_geopackage('path/to/your/geopackage/file.gpkg')
```

- **Read NetCDF**:

```python
    from marvin.tools.spio import read_netcdf

    netcdf_data = read_netcdf('path/to/your/netcdf/file.nc')
```

- **Read CSV**:

```python
    from marvin.tools.spio import read_csv

    csv_data = read_csv('path/to/your/csv/file.csv')
```

### Writing Data

- **Write CSV**:

```python
    from marvin.tools.spio import write_csv

    write_csv('path/to/your/output/file.csv', csv_data)
```

- **Write Excel**:

```python
    from marvin.tools.spio import write_excel

    write_excel('path/to/your/output/file.xlsx', excel_data)
```

### Additional Functionalities

Spio also provides additional functions to handle different data formats and processes.
You can explore these in the https://git.vito.be/projects/MARVIN/repos/sharepoint_tools/browse/test/tst_spio.py file for more complex scenarios such as writing to OneDrive, processing NetCDF4 files, and more.


## Contributing

If you want to contribute to spio, please follow the standard contributing guidelines and push your changes to a new branch in
https://git.vito.be/projects/MARVIN/repos/sharepoint_tools

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
