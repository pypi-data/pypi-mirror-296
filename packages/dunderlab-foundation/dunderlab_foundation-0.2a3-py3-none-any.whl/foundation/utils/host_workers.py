import os
import subprocess
import pickle
import random
from string import digits, ascii_letters
import psutil

user_home = os.path.expanduser('~')
project_folder = os.path.join(user_home, 'foundation')
os.makedirs(project_folder, exist_ok=True)

WORKER_NAME = "{}-host-worker"


########################################################################
class HostWorker:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, env='python3'):
        """"""
        self.log_file = os.path.join(project_folder, 'process_info')
        self.env = env

        try:
            self.load_ids(drop=True)
        except (FileNotFoundError, EOFError):
            self.ids = {}
            self.save_ids()

    # ----------------------------------------------------------------------
    def load_ids(self, drop=False):
        """"""
        with open(self.log_file, 'rb') as f:
            self.ids = pickle.load(f)

        self.update_status(drop)

    # ----------------------------------------------------------------------
    def save_ids(self):
        """"""
        with open(self.log_file, 'wb') as f:
            pickle.dump(self.ids, f)

    # ----------------------------------------------------------------------
    def start_worker(
        self,
        worker_path,
        service_name=None,
        run="main.py",
        restart=False,
        tag='1.1',
        env={},
    ):
        """"""

        if os.path.isabs(worker_path) or os.path.exists(worker_path):
            worker_path = os.path.abspath(worker_path)

        if service_name is None:
            service_name = WORKER_NAME.format(
                os.path.split(worker_path)[-1].replace("_", "-")
            )

        service_name_env = service_name.replace('-host-worker', '')

        if service_name in self.ids:
            if restart:
                self.restart(service_name)
            return

        with open(os.path.join(worker_path, 'logfile'), 'w') as logfile:
            process = subprocess.Popen(
                [self.env, os.path.join(worker_path, run)],
                env={
                    "SERVICE_NAME": service_name_env,
                    "WORKER_NAME": service_name,
                    **env,
                },
                stdout=logfile,
                stderr=logfile,
                preexec_fn=os.setpgrp,
            )

        self.ids[service_name] = {
            'pid': process.pid,
            'restart': restart,
            'service_name_env': service_name_env,
            'worker_path': worker_path,
            'run': run,
            'env': env,
        }

        self.save_ids()

    # ----------------------------------------------------------------------
    def stop(self, service_name, command='kill'):
        """"""
        pid = self.ids[service_name]['pid']

        try:
            process = psutil.Process(pid)
            getattr(process, command)()

        except psutil.NoSuchProcess:
            pass

    # ----------------------------------------------------------------------
    def restart(self, service_name):
        """"""
        self.stop(service_name)

        proc = self.ids[service_name]
        with open(
            os.path.join(proc['worker_path'], 'logfile'), 'w'
        ) as logfile:
            process = subprocess.Popen(
                [self.env, os.path.join(proc['worker_path'], proc['run'])],
                env={
                    "SERVICE_NAME": proc['service_name_env'],
                    "WORKER_NAME": service_name,
                    **proc['env'],
                },
                stdout=logfile,
                stderr=logfile,
                preexec_fn=os.setpgrp,
            )

        proc['pid'] = process.pid
        self.save_ids()

    # ----------------------------------------------------------------------
    def gen_worker_name(self, length=8):
        """"""
        id_ = "".join(
            [random.choice(ascii_letters + digits) for _ in range(length)]
        )
        if not WORKER_NAME.format(id_) in self.ids:
            return WORKER_NAME.format(id_)

        return self.gen_worker_name(length)

    # ----------------------------------------------------------------------
    def update_status(self, drop):
        """"""
        for name in self.ids:
            pid = self.ids[name]['pid']
            try:
                process = psutil.Process(pid)
                status = process.status()

                self.ids[name]['status'] = status
            except psutil.NoSuchProcess:
                self.ids[name]['status'] = 'None'

        if drop:
            ids = self.ids.copy()
            for name in self.ids:
                if self.ids[name]['status'] == 'None':
                    ids.pop(name)
            self.ids = ids

        self.save_ids()
