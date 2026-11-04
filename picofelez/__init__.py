from decouple import config

if not config('DEBUG', default=False, cast=bool):
    import pymysql

    pymysql.version_info = (2, 2, 1, "final", 0)
    pymysql.install_as_MySQLdb()