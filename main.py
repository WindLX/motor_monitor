import uvicorn

from service.web import app, config


def main():
    uvicorn.run(app, host=config.web_server.host, port=config.web_server.port)


if __name__ == "__main__":
    main()
