#!/usr/bin/python3
import os, sys, imp

# Configuration info.
madz_config = {
    "user_config_env": "CRAFT_ENGINE_USER_CONFIG",
    "log_to_stdout": True,
    "logging_file": "./engine.log",
    "plugin_directories" : ["./plugins/"],
    "plugin_configs" : ["system_config.py"],
    "executable_directories" : ["executables/unit_test"],
    "executable_configs" : ["executables/unit_test/unit_test_config.py"]
}

attached = False
def attach_madz():
    """Add Madz to your system path"""
    global attached
    if not attached:
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        sys.path.append(os.path.abspath("../massive-dangerzone/"))
    attached = True

def start_daemon():
    """Start a Madz Server"""
    attach_madz()

    import madz.live_script as madz

    daemon = madz.Daemon(**madz_config)
    print("Configuring Server...")
    daemon.configure()
    print("Starting Server")
    daemon.start()

def create_client():
    attach_madz()
    import madz.live_script as madz
    return madz.Client(madz_config)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: main.py {daemon} | command {command_name} [-p {plugin_namespace}] [-l{log_level}]}")
        exit(1)

    attach_madz()

    if sys.argv[1] == "daemon":
        start_daemon()

    else:
        client = create_client()
        client.set_executable(sys.argv[1])
        sys.argv.remove(sys.argv[1])

        client.run_raw(sys.argv)