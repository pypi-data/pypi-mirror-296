[![CI](https://github.com/frobnitzem/psik_api/actions/workflows/python-package.yml/badge.svg)](https://github.com/frobnitzem/psik_api/actions)
[![Coverage](https://codecov.io/github/frobnitzem/psik_api/branch/main/graph/badge.svg)](https://app.codecov.io/gh/frobnitzem/psik_api)

PSI\_K API
==========

This project presents a REST-HTTP API to
functionality available through other APIs and
command-line utilities on PSI\_K systems.

This API is inspired by the NERSC "superfacility" API
v1.2 and the ExaWorks JobSpec.  Differences come from
the need to make the superfacility more portable between
backends and the JobSpec more API-friendly.

To setup and run:

1. Install the rc shell and psik\_api (from the site you intend to use):

```
     module load python/3
     python3 -m venv
     getrc.sh venv # https://github.com/frobnitzem/rcrc
     VIRTUAL_ENV=/full/path/to/venv
     PATH=$VIRTUAL_ENV/bin:$PATH
   
     pip install git+https://github.com/frobnitzem/psik_api.git
```

2. Setup a psik\_api config file.  This file is a key-value store
   mapping machine names to psik config files
   -- one for each scheduler configuration.

   Be careful with the `psik_path` and `rc_path`
   options here. These paths must be
   accessible during the execution of the job, and
   on the host running psik\_api.

   Note that the `PSIK_CONFIG` environment variable does not
   influence the server running `psik_api`.

   Create a config file at `$PSIK_API_CONFIG` (defaults to
   `$VIRTUAL_ENV/etc/psik_api.json`) like,

       { "default": {
             "prefix": "/tmp/psik_jobs",
             "backend": { "type": "local"}
         }
       }

   or

       { "default": {
           "prefix": "/ccs/proj/stf006/rogersdd/frontier",
           "psik_path": "/ccs/proj/stf006/rogersdd/frontier/bin/psik",
           "rc_path": "/ccs/proj/stf006/rogersdd/frontier/bin/rc",
           "backend": {
             "type": "slurm",
             "project_name": "stf006",
             "attributes": {
               "---gpu-bind": "closest"
             }
           }
         }
       }


3. Start the server.  This can be done either directly
   by ssh-tunneling to a login node, or indirectly
   by starting a long-running containerized service.

   The ssh-tunnel method is simplest,

```
    ssh frontier -L 127.0.0.1:8000:/ccs/home/rogersdd/psik_api.sock
    activate /ccs/proj/stf006/frontier
    uvicorn psik_api.main:app --log-level info --uds $HOME/psik_api.sock
```

    Note that using a UNIX socket in `$HOME` is secure as long as
    only your user can read/write from it.

    For a more secure environment, use the `certified` package with:

        ssh frontier -L 8000:localhost:4433
        activate /ccs/proj/stf006/frontier
        certifiied serve psik_api.main:app https://127.0.0.1:4433

4. Browse / access the API at:

```
   http://127.0.0.1:8000/
```

5. Send a test job:

```
    curl -X POST \
      http://127.0.0.1:8000/compute/jobs/default \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "name": "show system info",
      "script": "cat /proc/cpuinfo; cat /proc/meminfo; rocm-smi; echo $nodes; $mpirun hostname",
      "resources": {
        "process_count": 8,
        "cpu_cores_per_process": 7,
        "duration": 2,
        "gpu_cores_per_process": 1
      }
    }'

    curl -X 'GET' \
      'http://127.0.0.1:8000/tasks/' \
      -H 'accept: application/json'

    # replace 1693992878.203 with your job's timestamp
    curl -X 'GET' \
      'http://127.0.0.1:8000/compute/jobs/default/1693992878.203' \
      -H 'accept: application/json'
```
