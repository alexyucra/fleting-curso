
DATABASE = {
    "ENGINE": "sqlite",  # sqlite | mysql

    "SQLITE": {
        "PATH": "data/fleting.db"
    },

    "MYSQL": {
        "HOST": "localhost",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "",
        "NAME": "fleting",
        "OPTIONS": {
            "charset": "utf8mb4"
        }
    }
}
