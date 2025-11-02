import warnings

# Silenciar deprecations de terceros (argon2, pydantic v2 ya lo corregiste)
warnings.filterwarnings(
    "ignore",
    message="Accessing argon2.__version__ is deprecated",
    category=DeprecationWarning,
    module="passlib.handlers.argon2",
)
