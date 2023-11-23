#!/usr/bin/env python

from netCDF4 import Dataset
from datetime import datetime, timedelta
import  numpy as np
import sys
import WithDatabase
import Withfiles
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata


def Principal_Menu():
    while True:
        print('Select option:')
        print('1. Extract Temperature data from netcdf file')
        print('2. Insert in databse temperature data')
        print('3. Obtain sea surface temperature on the coast')
        print('4. Insert in database sea surface Temperature on the coast')
        print('5. Calculate thermal efficiency')
        print('6. Insert in database thermal efficiency')
        print('7. Generate Maximum Efficiency Map')
        print('8. Exit')
        option = input('option: ')
        if option == '1':
            Temperature_Parameters()
        else:
            if option == '2':
                Insert_Temperature()
            else:
                if option == '3':
                    InitialPoints_Parameters()
                else:
                    if option == '4':
                        Insert_Initial_Points()
                    else:
                        if option == '5':
                            EfficiencyParameters()
                        else:
                            if option == '6':
                                Insert_Efficiency()
                            else:
                                if option == '7':
                                    Maps_Parameters()
                                else:
                                    if option == '8':
                                        sys.exit()
                                    else:
                                        print('Invalid option, try again')


def Temperature_Parameters():
    print('Parameters for Temperature')
    file_input_dir = input('File input address: ')
    file_ouput_dir = input('File output address: ')
    depth_level = int(input('Depth level netcdf file (0, 1, 2, ... ): '))
    WithTemperature(depth_level, file_input_dir, file_ouput_dir)

def InitialPoints_Parameters():
    print('Parameters for Initial Points')
    file = input('Geographic coordinates file: ')
    file_ouput_dir = input('File output address: ')
    year = int(input('Write year: '))
    north = int(input('Calculation orientation:' + '\n' + '0 for north-south orientation.' + '\n' + '1 for south-north orientation.' + '\n' + '2 for west-east orientation.' + '\n' + '3 for east-west orientation.: '))
    WithInitialPoints(file, year, file_ouput_dir, north)

def Maps_Parameters():
    print('Parameters for maps')
    ini = input('From (Date format yyyy-mm-dd): ')
    end = input('Until (Date format: yyyy-mm-dd): ')
    depth = float(input('Depth in meters: '))
    file_ouput_dir = input('File output address: ')
    WithMaps(ini, end, depth, file_ouput_dir)

def WithMaps(ini, end, depth, fileout):
    c = WithDatabase.LoadEfficiencyData(ini, end, depth)

    x = []
    y = []
    z = []

    for tupla in c:
        temx = float(tupla[0])
        temy = float(tupla[1])
        temz = float(tupla[2])
        x.append(temx)
        y.append(temy)
        z.append(temz)

    # This is the study area for Cuba
    lons = np.arange(-85.5, -73.5, 0.001)
    lats = np.arange(19.5, 23.5, 0.001)

    xx, yy = np.meshgrid(lons, lats)
    points = np.column_stack((x, y))
    zz = griddata(np.array(points), np.array(z), (xx, yy), method='linear')

    region_coords = (-85.5, 18.5, -73.5, 23.5)

    fig = plt.figure(1, figsize=(12, 12), dpi=500)
    ax = fig.add_subplot(111)

    m = Basemap(resolution='h', llcrnrlon=region_coords[0], llcrnrlat=region_coords[1], urcrnrlon=region_coords[2],
                urcrnrlat=region_coords[3], projection='lcc', lat_0=21.4, lon_0=-83.1, area_thresh=50.)

    m.drawparallels(np.arange(region_coords[1], region_coords[3] + 1, 1), labels=[1, 1, 0, 0], zorder=1)
    m.drawmeridians(np.arange(region_coords[0], region_coords[2], 1), labels=[0, 0, 0, 1], zorder=1)
    x, y = m(xx, yy)
    m.drawmapscale(-84.2, 18.8, -80.1, 19.2, 200, barstyle='fancy')

    m.drawcoastlines()
    clevs = [0.625, 0.650, 0.675, 0.700, 0.725, 0.750, 0.775, 0.800, 0.825, 0.850]

    cs = m.contourf(x, y, zz, clevs, cmap=(plt.get_cmap('jet')))
    cs.cmap.set_over('darkred')
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label('Thermal Efficiency')
    m.fillcontinents(color='gray')

    plt.title('Mean Thermal Efficiency from %s to %s, at depth %s m' % (ini, end, depth))
    plt.savefig(fileout)

    plt.show()


def Insert_Temperature():
    file_ouput_dir = input('File output address: ')
    print('Inserting Temperature')
    WithDatabase.Insert_Temperature(file_ouput_dir)

def Insert_Efficiency():
    file_ouput_dir = input('File output address: ')
    print('Inserting Maximum Efficiency')
    WithDatabase.Insert_MaxEfficiency(file_ouput_dir)

def Insert_Initial_Points():
    file_ouput_dir = input('File output address: ')
    print('Inserting Initial Points')
    WithDatabase.Insert_InitialPoints(file_ouput_dir)



def EfficiencyParameters():
    print('Parameters for Thermal Efficiency')
    year = input('Write year: ')
    depth = float(input('Depth in meters: '))
    file_ouput_dir = input('File output address: ')
    north = int(input('Calculation orientation:' + '\n' + '0 for north-south orientation.' + '\n' + '1 for orientation south-north.' + '\n' + '2 for west-east orientation.' + '\n' + '3 for east-west orientation.: '))
    WithEfficiency(north, year, depth, file_ouput_dir)


def EfficiencyCalculation(t1,t2):
    return (t1 - t2)/t1

def WithEfficiency(north, year, depth, fileout):
    pointsN = WithDatabase.LoadCoastalPoints(north, depth, year)

    days = []
    lon = []
    lat = []
    t1 = []
    t2 = []

    days1 = []
    lon1 = []
    lat1 = []
    t11 = []
    t21 = []

    for pointN in pointsN:
        days.append(pointN[0])
        lon.append(pointN[1])
        lat.append(pointN[2])
        t1.append(pointN[3])
        t2.append(pointN[4])
        print('Point added')


    var = np.column_stack((days, lon, lat, t1, t2))

    for list in var:
        if list[4] != -32767:
            e = EfficiencyCalculation(float(list[3]), float(list[4]))
        else:
            e = -32767
        Withfiles.SaveMaxEficiency(list[0], depth, list[1], list[2], e, fileout)



def WithInitialPoints(file, year, file_out, north):
    # For Cuba, these are the points from the coast that match the mesh longitude values
    points = open(file, 'r')

    days = []
    lon = []
    lat = []
    t = []
    position = []

    for point in points:
        lon_point = float(point.split(',')[0])
        lat_point = float(point.split(',')[1])
        pointlist = WithDatabase.SelectInitialTemperature(0.494025, year)

        for list1 in pointlist:
            if lon_point == round(list1[1], 4) and lat_point == round(list1[2], 4):
                if list1[3] > 0:
                    days.append(list1[0])
                    lon.append(list1[1])
                    lat.append(list1[2])
                    t.append(list1[3])
                    position.append(north)
                    print
                    'added point'

    var = np.column_stack((days, lon, lat, t, position))

    for list in var:
        Withfiles.SaveInitialPoints(list[0], list[1], list[2], list[3], list[4] , file_out)


def WithTemperature(dd, fileread_dir, fileout_dir):
    fileread = Dataset(fileread_dir)
    lon_dim = fileread.dimensions['longitude'].size
    lat_dim = fileread.dimensions['latitude'].size
    time_dim = fileread.dimensions['time'].size
    for pp in range(0, time_dim):
        T = fileread.variables['to'][pp, dd, :]
        lat = fileread.variables['latitude'][:]
        lon = fileread.variables['longitude'][:]
        depth = fileread.variables['depth'][dd]
        hourss = int(fileread.variables['time'][pp])
        lat1 = []
        lon1 = []
        for q in range(0, lat_dim):
            lon1 = np.append(lon1, lon)
            for p in range(0, lon_dim):
                lat1 = np.append(lat1, lat[q])
        T = T.flatten()
        table = np.column_stack((lon1, lat1, T))
        date = datetime(1950, 1, 1, 00, 00, 00) + timedelta(hours=hourss)
        for row in table:
            Withfiles.SaveTemperature(date, depth, row[0], row[1], row[2], fileout_dir)

    fileread.close()



if __name__=='__main__':
    Principal_Menu()
