import yaml


from server.tcp import TCPServer
from server.udp import UDPServer

def load_config():
    with open("server_conf.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():

    config = load_config()
    
    if config["type"] == "tcp":
        server = TCPServer(config)
    elif config["type"] == "udp":
        server = UDPServer(config)
    else:
        raise ValueError("Invalid server type")
    for _ in server.run():
        pass

if __name__ == "__main__":
    main()
