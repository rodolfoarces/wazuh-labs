param(
    [switch]$Bios
    )
if ($Bios) {
    # Obtaing BIOS information and output JSON compressed format text
    Get-WmiObject win32_bios | Select-Object -Property Name,Manufacturer,Version,SerialNumber | ConvertTo-Json -Compress
}