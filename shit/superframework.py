from fastapi import FastAPI

my_incredible_application = FastAPI()


@my_incredible_application.get('/')
def read_root():
    return {'Hello': 'FastAPI'}
