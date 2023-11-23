def SaveTemperature(fecha, depth, lon, lat, temp, file_out):
	#The temperature txt file is saved, to be imported into the database
    texto = open(file_out,'a')
    texto.write (str(fecha) + ',' + str(depth) + ',' + str(lon) + ',' + str(lat) + ',' + str(temp) + '\n')
    texto.close()

    print(fecha, depth, lat, lon, temp, 'Saved Record')

def SaveInitialPoints(fecha, lon, lat, temp, norte, file_out):
    texto = open(file_out,'a')
    texto.write(str(fecha) + ',' + str(lon) + ',' + str(lat) + ',' + str(temp) + ',' + str(norte) + '\n')
    texto.close()

    print(fecha, lon, lat, temp, norte, 'Saved Record')

def SaveMaxEficiency(fecha, lev, lon, lat, e, fileout):
    year = str(fecha)
    texto = open(fileout,'a')
    texto.write(str(fecha) + ',' + str(lev) + ',' + str(lon) + ',' + str(lat) + ',' + str(e) + '\n')
    texto.close()
    print(fecha, lev, lon, lat, e, 'Safe Record')
