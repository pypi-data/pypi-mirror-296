import os
import random
import socket
import logging

from string import digits, ascii_letters
import docker
from foundation.utils.swarm import Swarm
from foundation.workers import select_worker

WORKER_NAME = "{}-worker"


########################################################################
class Workers:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, swarm=None, swarm_advertise_addr=None):
        """Constructor"""

        if (swarm_advertise_addr) and (swarm is None):
            self.swarm = Swarm(advertise_addr=swarm_advertise_addr)
        elif (swarm_advertise_addr is None) and (swarm):
            self.swarm = swarm
        else:
            self.swarm = Swarm()

    # ----------------------------------------------------------------------
    def gen_worker_name(self, length=8):
        """"""
        id_ = "".join(
            [random.choice(ascii_letters + digits) for _ in range(length)]
        )
        if not WORKER_NAME.format(id_) in self.swarm.services:
            return WORKER_NAME.format(id_)
        return self.gen_worker_name(length)

    # ----------------------------------------------------------------------
    def get_open_port(
        self,
    ):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    # ----------------------------------------------------------------------
    def stop_all_workers(self):
        """"""
        for worker in self.swarm.services:
            if worker.endswith(WORKER_NAME.format("")):
                self.swarm.stop_service(worker)

    # ----------------------------------------------------------------------
    def start_django_worker(
        self,
        worker_path,
        service_name=None,
        port=None,
        restart=False,
        image='djangoship',
        tag=None,
        endpoint='',
        env={},
        mounts=None,
        request_ports={},
    ):
        """"""
        if tag == None and image == 'djangoship':
            tag = '1.4'
        if tag == None and image == 'djangorun':
            tag = '1.1'

        if os.path.isabs(worker_path) or os.path.exists(worker_path):
            worker_path = os.path.abspath(worker_path)
            app_name = os.path.split(worker_path)[-1]
        elif os.path.exists(select_worker(worker_path)):
            app_name = worker_path
            service_name = WORKER_NAME.format(worker_path.replace("_", "-"))
            worker_path = select_worker(worker_path)
        else:
            logging.warning(f"Service {worker_path} doesn't exits.")
            return

        if port is None:
            port = self.get_open_port()

        if service_name is None:
            service_name = self.gen_worker_name()
        else:
            service_name = WORKER_NAME.format(service_name)
        service_name_env = os.path.split(worker_path)[-1]

        if restart and (service_name in self.swarm.services):
            self.swarm.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.swarm.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        endpoint_spec_ports = []
        env_ports = {}
        for port_env in request_ports:
            port_ = request_ports[port_env]
            if port_ is None:
                port_ = self.get_open_port()
            endpoint_spec_ports.append(
                {
                    'Protocol': 'tcp',
                    'PublishedPort': port_,
                    'TargetPort': port_,
                }
            )
            env_ports[port_env] = port_

        docker_mounts = []
        if mounts:
            for source, target in mounts:

                docker_mounts.append(
                    docker.types.Mount(
                        type='bind', source=source, target=target
                    )
                )

        service = self.swarm.client.services.create(
            image=f"dunderlab/{image}:{tag}",
            name=service_name,
            networks=self.swarm.networks,
            hosts=self.swarm.extra_host(),
            endpoint_spec={
                'Ports': [
                    {
                        'Protocol': 'tcp',
                        'PublishedPort': port,
                        'TargetPort': 80,
                    },
                    *endpoint_spec_ports,
                ]
            },
            mounts=[
                docker.types.Mount(
                    type="bind",
                    source=worker_path,
                    target=f"/app/{image}",
                    read_only=False,
                ),
                docker.types.Mount(
                    type="bind",
                    source="/var/run/docker.sock",
                    target="/var/run/docker.sock",
                ),
                *docker_mounts,
            ],
            env={
                "DJANGOPROJECT": app_name,
                "PORT": port,
                "ENDPOINT": endpoint,
                "SERVICE_NAME": service_name_env,
                "WORKER_NAME": service_name,
                **env_ports,
                **env,
            },
        )

        return port

    # ----------------------------------------------------------------------
    def start_brython_worker(
        self,
        worker_path,
        service_name=None,
        port=None,
        run="main.py",
        restart=False,
        tag='1.1',
        env={},
        mounts=None,
        request_ports={},
    ):
        """"""
        if os.path.isabs(worker_path) or os.path.exists(worker_path):
            worker_path = os.path.abspath(worker_path)
        elif os.path.exists(select_worker(worker_path)):
            service_name = WORKER_NAME.format(worker_path.replace("_", "-"))
            worker_path = select_worker(worker_path)

        if port is None:
            port = self.get_open_port()

        if service_name is None:
            service_name = self.gen_worker_name()
        else:
            service_name = WORKER_NAME.format(service_name)
        service_name_env = os.path.split(worker_path)[-1]

        if restart and (service_name in self.swarm.services):
            self.swarm.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.swarm.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        endpoint_spec_ports = []
        env_ports = {}
        for port_env in request_ports:
            port_ = request_ports[port_env]
            if port_ is None:
                port_ = self.get_open_port()
            endpoint_spec_ports.append(
                {
                    'Protocol': 'tcp',
                    'PublishedPort': port_,
                    'TargetPort': port_,
                }
            )
            env_ports[port_env] = port_

        docker_mounts = []
        if mounts:
            for source, target in mounts:

                docker_mounts.append(
                    docker.types.Mount(
                        type='bind', source=source, target=target
                    )
                )

        service = self.swarm.client.services.create(
            image=f"dunderlab/python312:{tag}",
            name=service_name,
            networks=self.swarm.networks,
            hosts=self.swarm.extra_host(),
            command=[
                "/bin/bash",
                "-c",
                # f"if [ -f \"/app/worker/requirements.txt\" ]; then pip install --root-user-action=ignore -r /app/worker/requirements.txt; fi && startup.sh && python /app/worker/{run}",
                f"ntpd -g && if [ -f \"/app/worker/requirements.txt\" ]; then pip install --root-user-action=ignore -r /app/worker/requirements.txt; fi && if [ -f \"/app/worker/startup.sh\" ]; then /app/worker/startup.sh; fi && python /app/worker/{run}",
            ],
            endpoint_spec={
                'Ports': [
                    {
                        'Protocol': 'tcp',
                        'PublishedPort': port,
                        'TargetPort': port,
                    },
                    *endpoint_spec_ports,
                ]
            },
            mounts=[
                docker.types.Mount(
                    type="bind",
                    source=worker_path,
                    target="/app/worker",
                    read_only=False,
                ),
                docker.types.Mount(
                    type="bind",
                    source="/var/run/docker.sock",
                    target="/var/run/docker.sock",
                ),
                *docker_mounts,
            ],
            env={
                # "STREAM": port_stream,
                "RADIANT": port,
                "PORT": port,
                "SERVICE_NAME": service_name_env,
                "WORKER_NAME": service_name,
                **env_ports,
                **env,
            },
        )

        return port

    # ----------------------------------------------------------------------
    def start_python_worker(
        self,
        worker_path,
        service_name=None,
        port=None,
        run="main.py",
        restart=False,
        tag='1.1',
        env={},
        mounts=None,
        request_ports={},
    ):
        """"""
        if os.path.isabs(worker_path) or os.path.exists(worker_path):
            worker_path = os.path.abspath(worker_path)
        elif os.path.exists(select_worker(worker_path)):
            service_name = WORKER_NAME.format(worker_path.replace("_", "-"))
            worker_path = select_worker(worker_path)

        if port is None:
            port = self.get_open_port()

        if service_name is None:
            service_name = self.gen_worker_name()
        else:
            service_name = WORKER_NAME.format(service_name)
        service_name_env = os.path.split(worker_path)[-1]

        if restart and (service_name in self.swarm.services):
            self.swarm.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.swarm.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        endpoint_spec_ports = []
        env_ports = {}
        for port_env in request_ports:
            port_ = request_ports[port_env]
            if port_ is None:
                port_ = self.get_open_port()
            endpoint_spec_ports.append(
                {
                    'Protocol': 'tcp',
                    'PublishedPort': port_,
                    'TargetPort': port_,
                }
            )
            env_ports[port_env] = port_

        docker_mounts = []
        if mounts:
            for source, target in mounts:

                docker_mounts.append(
                    docker.types.Mount(
                        type='bind', source=source, target=target
                    )
                )

        service = self.swarm.client.services.create(
            image=f"dunderlab/python312:{tag}",
            name=service_name,
            networks=self.swarm.networks,
            hosts=self.swarm.extra_host(),
            command=[
                "/bin/bash",
                "-c",
                f"ntpd -g && if [ -f \"/app/worker/requirements.txt\" ]; then pip install --root-user-action=ignore -r /app/worker/requirements.txt; fi && if [ -f \"/app/worker/startup.sh\" ]; then /app/worker/startup.sh; fi && python /app/worker/{run}",
                # f"if [ -f \"/app/worker/requirements.txt\" ]; then pip install --root-user-action=ignore -r /app/worker/requirements.txt; fi && startup.sh && python /app/worker/{run}",
            ],
            endpoint_spec={
                'Ports': [
                    {
                        'Protocol': 'tcp',
                        'PublishedPort': port,
                        'TargetPort': port,
                    },
                    *endpoint_spec_ports,
                ]
            },
            mounts=[
                docker.types.Mount(
                    type="bind",
                    source=worker_path,
                    target="/app/worker",
                    read_only=False,
                ),
                docker.types.Mount(
                    type="bind",
                    source="/var/run/docker.sock",
                    target="/var/run/docker.sock",
                ),
                *docker_mounts,
            ],
            env={
                "PORT": port,
                "SERVICE_NAME": service_name_env,
                "WORKER_NAME": service_name,
                **env_ports,
                **env,
            },
        )

        return port

    # ----------------------------------------------------------------------
    def start_worker(self, worker_path, **kwargs):
        """"""
        if os.path.isabs(worker_path) or os.path.exists(worker_path):
            worker_path = os.path.abspath(worker_path)
        elif os.path.exists(select_worker(worker_path)):
            if not 'service_name' in kwargs:
                kwargs['service_name'] = worker_path
            worker_path = select_worker(worker_path)
            kwargs['service_name'] = kwargs['service_name'].replace('_', '-')

        if os.path.exists(os.path.join(worker_path, 'manage.py')):
            logging.warning('Running a Django worker')
            return self.start_django_worker(worker_path, **kwargs)  # Django
        elif os.path.exists(os.path.join(worker_path, 'main.py')):
            with open(os.path.join(worker_path, 'main.py'), 'r') as file:
                content = file.read()
                if 'from foundation.radiant.server' in content:
                    logging.warning('Running a Brython worker')
                    return self.start_brython_worker(
                        worker_path, **kwargs
                    )  # Brython
                else:
                    logging.warning('Running a Pyhton worker')
                    return self.start_python_worker(
                        worker_path, **kwargs
                    )  # Python
        else:
            logging.warning('Impossible to detect a Worker')
