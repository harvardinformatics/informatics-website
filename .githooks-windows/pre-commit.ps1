# Re-comment development-only ignore line in mkdocs.yml (PowerShell)

$File = "mkdocs.yml"
if (-Not (Test-Path $File)) {
    exit 0
}

$Content = Get-Content $File
$Modified = $false
$Fixed = @()

foreach ($line in $Content) {
    if ($line -match "^\s*ignore: \['\*\.ipynb'\]") {
        $Fixed += "# $line"
        $Modified = $true
    } else {
        $Fixed += $line
    }
}

if ($Modified) {
    Set-Content $File $Fixed
    git add $File
    Write-Output "Re-commented development ignore line in mkdocs.yml"
}

exit 0