#!/usr/bin/env python

import os
import sys
import curses
import logging
import argparse

from foundation.utils import Workers, WORKER_NAME
from foundation.workers import list_workers, select_worker

logging.basicConfig(level=logging.CRITICAL)

parser = argparse.ArgumentParser(description="Start an HCI worker.")
parser.add_argument(
    '-a', '--advertise_addr', default=None, help="Advertise address."
)
args = parser.parse_args()

workers = Workers(swarm_advertise_addr=args.advertise_addr)

foundation_services = set(
    [
        # 'kafka-service',
        # 'zookeeper-service',
        # 'kafka-logs-service',
        # 'zookeeper-logs-service',
        'timescaledb-service',
        'jupyterlab-service',
        'ntp-service',
    ]
)

COMMANDS = [
    "['q' to close]",
    "['k' to kill all services]",
    "['l' to kill all workers]",
    # "['s' to run Foundation]",
]
COMMAND_START = '[START]'
COMMAND_RESTART = '[RESTART]'
COMMAND_STOP = '[STOP]'

system_workers = set(
    [
        WORKER_NAME.format(worker).replace('_', '-')
        for worker in list_workers()
    ]
)

extra_args = {
    'start_timescaledb_api_worker': {
        'service_name': 'timescaledb_api',
        'image': 'djangorun',
        'endpoint': '/timescaledbapp/',
        'port': 51102,
        'restart': True,
    },

    'start_chaski_root_worker': {'port': 51110,},
    'start_chaski_ca_worker': {'port': 51111,},
    'start_chaski_remote_worker': {'port': 51112,},
    'start_chaski2api_worker': {'port': 51113,},
    'start_chaski_logger_root_worker': {'port': 51114,},
    'start_chaski_api_logger_worker': {'port': 51115,},

}

CONTINUE = True


########################################################################
class Stats:
    """"""

    COL = [0, 16, 60, 73, 87, 109, 126, 164]
    COL_NAMES = [
        "",
        "RUNNING",
        "NODE",
        "SERVICE ID",
        "CONTAINER ID",
        "IMAGE",
        "URL",
    ]

    # ----------------------------------------------------------------------
    def __init__(self, stdscr):
        """Constructor"""
        global CONTINUE
        self.row_services = {}
        curses.resizeterm(100, 1000)
        curses.curs_set(0)
        stdscr.nodelay(True)
        curses.mousemask(1)
        self.stdscr = stdscr

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

        while CONTINUE:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, '-' * 80)
            start = self.update_services_stats(
                foundation_services, name='FOUNDATION SERVICES', start=1
            )
            start = self.update_services_stats(
                system_workers, name='SYSTEM WORKERS', start=start
            )
            start = self.update_services_stats(
                set(workers.swarm.services)
                - foundation_services
                - system_workers,
                name='USER WORKERS',
                start=start,
            )
            self.stdscr.addstr(start, 0, '-' * 80)
            start = self.update_volumes_stats(
                name='VOLUMES', start=start + 2
            )
            self.stdscr.addstr(start, 0, '-' * 80)
            self.stdscr.addstr(
                start + 2, 0, workers.swarm.get_join_command()
            )
            self.stdscr.addstr(
                start + 10, 0, ' '.join(COMMANDS), curses.color_pair(5)
            )
            self.stdscr.addstr(start + 4, 0, '')  # logs
            self.stdscr.refresh()

            event = stdscr.getch()
            if event == curses.KEY_MOUSE:
                _, x, y, _, _ = curses.getmouse()
                command = stdscr.instr(
                    y, max([0, x - 7]), 15 + min([0, x - 7])
                ).decode('utf-8')
                line = stdscr.instr(y, 0, 500).decode('utf-8')
                if len(line.split()) > 1:
                    worker = line.split()[1][line.split()[1].find('@') + 1 :]
                else:
                    worker = None
                self.process_event(command, y, worker)

            elif event == ord('q'):
                CONTINUE = False
                break

            elif event == ord('k'):
                workers.swarm.stop_all_services()

            elif event == ord('l'):
                workers.stop_all_workers()

            # elif event == ord('s'):
            #     os.system('foundation_start > /dev/null 2>&1')

    # ----------------------------------------------------------------------
    def process_event(self, command, row, worker):
        """"""
        if not row in self.row_services:
            return

        if COMMAND_RESTART in command:
            command = COMMAND_RESTART
        elif COMMAND_STOP in command:
            command = COMMAND_STOP
        elif COMMAND_START in command:
            command = COMMAND_START

        service_name = self.row_services[row]
        if command == COMMAND_STOP:
            workers.swarm.stop_service(service_name)
        elif command in [COMMAND_RESTART, COMMAND_START]:

            method_service = f'start_{service_name.replace("-service",  "").replace("-",  "_")}'
            # service_name = service_name.replace("-worker", "").replace("-", "_")
            worker_name = service_name.replace("-worker", "").replace(
                "-", "_"
            )

            if hasattr(workers.swarm, method_service):
                getattr(workers.swarm, method_service)(
                    **extra_args.get(
                        method_service,
                        {
                            'restart': True,
                        },
                    )
                )

            elif worker_name in workers.swarm.services or os.path.exists(
                select_worker(worker_name)
            ):
                workers.start_worker(
                    worker_name,
                    **extra_args.get(
                        method_service,
                        {
                            'restart': True,
                        },
                    ),
                )

            elif worker_name in workers.swarm.services:
                workers.start_worker(
                    worker,
                    service_name=worker_name,
                    **extra_args.get(
                        method_service,
                        {
                            'restart': True,
                        },
                    ),
                )

    # ----------------------------------------------------------------------
    def write_row(self, items, row=0, m=0):
        """"""
        for item, col in zip(items, self.COL):
            if ('----' in items[:-1] or 'N/A' in items[:-1]) and (
                col == self.COL[1]
            ):
                color = curses.color_pair(1)
            elif (items[2] == 'True') and (col == self.COL[1]):
                color = curses.color_pair(2)
            elif col == 0 and item in [
                COMMAND_START,
                COMMAND_STOP + COMMAND_RESTART,
            ]:
                if item == COMMAND_START:
                    color = curses.color_pair(3)
                elif item == COMMAND_STOP + COMMAND_RESTART:
                    color = curses.color_pair(4)
                else:
                    color = curses.color_pair(0)

            elif col == 126 and not item in ['IMAGE', '----']:
                images = workers.swarm.client.images.list()
                if not any(item in tag for image in images for tag in image.tags):
                    color = curses.color_pair(1)
            else:
                color = curses.color_pair(0)

            self.stdscr.addstr(row, col, item, color)

    # ----------------------------------------------------------------------
    def service_get(self, service, attr='id', default='----'):
        """"""
        service = workers.swarm.client.services.list(
            filters={
                'name': service,
            }
        )
        if service:
            try:
                match attr:
                    case 'id':
                        return service[0].id[:12]
                    case 'container_id':
                        return service[0].tasks()[0]['Status'][
                            'ContainerStatus'
                        ]['ContainerID'][:12]
                    case 'image':
                        return service[0].tasks()[0]['Spec'][
                            'ContainerSpec'
                        ]['Image']
                    case 'ip':
                        return list(
                            filter(
                                lambda s: s.startswith('PORT='),
                                service[0].tasks()[0]['Spec'][
                                    'ContainerSpec'
                                ]['Env'],
                            )
                        )[0].replace('PORT=', '')
                    case 'url':
                        return list(
                            filter(
                                lambda s: s.startswith('URL='),
                                service[0].tasks()[0]['Spec'][
                                    'ContainerSpec'
                                ]['Env'],
                            )
                        )[0].replace('URL=', '')
                    case 'service_name':
                        try:
                            return "@" + list(
                                filter(
                                    lambda s: s.startswith('SERVICE_NAME='),
                                    service[0].tasks()[0]['Spec'][
                                        'ContainerSpec'
                                    ]['Env'],
                                )
                            )[0].replace('SERVICE_NAME=', '')
                        except:
                            return ''
                    case 'endpoint':
                        try:
                            return list(
                                filter(
                                    lambda s: s.startswith('ENDPOINT='),
                                    service[0].tasks()[0]['Spec'][
                                        'ContainerSpec'
                                    ]['Env'],
                                )
                            )[0].replace('ENDPOINT=', '')
                        except:
                            return ''
                    case 'node':

                        node_id = service[0].tasks()[0]['NodeID']

                        node_info = workers.swarm.client.nodes.get(node_id)

                        return node_info.attrs['Description']['Hostname']

            except:
                return "N/A"
        else:
            return default

    # ----------------------------------------------------------------------
    def update_services_stats(self, services, name, start=0):
        """"""
        if not services:
            return start
        self.write_row([name] + self.COL_NAMES, row=start, m=0)
        for row, service in enumerate(services, start=start + 1):

            self.row_services[row] = service

            url = '----'
            if self.service_get(service, attr='ip') not in ['----', 'N/A']:
                url = f"http://127.0.0.1:{self.service_get(service, attr='ip')}{self.service_get(service, attr='endpoint')}"
            elif self.service_get(service, attr='url') not in [
                '----',
                'N/A',
            ]:
                url = f"{self.service_get(service, attr='url')}:{self.service_get(service, attr='ip')}{self.service_get(service, attr='endpoint')}"

            if service in workers.swarm.services:
                command = COMMAND_STOP + COMMAND_RESTART
            else:
                command = COMMAND_START

            self.write_row(
                [
                    command,
                    f"{service}{self.service_get(service, attr='service_name',  default='')}",
                    f"{service in workers.swarm.services}",
                    f"{self.service_get(service, attr='node')}",
                    f"{self.service_get(service, attr='id')}",
                    f"{self.service_get(service, attr='container_id')}",
                    f"{self.service_get(service, attr='image')}",
                    url,
                ],
                row=row,
            )
        return row + 2

    # ----------------------------------------------------------------------
    def update_volumes_stats(self, name, start=0):
        """"""
        self.stdscr.addstr(start, 0, name)
        networks = sorted(
            [
                v
                for v in workers.swarm.client.volumes.list()
                if v.name.endswith('-volume')
            ],
            key=lambda s: s.name,
        )
        for row, volume in enumerate(networks, start=start + 1):
            self.stdscr.addstr(row, 0, volume.name)
        return row + 2


# ----------------------------------------------------------------------
def main():
    """"""
    while True:
        try:
            curses.wrapper(Stats)
            if not CONTINUE:
                break
        except Exception as e:
            pass
    sys.exit()


if __name__ == '__main__':
    main()
