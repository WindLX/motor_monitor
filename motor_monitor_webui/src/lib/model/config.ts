export interface WebServerConfig {
  host: string;
  port: number;
}

export interface UdpNodeConfig {
  host: string;
  port: number;
}

export interface DownstreamConfig {
  host: string;
  port: number;
}

export interface Config {
  web_server: WebServerConfig;
  udp_node: UdpNodeConfig;
  downstream: DownstreamConfig;
}
