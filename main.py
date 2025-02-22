import uvicorn

from service.web import app, config


def main():
    uvicorn.run(app, host=config.server.host, port=config.server.port)


if __name__ == "__main__":
    main()
