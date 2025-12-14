class AppError(Exception):
    pass

class ParseError(AppError):
    pass

class ValidationError(AppError):
    pass
