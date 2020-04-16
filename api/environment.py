import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env()
