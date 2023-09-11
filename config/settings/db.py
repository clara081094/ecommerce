from .base import env

POSTGRESQL = {
    "default": {
        "ENGINE": env.str("DRIVER"),
        "NAME": env.str("NAME"),
        "USER": env.str("USER_DB"),
        "PASSWORD": env.str("PASSWORD"),
        "HOST": env.str("HOST"),
        "PORT": env.str("PORT")
    },
}