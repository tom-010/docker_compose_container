from pprint import pprint
import yaml
import sys
from yaml.representer import Representer
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.resolver import Resolver
import os


def dump_to_stdout(docker_compose):
    class MyRepresenter(Representer):
        def represent_none(self, data):
            return self.represent_scalar(u'tag:yaml.org,2002:null',
                                    u'')
    class MyDumper(Emitter, Serializer, MyRepresenter, Resolver):
        def __init__(self, stream,
                default_style=None, default_flow_style=None,
                canonical=None, indent=None, width=None,
                allow_unicode=None, line_break=None,
                encoding=None, explicit_start=None, explicit_end=None,
                version=None, tags=None, **kwargs):
            Emitter.__init__(self, stream, canonical=canonical,
                    indent=indent, width=width,
                    allow_unicode=allow_unicode, line_break=line_break)
            Serializer.__init__(self, encoding=encoding,
                    explicit_start=explicit_start, explicit_end=explicit_end,
                    version=version, tags=tags)
            MyRepresenter.__init__(self, default_style=default_style,
                    default_flow_style=default_flow_style)
            Resolver.__init__(self)
    MyRepresenter.add_representer(type(None), MyRepresenter.represent_none)
    yaml.dump(docker_compose, stream=sys.stdout, Dumper=MyDumper, default_flow_style=False)

# if a port is present here as key, it stays public but is 
# replaced by the value. Say, a container like nginx publishes
# port 80 and PUBLIC_PORTS="8081:80", then the port 80 of nginx
# will be replaced by 8081 
port_mappings = {}
public_ports = os.environ.get('PORTS', '').split(',')
for port in public_ports:
    if not port:
        continue
    if ':' in port:
        host, container = port.split(':')
    else:
        host, container = port, port
    host = int(host)
    container=int(container)
    port_mappings[container] = host


docker_compose = yaml.safe_load(sys.stdin)
for service_name, service in docker_compose['services'].items():
    expose = set(service.get('expose', []))
    public_ports = set()
    ports = service.get('ports')
    if not ports:
        continue
    for port in ports:
        if ':' in port:
            host_port, container_port = port.split(':')
        else:
            host_port, container_port = port, port 

        host_port = int(host_port)
        container_port = int(container_port)

        expose.add(container_port)

        if host_port in port_mappings.keys():
            new_host_port = port_mappings[host_port]
            public_ports.add(str(new_host_port) + ':' + str(container_port))

    docker_compose['services'][service_name]['expose'] = list(expose)
    if public_ports:
        docker_compose['services'][service_name]['ports'] = list(public_ports)
    elif docker_compose['services'][service_name].get('ports'):
        del docker_compose['services'][service_name]['ports']


dump_to_stdout(docker_compose)

#####


