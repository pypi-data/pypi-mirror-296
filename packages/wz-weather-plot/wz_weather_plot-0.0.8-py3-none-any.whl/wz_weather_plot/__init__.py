# -*- coding: UTF-8 -*-
"""
@Name:__init__.py.py
@Auth:yujw
@Date:2024/8/11-13:05
"""
import copy
import os
from pathlib import Path

import numpy as np

from wz_weather_utils import TimeZone
from wz_weather_utils.read_yaml import ReadYaml
from wz_weather_utils.save_type import SaveType
from ._plot_images import DrawImages

DIRNAME = Path(__name__).parent.absolute()
CFG_CONFIG = os.path.join(DIRNAME, "resources", "wea_config.yaml")

if os.path.exists(CFG_CONFIG):
    try:
        ENV_NAME = ReadYaml(CFG_CONFIG).read("ENV").get("NAME", "CONFIG_LOCAL")
    except KeyError:
        ENV_NAME = "CONFIG_LOCAL"

    ENV_CFG = ReadYaml(CFG_CONFIG).read(ENV_NAME)
    ANALYSIS_CONFIG = dict(
        PLOT_CFG=os.path.join(DIRNAME, "resources", ENV_CFG.get("PLOT_CFG", "plot_cfg.yaml"))
    )
    if Path(ANALYSIS_CONFIG.get("PLOT_CFG")).exists():
        PLOT_CONFIG = ReadYaml(ANALYSIS_CONFIG.get("PLOT_CFG"))


class ContourfSettings:
    def __init__(self, add_color_bar=True, elements_detail: dict = None):
        self.add_color_bar = add_color_bar
        self.elements_detail = elements_detail


class DataDetailSettings:
    def __init__(self, data_type="WIZGRD02", save_path=None, u_path=None, v_path=None, contour_paths: dict = None,
                 contourf_paths: dict = None):
        self.data_type = SaveType[data_type]
        self.u_path = u_path
        self.v_path = v_path
        self.save_path = save_path
        self.contour_paths = contour_paths
        self.contourf_paths = contourf_paths
        self.contourf_keys = list(contourf_paths.keys()) if contourf_paths else []
        self.contour_keys = list(contour_paths.keys()) if contour_paths else []


class ContourSettings:
    def __init__(self, colors, levels, line_widths=1.5, line_styles="-"):
        self.colors = colors
        if len(levels) == 3:
            self.levels = np.arange(levels[0], levels[1] + 1, levels[2])
        else:
            self.levels = levels

        self.line_widths = line_widths
        self.line_styles = line_styles


class WindBarSettings:
    def __init__(self, barb_color="black", length=7, re_grid_shape=20):
        self.barb_color = barb_color
        self.length = length
        self.re_grid_shape = re_grid_shape


class MapSettings:
    def __init__(self, extent=(70, 140, 0, 50, 10, 10), add_province=True, add_city=False, dpi=200, **kwargs):
        self.extent = extent[0:4]
        self.x_scale, self.y_scale = extent[4], extent[5]
        self.add_province = add_province
        self.add_city = add_city
        self.dpi = dpi
        self.title = kwargs.get("title", "")


class PlotConfig:
    def __init__(self, cfg_name):
        _cfg = PLOT_CONFIG.read(cfg_name)
        self.contourf_sets = ContourfSettings(**_cfg.get("contourf_cfg", {}))
        self.contour_sets = {ik: [ContourSettings(**val) for val in iv] for ik, iv in
                             _cfg.get("contour_cfg", {}).items()}
        self.wind_bar_sets = WindBarSettings(**_cfg.get("wind_bar_cfg", {}))
        self.map_sets = MapSettings(**_cfg.get("map_cfg", {}))
        self.deta_detail_sets = DataDetailSettings(**_cfg.get("data_detail_cfg", {}))
        cst_cfg = _cfg.get("cst_hour")
        self.cst_range = range(cst_cfg.get("start_cst"), cst_cfg.get("end_cst") + 1, cst_cfg.get("step"))
        self.time_interval = _cfg.get("time_interval")
        self.time_zone = TimeZone[_cfg.get("time_zone")]
        self.save_path = _cfg.get("save_path")
