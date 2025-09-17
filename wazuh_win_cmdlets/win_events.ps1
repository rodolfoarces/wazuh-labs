$filterTable = @{
    LogName = 'System'
    Id = 41, 1074, 6005 , 6006, 6008
    StartTime = (Get-Date).AddHours(-24)
}
$eventList = @(Get-WinEvent -FilterHashtable $filterTable -ErrorAction SilentlyContinue);
if ($eventList.Count -eq 0) {
    Write-Host "No events found.";
    exit 0;
} else {
    Write-Host "Events retrieved successfully.";
    foreach ( $event_found in $eventList ) {
        Write-Host "$($event_found | ConvertTo-Json -Compress)";
    }
}