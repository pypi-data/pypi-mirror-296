import copy
from datetime import timedelta
from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import numpy as np
from cartopy import crs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib import pyplot as plt, font_manager
from scipy import ndimage
from wz_weather_utils.grid_data import GridData
from cartopy import feature as cfeature

static_cfg = Path(Path(__file__).parent.absolute(), "static")

font_manager.fontManager.addfont(Path(static_cfg, "fonts", "HELVETI1.TTF"))
font_manager.fontManager.addfont(Path(static_cfg, "fonts", "simkai.ttf"))
font_manager.fontManager.addfont(Path(static_cfg, "fonts", "simsun.ttc"))
font_manager.fontManager.addfont(Path(static_cfg, "fonts", "msyh.ttc"))
mpl.rcParams['font.sans-serif'] = 'simsun'  # 显示中文标签
mpl.rcParams['axes.unicode_minus'] = False  # 显示中文标签


class DrawImages:
    def __init__(self, extent=(70, 140, 0, 60), x_scale=10, y_scale=10,
                 central_longitude=0, dpi=200,
                 fig_size=(12, 10)):
        self.extent = extent
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.central_longitude = central_longitude
        self.fig_size = fig_size
        self.dpi = dpi
        self.fig = plt.figure(figsize=fig_size, dpi=dpi)
        self.ax = self.fig.add_axes((0, 0, 1, 1), projection=crs.PlateCarree(central_longitude=central_longitude))
        self.ax.set_extent(extent, crs=crs.PlateCarree())
        self.sub_poss = ["left", "right"]
        self.review_number = "GS(2024)0650号"
        self.sub_ax = None

    def __init_chn_map(self, add_chn_border=True, add_province=True, add_city=False, add_cnty=False,
                       single_province=None, line_color="black", sub_ax=None):
        """
        绘制全国地图
        :param add_province:
        :param add_city:
        :param add_cnty:
        :param single_province:
        :return:
        """
        if sub_ax is None:
            sub_ax = self.ax
        z_order = 6
        map_cfg = Path(static_cfg, "chn")
        if add_province:
            province_json = Path(map_cfg, "chn_province.geojson")
            province_data = gpd.read_file(province_json)
            province_data.plot(linewidths=1, zorder=z_order, ax=sub_ax, facecolor="None", edgecolor=line_color,
                               transform=crs.PlateCarree())

        if add_chn_border:
            border_json = Path(map_cfg, "chinaGJ.json")
            border_data = gpd.read_file(border_json)
            border_data.plot(linewidths=0.6, zorder=z_order, ax=sub_ax, facecolor="None", edgecolor=line_color,
                             transform=crs.PlateCarree())

        if add_city:
            city_json = Path(map_cfg, "chn_city.geojson")
            city_data = gpd.read_file(city_json)
            city_data.plot(linewidths=0.4, zorder=z_order, ax=sub_ax, facecolor="None", edgecolor=line_color,
                           transform=crs.PlateCarree())
        if add_cnty:
            cnty_json = Path(map_cfg, "chn_cnty.geojson")
            cnty_data = gpd.read_file(cnty_json)
            cnty_data.plot(linewidths=0.2, zorder=z_order, ax=sub_ax, facecolor="None", edgecolor=line_color,
                           transform=crs.PlateCarree())
        if single_province is not None:
            province_json = Path(map_cfg, "chn_province.geojson")
            province_data = gpd.read_file(province_json)

            city_json = Path(map_cfg, "chn_city.geojson")
            city_data = gpd.read_file(city_json)

            province_data = province_data[province_data["name"] == single_province]
            city_data = gpd.sjoin(city_data, province_data, how="inner", predicate="within")

            province_data.plot(linewidths=2, zorder=z_order, ax=sub_ax, facecolor="None", edgecolor=line_color,
                               transform=crs.PlateCarree())
            city_data.plot(linewidths=1, zorder=z_order, ax=sub_ax, facecolor="None", edgecolor=line_color,
                           transform=crs.PlateCarree())

    def __init_glb_map(self, add_coastline=False, add_lake=False, add_river=False, add_land=False,
                       add_ocean=False, ocean_color="#aadaff", land_color="#ffffff", land_order=3, ocean_order=2,
                       sub_ax=None):
        """
        初始化全球地图
        :return:
        """
        if sub_ax is None:
            sub_ax = self.ax
        if add_coastline:
            sub_ax.coastlines(resolution="50m", zorder=land_order, color="black")
        if add_lake:
            sub_ax.add_feature(cfeature.LAKES, alpha=0.5, zorder=ocean_order, facecolor=ocean_color, edgecolor="black")
        if add_ocean:
            sub_ax.add_feature(cfeature.OCEAN, zorder=ocean_order, facecolor=ocean_color, edgecolor="black")
        if add_river:
            sub_ax.add_feature(cfeature.RIVERS, zorder=ocean_order, facecolor=ocean_color, edgecolor="black")
        if add_land:
            sub_ax.add_feature(cfeature.LAND, zorder=land_order, facecolor=land_color, edgecolor="black")

    def init_map(self, axis_label_size=16, chn_kwargs: dict = None, glb_kwargs: dict = None):
        """
        初始化地图
        :param axis_label_size:
        :param chn_kwargs:
        :param glb_kwargs:
        :return:
        """
        if chn_kwargs is None:
            chn_kwargs = dict(add_chn_border=True, add_province=True, add_city=False, add_cnty=False,
                              single_province=None,
                              line_color="black")
        self.__init_chn_map(**chn_kwargs)
        if glb_kwargs is None:
            glb_kwargs = dict()
        self.__init_glb_map(**glb_kwargs)
        self.__set_x_y_axis(label_size=axis_label_size)

    def contourf(self, grid_data: GridData, levels, colors=None, cmap=None, z_order=2, alpha=0.85, sub_ax=None,
                 clip=True):
        """
        绘制等值面图
        :param clip:
        :param sub_ax:
        :param grid_data:
        :param levels:
        :param colors:
        :param cmap:
        :param z_order:
        :param alpha:
        :return:
        """
        if sub_ax is None:
            sub_ax = self.ax
        if clip:
            grid_data = self.__interp_data_for_extent(grid_data, ax=sub_ax)
        if cmap is not None:
            sub_ax.contourf(grid_data.longitudes, grid_data.latitudes, grid_data.values, levels=levels,
                            cmap=cmap, extend="neither", zorder=z_order, transform=crs.PlateCarree(), alpha=alpha)

        else:
            if levels == "#ffffff":
                sub_ax.contourf(grid_data.longitudes, grid_data.latitudes,
                                grid_data.values, levels=levels[1:],
                                colors=colors[1:], extend="neither", zorder=z_order,
                                transform=crs.PlateCarree(), alpha=alpha)

            else:
                sub_ax.contourf(grid_data.longitudes, grid_data.latitudes,
                                grid_data.values, levels=levels,
                                colors=colors, extend="neither", zorder=z_order,
                                transform=crs.PlateCarree(), alpha=alpha)

    def add_default_title(self, title, report_time, cst_hour):
        left = (f"起报时间:{report_time:%Y-%m-%d %H:%M}+{cst_hour:03d}\n"
                f"预报时间:{report_time + timedelta(hours=cst_hour):%Y-%m-%d %H:%M}")
        bbox_props = dict(boxstyle="square", pad=0.1, fc="w", ec="0.4", alpha=0.75)
        self.set_text(0.004, 0.996, left, size=15, ha="left", va="top", bbox=bbox_props, zorder=99)
        self.set_text(0, 1.02, title, size=18, zorder=99)

    def sub_nine_map(self, sub_position="right", line_color="black", sub_offset_y=0):
        if sub_position not in self.sub_poss:
            raise Exception(str(self.sub_poss))
        pos1 = self.ax.get_position()
        sub_nine_extent = (pos1.x0, pos1.y0 + sub_offset_y, 0.12, 0.22)
        if sub_position == "right":
            sub_nine_extent = (pos1.x1 - 0.12, pos1.y0 + sub_offset_y, 0.12, 0.22)
        self.sub_ax = self.fig.add_axes(sub_nine_extent, projection=crs.PlateCarree())
        self.sub_ax.set_extent([105, 125, 0, 25])
        self.__init_chn_map(sub_ax=self.sub_ax, line_color=line_color)

    def contour(self, grid_data: GridData, levels, colors, gauss_filter=True, sigma=2, fontcolor="black", fontsize=16,
                fmt="%.1f", line_widths=1, line_styles="-", sub_ax=None, add_label=True, manual=None, **kwargs):
        """
        绘制等值线图
        :param manual:
        :param add_label:
        :param sub_ax:
        :param line_styles:
        :param grid_data:
        :param levels:
        :param colors:
        :param gauss_filter:
        :param sigma:
        :param fontcolor:
        :param fontsize:
        :param fmt:
        :param line_widths:
        :param kwargs:
        :return:
        """

        if sub_ax is None:
            sub_ax = self.ax
        grid_data = self.__interp_data_for_extent(grid_data, ax=sub_ax)
        values = grid_data.values
        if gauss_filter:
            values = ndimage.gaussian_filter(grid_data.values, sigma=sigma)

        CS = sub_ax.contour(grid_data.longitudes, grid_data.latitudes,
                            values, levels=levels, colors=colors, zorder=4, linewidths=line_widths,
                            linestyles=line_styles, transform=crs.PlateCarree(), **kwargs)

        if add_label:
            sub_ax.clabel(CS, inline=1, fontsize=fontsize, colors=fontcolor, fmt=fmt, zorder=5, manual=manual)

    def scatter(self, df_data, levels, colors, value_key="value", lat_key="lat", lon_key="lon", marker="o",
                marker_size=10, z_order=4):
        """
        绘制散点图
        :param df_data:
        :param levels:
        :param colors:
        :param value_key:
        :param lat_key:
        :param lon_key
        :param marker:
        :param marker_size:
        :param z_order:
        :return:
        """
        _l = 1
        if colors[0] == "#ffffff":
            _l = 2

        for idx in range(_l, len(levels)):
            _tmp_data = df_data[
                (df_data[value_key] >= levels[
                    idx - 1]) & (
                        df_data[value_key] <
                        levels[idx])]
            self.ax.scatter(_tmp_data[lon_key].values,
                            _tmp_data[lat_key].values,
                            marker=marker,
                            edgecolor="black",
                            linewidth=0.5, s=marker_size, alpha=1,
                            c=colors[idx - 1], transform=crs.PlateCarree(),
                            zorder=z_order)

    def __interp_data_for_extent(self, grid_data: GridData, ax=None):
        if ax is None:
            ax = self.ax
        grd_data = copy.copy(grid_data)
        extent = np.round(ax.get_extent(), 3)
        grd_data.crop(extent[2] - 1, extent[3] + 1, extent[0] - 1,
                      extent[1] + 1)
        return grd_data

    def stream(self):
        """
        绘制流场
        :return:
        """
        pass

    def wind_barbs(self, u_grd_data: GridData, v_grd_data: GridData, length=6, line_width=0.5, barb_color="blue",
                   flag_color="#111111",
                   regrid_shape=20, barb_increments=None, sub_ax=None):
        """
        绘制风向风速图
        :param line_width:
        :param sub_ax:
        :param u_grd_data:
        :param v_grd_data:
        :param length:
        :param barb_color:
        :param flag_color:
        :param regrid_shape:
        :param barb_increments:
        :return:
        """
        if sub_ax is None:
            sub_ax = self.ax
        if barb_increments is None:
            barb_increments = {'half': 2, 'full': 4, 'flag': 20}
        u_grd_data = self.__interp_data_for_extent(u_grd_data, ax=sub_ax)
        v_grd_data = self.__interp_data_for_extent(v_grd_data, ax=sub_ax)

        sub_ax.barbs(u_grd_data.longitudes,
                     u_grd_data.latitudes,
                     u_grd_data.values,
                     v_grd_data.values, length=length, barbcolor=barb_color,
                     transform=crs.PlateCarree(),
                     barb_increments=barb_increments, regrid_shape=regrid_shape, linewidth=line_width,
                     flagcolor=flag_color, zorder=3,
                     sizes=dict(emptybarb=0.0),
                     )

    def color_bar(self, levels, colors=None, cmap=None, orientation="vertical", bar_bounds_position="center",
                  color_bar_label=None, bar_bounds_name=None, extend="both", axes=None, length=1.2,
                  tick_kwargs=None):
        """
        设置颜色条
        :param length:
        :param tick_kwargs:
        :param axes:
        :param levels:
        :param colors:
        :param cmap:
        :param orientation:
        :param bar_bounds_position:
        :param color_bar_label:
        :param bar_bounds_name:
        :param extend:
        :return:
        """
        if tick_kwargs is None:
            tick_kwargs = dict(labelsize=12, size=3)
        if axes is None:
            pos1 = self.ax.get_position()
            _height = pos1.height / length
            _width = pos1.width / length
            axes = (pos1.x1 + 0.02, pos1.y0 + (pos1.height - _height) / 2, 0.02, _height)
            if orientation == "horizontal":
                axes = (pos1.x0 + (pos1.width - _width) / 2, pos1.y0 - 0.06, _width, 0.02)

        ax2 = self.fig.add_axes(axes)
        new_level = np.array(levels)
        colors = colors
        levels = levels
        if cmap is not None:
            cmap = plt.get_cmap(cmap)
        else:
            new_color = np.array(colors)

            cmap = mpl.colors.ListedColormap(new_color)
            if extend == "both":
                new_color = new_color[1:-1]
                new_level = new_level[1:-1]
                cmap = mpl.colors.ListedColormap(new_color)
                cmap.set_over(colors[len(colors) - 1])
                cmap.set_under(colors[0])

            if extend == "min":
                new_color = new_color[1:]
                new_level = new_level[1:]
                cmap = mpl.colors.ListedColormap(new_color)
                cmap.set_under(colors[0])

            if extend == "max":
                new_color = new_color[0:-1]
                new_level = new_level[0:-1]
                cmap = mpl.colors.ListedColormap(new_color)
                cmap.set_over(colors[len(colors) - 1])

        bounds = new_level

        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                        norm=norm,
                                        boundaries=bounds,
                                        extend=extend,
                                        extendfrac='auto',
                                        orientation=orientation)

        cb2.ax.tick_params(**tick_kwargs)
        if color_bar_label is not None:
            cb2.set_label(color_bar_label, labelpad=-0.1, fontdict={"size": "20"})

        if bar_bounds_name is not None:
            loc = []
            if bar_bounds_position == "center":
                loc = [np.nanmean([levels[idx], levels[idx + 1]]) for idx in range(len(levels) - 1)]
            if bar_bounds_position == "bottom":
                loc = copy.copy(levels)

            cb2.locator = mpl.ticker.FixedLocator(loc)
            cb2.formatter = mpl.ticker.FixedFormatter(bar_bounds_name)
        cb2.update_ticks()

    def add_more_color_bar(self, param, gap=0.01, scale=9):
        pos1 = self.ax.get_position()
        all_height = pos1.height / 10 * scale
        _height = all_height / len(param)
        for idx, par in enumerate(param):
            axes = [pos1.x1 + 0.02, (pos1.y0 + (pos1.height - all_height) / 2) + _height * idx + gap, 0.02,
                    _height - gap]
            color_bar_label = None
            bar_bounds_name = None
            extend = "both"
            if "extend" in par.keys():
                extend = par["extend"]
            if "color_bar_label" in par.keys():
                color_bar_label = par["color_bar_label"]
            if "bar_bounds_name" in par.keys():
                bar_bounds_name = par["bar_bounds_name"]
            self.color_bar(colors=par["colors"], levels=par["levels"], color_bar_label=color_bar_label, extend=extend,
                           bar_bounds_name=bar_bounds_name, axes=axes)

    def clip_path(self):
        pass

    def legend(self):
        pass

    def __set_x_y_axis(self, label_size=12):
        """
        设置x轴和y轴的刻度
        :return:
        """
        x_ticks = np.arange(self.extent[0], self.extent[1] + 1, self.x_scale).tolist()
        y_ticks = np.arange(self.extent[2], self.extent[3] + 1, self.y_scale).tolist()
        self.ax.set_xticks(x_ticks[1:], crs=crs.PlateCarree())
        self.ax.set_yticks(y_ticks, crs=crs.PlateCarree())
        self.ax.tick_params(labelcolor='#2b2b2b', labelsize=label_size, width=0.5, top=False, right=False)
        # zero_direction_label用来设置经度的0度加不加E和W
        lon_formatter = LongitudeFormatter(zero_direction_label=False, degree_symbol="$^{\circ}$")
        lat_formatter = LatitudeFormatter(degree_symbol="$^{\circ}$")
        self.ax.xaxis.set_major_formatter(lon_formatter)
        self.ax.yaxis.set_major_formatter(lat_formatter)

    def set_title(self, y, title, family="helvetica", size=22):
        """
        设置标题
        :param size:
        :param family:
        :param y:
        :param title:
        :return:
        """
        font_family = {
            "family": family,
            "size": size,
        }
        self.ax.set_title(title, y=y, fontdict=font_family, transform=self.ax.transAxes)

    def set_text(self, x, y, text, **kwargs):
        """
        设置文字
        :param x:
        :param y:
        :param text:
        :param kwargs:
        :return:
        """
        self.ax.text(x, y, text, transform=self.ax.transAxes, **kwargs)

    def save_file(self, save_path):
        """
        保存图片
        :param save_path:
        :return:
        """
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        self.fig.savefig(save_path, bbox_inches="tight", pad_inches=0.15)

    def __del__(self):
        try:
            plt.close(self.fig)
        except Exception:
            ...

    def set_review_number(self, font_size=12):
        bbox_props = dict(boxstyle="round", pad=0.4, fc="w", edgecolor="None", alpha=0.7)
        self.ax.text(0.014, 0.024, f"审图号：{self.review_number}", zorder=8, ha="left", va="center", bbox=bbox_props,
                     transform=self.ax.transAxes,
                     fontdict=dict(size=font_size, ))
