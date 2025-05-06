param(
    [switch]$Bios
    )
if ($Bios) {
    Get-WmiObject win32_bios | Select-Object -Property Name,SMBIOSBIOSVersion,Manufacturer,Version | ConvertTo-Json -Compress
}