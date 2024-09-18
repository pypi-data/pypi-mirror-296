import docker
import logging
import netifaces


########################################################################
class Swarm:
    """"""

    # ----------------------------------------------------------------------
    def __init__(
        self, base_url='unix://var/run/docker.sock', advertise_addr=''
    ):
        """Constructor"""
        self.client = docker.DockerClient(base_url=base_url)
        try:
            logging.warning("Starting swarm...")
            if not self.client.swarm.attrs.get('ID'):
                swarm_init_response = self.client.swarm.init(
                    advertise_addr=advertise_addr
                )
                logging.warning(f"Swarm started, ID: {swarm_init_response}")
            else:
                logging.warning(
                    f"Swarm is already running, ID: {self.client.swarm.attrs.get('ID')}"
                )
        except docker.errors.APIError as e:
            logging.warning("Error:", str(e))
            return

        self.create_networks()

    # ----------------------------------------------------------------------
    def create_networks(self):
        """"""
        self.networks = ['hci_network']
        logging.warning("Creating networks...")
        for network in self.networks:
            if network not in [n.name for n in self.client.networks.list()]:
                self.client.networks.create(network, driver="overlay")
                logging.warning(f"Created network '{network}'")

    # ----------------------------------------------------------------------
    def create_volume(self, volume_name):
        """"""
        logging.warning("Creating volumes...")
        if not volume_name in self.volumes:
            if not volume_name.endswith('-volume'):
                volume_name = f'{volume_name}-volume'
            self.client.volumes.create(name=volume_name)
        else:
            logging.warning(f"Volume '{volume_name}' already exists")

        return volume_name

    # ----------------------------------------------------------------------
    def delete_volume(self, volume_name):
        """"""
        logging.warning("Deleting volumes...")
        try:
            # Fetch the volume
            volume = self.client.volumes.get(volume_name)
            # Remove the volume
            volume.remove()
            logging.info(f"Volume '{volume_name}' has been deleted.")
        except docker.errors.NotFound:
            logging.warning(f"Volume '{volume_name}' does not exist.")
        except docker.errors.APIError as e:
            logging.error(
                f"An error occurred while attempting to remove the volume: {e}"
            )

        return None

    # ----------------------------------------------------------------------
    @property
    def services(self, attr='name'):
        """"""
        return [
            getattr(service, attr) for service in self.client.services.list()
        ]

    # ----------------------------------------------------------------------
    @property
    def containers(self, attr='id'):
        """"""
        return [
            getattr(container, attr)
            for container in self.client.containers.list()
        ]

    # ----------------------------------------------------------------------
    @property
    def volumes(self):
        """"""
        return [
            v.name
            for v in self.client.volumes.list()
            if v.name.endswith('-volume')
        ]

    # ----------------------------------------------------------------------
    def stop_service(self, service_name):
        """"""
        service = self.client.services.get(service_name)
        return service.remove()

    # ----------------------------------------------------------------------
    def restart_service(self, service_name):
        """"""
        service = self.client.services.get(service_name)
        return service.update(force_update=True)

    # ----------------------------------------------------------------------
    def stop_all_services(self):
        """"""
        return [self.stop_service(service) for service in self.services]

    # ----------------------------------------------------------------------
    def stats(self, service_name):
        """"""
        service = self.client.services.get(service_name)
        stats = []
        for task in service.tasks():
            container_id = task['Status']['ContainerStatus']['ContainerID']
            if container_id in self.containers:
                stats.append(
                    self.client.containers.get(container_id).stats(
                        stream=False
                    )
                )
        return stats

    # ----------------------------------------------------------------------
    def start_ntp(
        self, service_name="ntp-service", port=123, restart=False, tag='1.0'
    ):
        """"""
        if restart and (service_name in self.services):
            self.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        service = self.client.services.create(
            image=f'dunderlab/ntp:{tag}',
            name=service_name,
            networks=self.networks,
            endpoint_spec={
                'Ports': [
                    {
                        'Protocol': 'udp',
                        'PublishedPort': port,
                        'TargetPort': 123,
                    },
                ]
            },
            env=[
                f"PORT={port}",
            ],
        )

        return service_name in self.services

    # ----------------------------------------------------------------------
    def start_jupyterlab(
        self,
        service_name="jupyterlab-service",
        port=8888,
        restart=False,
        tag='1.1',
        volume_name=None,
        mounts=None,
        env={},
    ):
        """"""
        if restart and (service_name in self.services):
            self.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        if volume_name is None:
            volume_name = self.create_volume(service_name)
        else:
            volume_name = self.create_volume(volume_name)

        docker_mounts = []
        if mounts:
            for source, target in mounts:

                docker_mounts.append(
                    docker.types.Mount(
                        type='bind', source=source, target=target
                    )
                )

        service = self.client.services.create(
            image=f"dunderlab/python312:{tag}",
            name=service_name,
            networks=self.networks,
            command=[
                "/bin/bash",
                "-c",
                "jupyter lab --notebook-dir='/app' --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token='' --NotebookApp.password=''",
            ],
            endpoint_spec={
                'Ports': [
                    {
                        'Protocol': 'tcp',
                        'PublishedPort': 8888,
                        'TargetPort': port,
                    },
                ]
            },
            hosts=self.extra_host(),
            mounts=[
                docker.types.Mount(
                    type='bind',
                    source='/var/run/docker.sock',
                    target='/var/run/docker.sock',
                ),
                docker.types.Mount(
                    target='/app',
                    source=volume_name,
                    type="volume",
                    read_only=False,
                ),
                *docker_mounts,
            ],
            env={
                f"PORT": {port},
                # "NTP_SERVER=ntp-service",
                **env,
            },
        )
        return service_name in self.services

    # ----------------------------------------------------------------------
    def start_kafka(
        self,
        kafka_service_name="kafka-service",
        zookeeper_service_name="zookeeper-service",
        kafka_port=9092,
        kafka_port_external=19092,
        zookeeper_port=2181,
        restart=False,
        tag='1.1',
    ):
        """"""
        if restart and (kafka_service_name in self.services):
            self.stop_service(kafka_service_name)
            logging.warning(f"Restarting service '{kafka_service_name}'")

        if restart and (zookeeper_service_name in self.services):
            self.stop_service(zookeeper_service_name)
            logging.warning(f"Restarting service '{zookeeper_service_name}'")

        if not kafka_service_name in self.services:
            kafka_service = self.client.services.create(
                image=f"dunderlab/kafka:{tag}",
                # restart_policy=docker.types.RestartPolicy(condition='any'),
                name=kafka_service_name,
                networks=self.networks,
                endpoint_spec={
                    'Ports': [
                        {
                            'Protocol': 'tcp',
                            'PublishedPort': kafka_port,
                            'TargetPort': kafka_port,
                        },
                        {
                            'Protocol': 'tcp',
                            'PublishedPort': kafka_port_external,
                            'TargetPort': kafka_port_external,
                        },
                    ]
                },
                env=[
                    f"KAFKA_ZOOKEEPER_CONNECT={zookeeper_service_name}:{zookeeper_port}",
                    f"KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT",
                    f"KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://{kafka_service_name}:{kafka_port},PLAINTEXT_HOST://localhost:{kafka_port_external}",
                    f"PORT={kafka_port_external}",
                ],
            )
        else:
            logging.warning(f"Service '{kafka_service_name}' already exist")

        if not zookeeper_service_name in self.services:
            zookeeper_service = self.client.services.create(
                image=f"dunderlab/zookeeper:{tag}",
                name=zookeeper_service_name,
                networks=self.networks,
                endpoint_spec={
                    'Ports': [
                        {
                            'Protocol': 'tcp',
                            'PublishedPort': zookeeper_port,
                            'TargetPort': zookeeper_port,
                        },
                    ]
                },
                env=[
                    f"ZOOKEEPER_CLIENT_PORT={zookeeper_port}",
                ],
            )
        else:
            logging.warning(
                f"Service '{zookeeper_service_name}' already exist"
            )

        return (
            kafka_service_name in self.services,
            zookeeper_service_name in self.services,
        )

    # ----------------------------------------------------------------------
    def start_kafka_logs(
        self,
        kafka_service_name="kafka-logs-service",
        zookeeper_service_name="zookeeper-logs-service",
        kafka_port=9093,
        kafka_port_external=19093,
        zookeeper_port=2182,
        restart=False,
        tag='1.1',
    ):
        """"""
        return self.start_kafka(
            kafka_service_name,
            zookeeper_service_name,
            kafka_port,
            kafka_port_external,
            zookeeper_port,
            restart,
            tag,
        )

    # ----------------------------------------------------------------------
    def start_timescaledb(
        self,
        service_name="timescaledb-service",
        port=5432,
        volume_name=None,
        restart=False,
        tag='latest-pg15',
    ):
        """"""
        if restart and (service_name in self.services):
            self.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        if volume_name is None:
            volume_name = self.create_volume(service_name)
        else:
            volume_name = self.create_volume(volume_name)

        timescaledb_service = self.client.services.create(
            image=f"timescale/timescaledb:{tag}",
            name=service_name,
            networks=self.networks,
            env=[
                "POSTGRES_PASSWORD=password",
                "POSTGRES_USER=postgres",
                "POSTGRES_DB=timescaledb",
                "POSTGRES_MAX_CONNECTIONS=500",
                f"PORT={port}",
            ],
            endpoint_spec={
                'Ports': [
                    {
                        'Protocol': 'tcp',
                        'PublishedPort': 5432,
                        'TargetPort': port,
                    },
                ]
            },
            mounts=[
                docker.types.Mount(
                    target='/var/lib/postgresql/data',
                    source=volume_name,
                    type="volume",
                    read_only=False,
                ),
            ],
        )
        return service_name in self.services

    # ----------------------------------------------------------------------
    def get_join_command(self):
        """"""
        swarm_info = self.client.info().get('Swarm')
        if swarm_info and swarm_info.get('ControlAvailable'):
            worker_join_token = self.client.swarm.attrs['JoinTokens'][
                'Worker'
            ]
            manager_addr = swarm_info.get('RemoteManagers')[0].get('Addr')
            return f'docker swarm join --token {worker_join_token} {manager_addr}'

    # ----------------------------------------------------------------------
    def advertise_addr(self):
        """"""
        swarm_info = self.client.info().get('Swarm')
        if swarm_info and swarm_info.get('ControlAvailable'):
            manager_addr = swarm_info.get('RemoteManagers')[0].get('Addr')
            return manager_addr

    # ----------------------------------------------------------------------
    def extra_host(self):
        """"""
        interfaces = netifaces.interfaces()
        ips = {}

        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                ip_info = addrs[netifaces.AF_INET][0]
                ips[interface] = ip_info['addr']

        return {
            f"host.docker.{interface}": ips[interface] for interface in ips
        }
