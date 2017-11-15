# use TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$downloadsPage = Invoke-WebRequest -Uri "https://rpcs3.net/download"

$downloadLink = ($downloadsPage.Links | Where-Object {($_.InnerText -ne $null)} | Where-Object { $_.InnerText.StartsWith("Download for Windows") } | Select-Object href).href

if ($downloadLink) {
    $zipFile = "RPCS3-Latest.zip"
    $extractTo = "$env:temp\RPCS3\"
    $finalDestination = "D:\win\Emulators\"

    Invoke-WebRequest -Uri $downloadLink -OutFile $zipFile

    Add-Type -assembly "system.io.compression.filesystem"
    [io.compression.zipfile]::ExtractToDirectory($zipFile, $extractTo)

    # recursively copy files from temp directory to destination, overwriting existing files
    Copy-Item -Path $extractTo -Destination $finalDestination -Recurse -Force

    # clean up downloaded archive and temp folder
    Remove-Item $zipFile
    Remove-Item $extractTo -Recurse
}
else {
    Write-Host "Could not find download link for latest RPCS3!"
}