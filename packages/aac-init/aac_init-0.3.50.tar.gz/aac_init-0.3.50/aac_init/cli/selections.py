# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

import os
import yamale

from typing import Any, Dict, List, Optional
from aac_init.logging import setup_logger
from aac_init.conf import settings
from aac_init.utils.aac_yaml import load_yaml_files
from aac_init.deployment.utils import Thread_Tool, CIMC_Tool, ACI_Switch_Tool
from ruamel import yaml

logger = setup_logger("selections.log")


class Selections:
    """
    Handle CLI selections
    """

    def __init__(self, data_path: str, output_path: str):
        logger.debug(
            f"Load selections with data_path: {data_path}, "
            f"output_path: {output_path}")

        self.data: Optional[Dict[str, Any]] = None
        self.data_path = data_path
        self.output_path = output_path
        self.fabric_mgmt = None
        self.global_policy = None
        self.errors: List[str] = []

        self._load_global_policy()

        if not self.global_policy:
            logger.error("global policy loaded failed!")
            exit(1)

        logger.debug("Selections initialized successfully!")

    def _load_global_policy(self):
        '''Load global policy'''

        logger.debug("Loading global policy...")
        for dir, _, files in os.walk(self.data_path):
            for filename in files:
                if filename in settings.DEFAULT_DATA_PATH:
                    self.global_policy_path = os.path.join(dir, filename)
        if self.global_policy_path:
            self.global_policy = load_yaml_files([self.global_policy_path])
            logger.debug("'00-global_policy' loaded successfully.")
            return True
        else:
            msg = "'00-global_policy' is missing!"
            logger.error(msg)
            self.errors.append(msg)
            return False

    def _load_fabric_mgmt(self):
        '''Load fabric mgmt'''

        logger.debug("Loading fabric mgmt...")
        for dir, _, files in os.walk(self.data_path):
            for filename in files:
                if filename in settings.DEFAULT_FABRIC_MGMT_PATH:
                    self.fabric_mgmt_path = os.path.join(dir, filename)
        if self.fabric_mgmt_path:
            self.fabric_mgmt = load_yaml_files([self.fabric_mgmt_path])
            logger.debug("'01-fabric-mgmt' loaded successfully.")
            return True
        else:
            msg = "'01-fabric-mgmt' is missing!"
            logger.error(msg)
            self.errors.append(msg)
            return False

    def fabric_bootstrap(self):
        '''
        Method: 01-fabric_bootstrap
        Description: Wipe and boot APIC/switch to particular version
        '''

        logger.debug("start to bootstrap ACI fabric...")

        fabric_policy = self.global_policy.get("fabric", {})
        global_policies = fabric_policy.get("global_policies", {}) or {}
        apic_check = "apic_nodes_connection" in fabric_policy
        aci_switch_check = "switch_nodes_connection" in fabric_policy

        fabric_bootstrap_threads = []

        # Validate APICs if have
        if apic_check:
            apics = fabric_policy.get("apic_nodes_connection", []) or []

            for apic_connection in apics:
                apic = CIMC_Tool(global_policies, apic_connection)
                if not apic.api_validate_apic():
                    msg = f"Validate APIC {apic.hostname} failed."
                    logger.error(msg)
                    self.errors.append(msg)
                    return False
                logger.info(f"Validate APIC {apic.hostname} successfully.")
                thread = Thread_Tool(target=apic.gen_install_apic)
                fabric_bootstrap_threads.append((apic.hostname, thread))

        # Validate ACI switches if have
        if aci_switch_check:
            aci_switches = fabric_policy.get("switch_nodes_connection", []) or []

            # Load fabric mgmt
            if self._load_fabric_mgmt():
                fabric_mgmt_policy_apic = self.fabric_mgmt.get("apic", {}) or {}
                fabric_mgmt_policy_apic_node_policies = fabric_mgmt_policy_apic.get("node_policies", {}) or {}
                aci_switches_mgmt = fabric_mgmt_policy_apic_node_policies.get("nodes", []) or []
            else:
                msg = "Unable to load fabric mgmt info!"
                logger.error(msg)
                self.errors.append(msg)
                return False

            for aci_switch_connection in aci_switches:
                aci_switch_mgmt = next((node for node in aci_switches_mgmt if node["id"] == aci_switch_connection["id"]), {})

                aci_switch = ACI_Switch_Tool(global_policies, aci_switch_connection, aci_switch_mgmt)
                if not aci_switch.validate_aci_switch():
                    msg = f"Validate ACI switch {aci_switch.hostname} failed."
                    logger.error(msg)
                    self.errors.append(msg)
                    return False
                logger.info(f"Validate ACI switch {apic.hostname} successfully.")
                thread = Thread_Tool(target=aci_switch.install_aci_switch)
                fabric_bootstrap_threads.append((aci_switch.hostname, thread))

        for _, thread in fabric_bootstrap_threads:
            thread.start()

        for _, thread in fabric_bootstrap_threads:
            thread.join()

        install_errors = []
        for hostname, thread in fabric_bootstrap_threads:
            if not thread.get_result():
                msg = f"Install {hostname} failed. Check APIC/switch logs for details."
                logger.error(msg)
                self.errors.append(msg)
                install_errors.append(hostname)

            logger.info(f"Install {hostname} successfully.")

        if install_errors:
            msg = "ACI fabric bootstrap failed, check APIC/switch logs for details."
            logger.error(msg)
            self.errors.append(msg)
            return False
        return True
