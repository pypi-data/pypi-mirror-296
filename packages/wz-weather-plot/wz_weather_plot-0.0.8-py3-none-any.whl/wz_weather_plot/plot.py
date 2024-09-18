# -*- coding: UTF-8 -*-
"""
@Name:plot.py
@Auth:yujw
@Date:2024/8/11-17:00
"""
import asyncio
import sys
import traceback
from datetime import timedelta, datetime
from pathlib import Path
from wz_weather_utils.logging import logger
from . import DrawImages, PlotConfig, ContourfSettings
from wz_weather_utils.wizgrd import open_grid_file, SaveType
from wz_weather_utils import get_report_time


def __plot_contourf(drw: DrawImages, report_time, cst_hour, data_type: SaveType, contourf_paths: dict,
                    contourf_cfg: ContourfSettings):
    # 考虑到不同数据类型可能有不同的等值面设置，所以这里需要遍历每个数据类型
    color_bar_params = []
    for key, path_fmt in contourf_paths.items():
        # 拼接文件路径
        file_path = path_fmt.format(report_time=report_time, cst_hour=cst_hour)
        if not Path(file_path).exists():
            continue
        # 读取等值面数据
        contourf_data = open_grid_file(file_path, data_type)
        _contourf_cfg = contourf_cfg.elements_detail.get(key)
        # 绘制等值面
        if _contourf_cfg:
            colors = [color.strip() for color in _contourf_cfg.get("colors", "").split(",")]
            levels = [float(level.strip()) for level in _contourf_cfg.get("levels", "").split(",")]
            color_bar_params.append({"colors": colors, "levels": levels,
                                     "extend": _contourf_cfg.get("extend", "both"),
                                     "cmap": _contourf_cfg.get("cmap", None),
                                     "color_bar_label": _contourf_cfg.get("color_bar_label", None),
                                     "bar_bounds_name": _contourf_cfg.get("bar_bounds_name", None),
                                     })
            drw.contourf(contourf_data, levels=levels, colors=colors,
                         cmap=_contourf_cfg.get("cmap"))
    if contourf_cfg.add_color_bar:
        drw.add_more_color_bar(color_bar_params)


def __plot_contour(drw: DrawImages, report_time, cst_hour, data_type: SaveType, contour_paths, contour_sets):
    # 考虑同一类数据可能会有多个等值线样式，所以这里需要遍历每个数据类型
    for key, path_fmt in contour_paths.items():
        # 读取等值线数据
        file_path = path_fmt.format(report_time=report_time, cst_hour=cst_hour)
        if not Path(file_path).exists():
            continue
        contour_data = open_grid_file(file_path, data_type)
        # 获取等值线设置
        _contour_set = contour_sets.get(key)
        if _contour_set:
            for c_detail in _contour_set:
                drw.contour(contour_data, levels=c_detail.levels, colors=c_detail.colors,
                            line_widths=c_detail.line_widths, line_styles=c_detail.line_styles)


def __plot_wind_barbs(drw, report_time, cst_hour, data_type, deta_detail_sets, wind_bar_sets):
    # 读取风场数据
    u_file_path = deta_detail_sets.u_path.format(report_time=report_time, cst_hour=cst_hour)
    v_file_path = deta_detail_sets.v_path.format(report_time=report_time, cst_hour=cst_hour)
    # 风场数据存在才绘制
    if not Path(u_file_path).exists() or not Path(v_file_path).exists():
        return
    # 加载风场数据
    u_data = open_grid_file(u_file_path, data_type)
    v_data = open_grid_file(v_file_path, data_type)
    # 绘制风场
    drw.wind_barbs(u_data, v_data, barb_color=wind_bar_sets.barb_color, length=wind_bar_sets.length,
                   regrid_shape=wind_bar_sets.re_grid_shape)


async def plot_images(report_time, cst_hour, pt_cfg: PlotConfig):
    # 初始化绘图对象
    drw = DrawImages(pt_cfg.map_sets.extent, x_scale=pt_cfg.map_sets.x_scale, y_scale=pt_cfg.map_sets.y_scale,
                     dpi=pt_cfg.map_sets.dpi)
    # 初始化地图
    drw.init_map(chn_kwargs=dict(add_province=pt_cfg.map_sets.add_province, add_city=pt_cfg.map_sets.add_city))
    # 添加标题
    drw.add_default_title(pt_cfg.map_sets.title, report_time, cst_hour)
    # 绘制等值面
    if pt_cfg.deta_detail_sets.contourf_paths:
        __plot_contourf(drw, report_time, cst_hour, pt_cfg.deta_detail_sets.data_type,
                        pt_cfg.deta_detail_sets.contourf_paths, pt_cfg.contourf_sets)
    # 绘制等值线
    if pt_cfg.deta_detail_sets.contour_paths:
        __plot_contour(drw, report_time, cst_hour, pt_cfg.deta_detail_sets.data_type,
                       pt_cfg.deta_detail_sets.contour_paths, pt_cfg.contour_sets)
    # 绘制风场
    if pt_cfg.deta_detail_sets.u_path:
        __plot_wind_barbs(drw, report_time, cst_hour, pt_cfg.deta_detail_sets.data_type,
                          pt_cfg.deta_detail_sets, pt_cfg.wind_bar_sets)
    # 保存图片
    drw.save_file(pt_cfg.deta_detail_sets.save_path.format(report_time=report_time, cst_hour=cst_hour))
    await asyncio.sleep(0.01)


def run_plot_task():
    """
    运行绘图任务
    :return:0
    """
    args = sys.argv
    assert len(args) >= 2, "未指定启动key"

    pt_cfg = PlotConfig(args[1])

    cst_hours = pt_cfg.cst_range
    try:
        if len(args) == 3:
            start = datetime.strptime(args[2], "%Y%m%d%H")
            end = start
        elif len(args) == 4:
            start = datetime.strptime(args[2], "%Y%m%d%H")
            end = datetime.strptime(args[3], "%Y%m%d%H")
        else:
            end = get_report_time(pt_cfg.time_interval, time_zone=pt_cfg.time_zone)
            start = end
            for idx in range(3):
                start = start - timedelta(**pt_cfg.time_interval)

        while start <= end:
            for cst in cst_hours:
                asyncio.run(plot_images(start, cst, pt_cfg))
            start = start + timedelta(**pt_cfg.time_interval)
    except BaseException as e:
        traceback.print_exception(None, e, e.__traceback__)
        logger.error(e)
