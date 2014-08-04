set +o errexit
createuser -s geo
createdb -U geo -O geo geo -T template0
psql -U geo -d geo -c "CREATE EXTENSION postgis;"

export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal