class Urls:
    MAIN_URL = 'https://stellarburgers.education-services.ru/api/'

    REGISTER_USER = f'{MAIN_URL}auth/register'
    LOGIN_USER = f'{MAIN_URL}auth/login'
    DELETE_USER = f'{MAIN_URL}auth/user'
    CREATE_ORDER = f'{MAIN_URL}orders'
    GET_INGREDIENTS = f'{MAIN_URL}ingredients'