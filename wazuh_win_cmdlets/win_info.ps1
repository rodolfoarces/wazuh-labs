param(
    [switch]$Bios
    )
if ($Bios) {
    Get-WmiObject win32_bios | Select-Object -Property Name,Manufacturer,Version,SerialNumber | ConvertTo-Json -Compress
}