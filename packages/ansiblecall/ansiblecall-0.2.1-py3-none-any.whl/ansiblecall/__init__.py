import importlib
import logging

import ansiblecall.utils.ansibleproxy

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(name)-17s][%(levelname)-8s:%(lineno)-4d][%(processName)s:%(process)d] %(message)s",
)


def module(mod_name, **params):
    """Run ansible module."""
    log.debug("Running module [%s] with params [%s]", mod_name, " ,".join(list(params)))
    modules = ansiblecall.utils.ansibleproxy.load_ansible_mods()
    mod = modules[mod_name]
    with ansiblecall.utils.ansibleproxy.Context(
        module_path=mod.path,
        module_name=mod.name,
        params=params,
    ) as ctx:
        mod = importlib.import_module(ctx.module_name)
        try:
            mod.main()
        except SystemExit:
            log.debug("Returning data to caller.")
            return ctx.ret


def refresh_modules():
    """Refresh Ansible module cache"""
    fun = ansiblecall.utils.ansibleproxy.load_ansible_mods
    fun.cache_clear()
    return fun()
