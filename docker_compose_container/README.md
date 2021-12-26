docker_compose_container
========================

Take your docker-compose project and bundle it into a single container 
with a specific version and no port conflicts.

All downloads of all containers used by the docker-compose are stored 
in the outer container so that there is only one download while building
and not while starting the contianer the first time, which is quite 
unpredictable. Also everything is packed together and testable, so you can
be sure, that it works.
