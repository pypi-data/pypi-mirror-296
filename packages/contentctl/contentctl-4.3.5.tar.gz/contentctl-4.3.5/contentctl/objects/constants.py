
ATTACK_TACTICS_KILLCHAIN_MAPPING = {
    "Reconnaissance": "Reconnaissance",
    "Resource Development": "Weaponization",
    "Initial Access": "Delivery",
    "Execution": "Installation",
    "Persistence": "Installation",
    "Privilege Escalation": "Exploitation",
    "Defense Evasion": "Exploitation",
    "Credential Access": "Exploitation",
    "Discovery": "Exploitation",
    "Lateral Movement": "Exploitation",
    "Collection": "Exploitation",
    "Command And Control": "Command and Control",
    "Exfiltration": "Actions on Objectives",
    "Impact": "Actions on Objectives"
}

SES_CONTEXT_MAPPING = {
    "Unknown": 0,
    "Source:Endpoint": 10,
    "Source:AD": 11,
    "Source:Firewall": 12,
    "Source:Application Log": 13,
    "Source:IPS": 14,
    "Source:Cloud Data": 15,
    "Source:Correlation": 16,
    "Source:Printer": 17,
    "Source:Badge": 18,
    "Scope:Internal": 20,
    "Scope:External": 21,
    "Scope:Inbound": 22,
    "Scope:Outbound": 23,
    "Scope:Local": 24,
    "Scope:Network": 25,
    "Outcome:Blocked": 30,
    "Outcome:Allowed": 31,
    "Stage:Recon": 40,
    "Stage:Initial Access": 41,
    "Stage:Execution": 42,
    "Stage:Persistence": 43,
    "Stage:Privilege Escalation": 44,
    "Stage:Defense Evasion": 45,
    "Stage:Credential Access": 46,
    "Stage:Discovery": 47,
    "Stage:Lateral Movement": 48,
    "Stage:Collection": 49,
    "Stage:Exfiltration": 50,
    "Stage:Command And Control": 51,
    "Consequence:Infection": 60,
    "Consequence:Reduced Visibility": 61,
    "Consequence:Data Destruction": 62,
    "Consequence:Denial Of Service": 63,
    "Consequence:Loss Of Control": 64,
    "Rares:Rare User": 70,
    "Rares:Rare Process": 71,
    "Rares:Rare Device": 72,
    "Rares:Rare Domain": 73,
    "Rares:Rare Network": 74,
    "Rares:Rare Location": 75,
    "Other:Peer Group": 80,
    "Other:Brute Force": 81,
    "Other:Policy Violation": 82,
    "Other:Threat Intelligence": 83,
    "Other:Flight Risk": 84,
    "Other:Removable Storage": 85
}

SES_KILL_CHAIN_MAPPINGS = {
    "Unknown": 0,
    "Reconnaissance": 1,
    "Weaponization": 2,
    "Delivery": 3,
    "Exploitation": 4,
    "Installation": 5,
    "Command and Control": 6,
    "Actions on Objectives": 7
}

SES_OBSERVABLE_ROLE_MAPPING = {
    "Other": -1,
    "Unknown": 0,
    "Actor": 1,
    "Target": 2,
    "Attacker": 3,
    "Victim": 4,
    "Parent Process": 5,
    "Child Process": 6,
    "Known Bad": 7,
    "Data Loss": 8,
    "Observer": 9
}

SES_OBSERVABLE_TYPE_MAPPING = {
    "Unknown": 0,
    "Hostname": 1,
    "IP Address": 2,
    "MAC Address": 3,
    "User Name": 4,
    "Email Address": 5,
    "URL String": 6,
    "File Name": 7,
    "File Hash": 8,
    "Process Name": 9,
    "Resource UID": 10,
    "Endpoint": 20,
    "User": 21,
    "Email": 22,
    "Uniform Resource Locator": 23,
    "File": 24,
    "Process": 25,
    "Geo Location": 26,
    "Container": 27,
    "Registry Key": 28,
    "Registry Value": 29,
    "Other": 99
}

SES_ATTACK_TACTICS_ID_MAPPING = {
    "Reconnaissance": "TA0043",
    "Resource_Development": "TA0042",
    "Initial_Access": "TA0001",
    "Execution": "TA0002",
    "Persistence": "TA0003",
    "Privilege_Escalation": "TA0004",
    "Defense_Evasion": "TA0005",
    "Credential_Access": "TA0006",
    "Discovery": "TA0007",
    "Lateral_Movement": "TA0008",
    "Collection": "TA0009",
    "Command_and_Control": "TA0011",
    "Exfiltration": "TA0010",
    "Impact": "TA0040"
}

RBA_OBSERVABLE_ROLE_MAPPING = {
    "Attacker": 0,
    "Victim": 1
}

# The relative path to the directory where any apps/packages will be downloaded
DOWNLOADS_DIRECTORY = "downloads"
