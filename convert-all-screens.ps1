function Zip($a1, $a2) {
    while ($a1) {
        $x, $a1 = $a1
        $y, $a2 = $a2
        [tuple]::Create($x, $y)
    }
}
$tops = Get-ChildItem -Path . -File -Filter "*_top.bmp"
$bots = Get-ChildItem -Path . -File -Filter "*_bot.bmp"
Foreach ($pair in Zip $tops $bots) {
  Write-Host "Converting " $pair
  $prm = 'convert', $pair.item1, "-gravity", "center", "-background", "None", $pair.item2, "-append", "$($pair.item1)_combined.png"
  & magick $prm
  del $pair.item1
  del $pair.item2
}
