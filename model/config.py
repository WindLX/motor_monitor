from pydantic import BaseModel


class WebServerConfig(BaseModel):
    host: str
    port: int


class UdpNodeConfig(BaseModel):
    host: str
    port: int


class DownstreamConfig(BaseModel):
    host: str
    port: int


class Config(BaseModel):
    web_server: WebServerConfig
    udp_node: UdpNodeConfig
    downstream: DownstreamConfig
