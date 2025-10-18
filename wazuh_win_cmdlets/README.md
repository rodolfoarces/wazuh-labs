# Wazuh Windows Commandlets

The information output is normally JSON (Compressed) for easier Wazuh decoding

# Files

[README.md](./README.md): project information and command usage examples]

[win_info.ps1](./win_info.ps1): Windows OS information extraction script

[win_events.ps1](./win_events.ps1): Windows events collection script

# Win Info

Windows OS and platform information extraction script

## Usage

```
.\win_info.ps1 [Parameters]

-Bios       Obtaing BIOS information
```

## Windows system information

### BIOS

```
.\win_info.ps1 -Bios
```

# Win events

Windows event collection script

## Usage

```
.\win_events.ps1
```


