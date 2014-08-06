set +o errexit
createuser -s geo
createdb -U geo -O geo geo -T template0
psql -U geo -d geo -c "CREATE EXTENSION postgis;"