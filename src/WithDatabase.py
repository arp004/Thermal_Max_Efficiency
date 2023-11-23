import psycopg2


connection = psycopg2.connect(database="Termica", user="postgres", password="1111", host="10.0.5.244", port="5432")

def Insert_Temperature(file):
    cursor = connection.cursor()
    with open(file, 'r') as f:
        cursor.copy_from(f,'public."Temperature"', sep= ',')
    connection.commit()
    cursor.close()

def SelectInitialTemperature(level, year):
    cursor = connection.cursor()
    sql = 'SELECT day, longitude, latitude,"T" FROM public."Temperature" WHERE "lev" = %s And EXTRACT(YEAR FROM day) = %s;'
    cursor.execute(sql, (level, year))
    num = cursor.fetchall()
    cursor.close()
    return num

def Insert_MaxEfficiency(file):
    cursor = connection.cursor()
    with open(file) as f:
        cursor.copy_from(f, 'public."Eficiency"', sep=',')
    connection.commit()
    cursor.close()

def Insert_InitialPoints(file):
    cursor = connection.cursor()
    with open(file) as f:
        cursor.copy_from(f, 'public."InitialPoints"', sep=',')
    connection.commit()
    cursor.close()

def LoadCoastalPoints(north, lev, year):
    sql = 'SELECT DISTINCT "Temperature".day, "Temperature".longitude, "Temperature".latitude, "InitialPoints"."T" AS T1, "Temperature"."T" AS T2 FROM public."Temperature" INNER JOIN public."InitialPoints" ON "InitialPoints".day = "Temperature".day WHERE "Temperature".latitude > "InitialPoints".latitude AND "Temperature".longitude = "InitialPoints".longitude AND "InitialPoints"."Norte" = %s AND "Temperature".lev = %s AND EXTRACT(YEAR FROM public."Temperature".day) = %s;'
    if north == '0':
        sql = 'SELECT DISTINCT "Temperature".day, "Temperature".longitude, "Temperature".latitude, "InitialPoints"."T" AS T1, "Temperature"."T" AS T2 FROM public."Temperature" INNER JOIN public."InitialPoints" ON "InitialPoints".day = "Temperature".day WHERE "Temperature".latitude < "InitialPoints".latitude AND "Temperature".longitude = "InitialPoints".longitude AND "InitialPoints"."Norte" = %s AND "Temperature".lev = %s AND EXTRACT(YEAR FROM public."Temperature".day) = %s;'
    else:
        if north == '2':
            sql = 'SELECT DISTINCT "Temperature".day, "Temperature".longitude, "Temperature".latitude, "InitialPoints"."T" AS T1, "Temperature"."T" AS T2 FROM public."Temperature" INNER JOIN public."InitialPoints" ON "InitialPoints".day = "Temperature".day WHERE "Temperature".longitude > "InitialPoints".longitude AND "Temperature".latitude = "InitialPoints".latitude AND "InitialPoints"."Norte" = %s AND "Temperature".lev = %s AND EXTRACT(YEAR FROM public."Temperature".day) = %s;'
        else:
            if north == '3':
                sql = 'SELECT DISTINCT "Temperature".day, "Temperature".longitude, "Temperature".latitude, "InitialPoints"."T" AS T1, "Temperature"."T" AS T2 FROM public."Temperature" INNER JOIN public."InitialPoints" ON "InitialPoints".day = "Temperature".day WHERE "Temperature".longitude < "InitialPoints".longitude AND "Temperature".latitude = "InitialPoints".latitude AND "InitialPoints"."Norte" = %s AND "Temperature".lev = %s AND EXTRACT(YEAR FROM public."Temperature".day) = %s;'

    cursor = connection.cursor()
    cursor.execute(sql, (north, lev, year))
    num = cursor.fetchall()
    cursor.close()
    return num

def LoadEfficiencyData(ini, end, depth):
    cursor = connection.cursor()
    sql = 'SELECT longitude, latitude, AVG(e) FROM public."Eficiency" WHERE (day >= %s AND day <= %s) AND lev = %s GROUP BY longitude, latitude ORDER BY longitude, latitude;'
    cursor.execute(sql,(ini, end, depth))
    num = cursor.fetchall()
    cursor.close()
    return num
