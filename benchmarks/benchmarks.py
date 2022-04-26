import os
import tempfile

import xarray as xr

from sarsen import apps


class TimeSuite:
    timeout = 240
    params = ["gamma_nearest", "gamma_bilinear"]

    def __init__(self):
        self.datadir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data")
        )
        self.dem_urlpath = tempfile.NamedTemporaryFile(suffix=".tif").name

    def setup(self, correct_radiometry):
        dem_raster = xr.open_dataarray(
            os.path.join(self.datadir, "South-of-Redmond-10m.tif"), engine="rasterio"
        )
        dem_raster_crop = dem_raster.sel(
            x=slice(575_000, 585_000), y=slice(5_200_000, 5_190_000)
        )
        dem_raster_crop.rio.to_raster(self.dem_urlpath)

    def time_terrain_correction(self, correct_radiometry):
        with tempfile.NamedTemporaryFile(suffix=".tif") as tmp:
            apps.terrain_correction(
                os.path.join(
                    self.datadir,
                    "S1B_IW_GRDH_1SDV_20211217T141304_20211217T141329_030066_039705_9048",
                ),
                measurement_group="IW/VV",
                dem_urlpath=self.dem_urlpath,
                correct_radiometry=correct_radiometry,
                output_urlpath=tmp.name,
                grouping_area_factor=(3, 3),
            )
