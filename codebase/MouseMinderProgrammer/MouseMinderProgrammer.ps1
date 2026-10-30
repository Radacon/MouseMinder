Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

[System.Windows.Forms.Application]::EnableVisualStyles()

$script:AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:ProgrammerPath = [System.IO.Path]::GetFullPath((Join-Path $script:AppDir '..\easy-pdk-programmer-software-master\easy-pdk-programmer-software-master\easypdkprog.exe'))
$script:DefaultFirmwarePath = [System.IO.Path]::GetFullPath((Join-Path $script:AppDir '..\VSCODE_FreePDK\.output\slowclocksleep_PMS150C.ihx'))

$form = New-Object System.Windows.Forms.Form
$form.Text = 'MouseMinder Programmer'
$form.StartPosition = 'CenterScreen'
$form.ClientSize = New-Object System.Drawing.Size(720, 500)
$form.MinimumSize = New-Object System.Drawing.Size(736, 539)
$form.Font = New-Object System.Drawing.Font('Segoe UI', 10)

$title = New-Object System.Windows.Forms.Label
$title.Text = 'MouseMinder Production Programmer'
$title.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 17)
$title.AutoSize = $true
$title.Location = New-Object System.Drawing.Point(20, 18)
$form.Controls.Add($title)

$settings = New-Object System.Windows.Forms.Label
$settings.Text = 'PMS150C  |  10 kHz programming clock  |  20 us phase'
$settings.AutoSize = $true
$settings.ForeColor = [System.Drawing.Color]::DimGray
$settings.Location = New-Object System.Drawing.Point(23, 55)
$form.Controls.Add($settings)

$firmwareLabel = New-Object System.Windows.Forms.Label
$firmwareLabel.Text = 'Firmware'
$firmwareLabel.AutoSize = $true
$firmwareLabel.Location = New-Object System.Drawing.Point(20, 91)
$form.Controls.Add($firmwareLabel)

$firmwareBox = New-Object System.Windows.Forms.TextBox
$firmwareBox.Location = New-Object System.Drawing.Point(23, 116)
$firmwareBox.Size = New-Object System.Drawing.Size(578, 28)
$firmwareBox.Text = $script:DefaultFirmwarePath
$form.Controls.Add($firmwareBox)

$browseButton = New-Object System.Windows.Forms.Button
$browseButton.Text = 'Browse...'
$browseButton.Location = New-Object System.Drawing.Point(610, 114)
$browseButton.Size = New-Object System.Drawing.Size(88, 31)
$form.Controls.Add($browseButton)

$checkButton = New-Object System.Windows.Forms.Button
$checkButton.Text = 'Check Programmer / PCB'
$checkButton.Location = New-Object System.Drawing.Point(23, 164)
$checkButton.Size = New-Object System.Drawing.Size(210, 42)
$form.Controls.Add($checkButton)

$programButton = New-Object System.Windows.Forms.Button
$programButton.Text = 'PROGRAM FIRMWARE'
$programButton.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 11)
$programButton.Location = New-Object System.Drawing.Point(245, 164)
$programButton.Size = New-Object System.Drawing.Size(230, 42)
$form.Controls.Add($programButton)

$clearButton = New-Object System.Windows.Forms.Button
$clearButton.Text = 'Clear Log'
$clearButton.Location = New-Object System.Drawing.Point(488, 164)
$clearButton.Size = New-Object System.Drawing.Size(100, 42)
$form.Controls.Add($clearButton)

$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.AutoSize = $true
$statusLabel.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 10)
$statusLabel.Location = New-Object System.Drawing.Point(23, 221)
$form.Controls.Add($statusLabel)

$logBox = New-Object System.Windows.Forms.TextBox
$logBox.Location = New-Object System.Drawing.Point(23, 251)
$logBox.Size = New-Object System.Drawing.Size(675, 224)
$logBox.Anchor = [System.Windows.Forms.AnchorStyles]::Top -bor [System.Windows.Forms.AnchorStyles]::Bottom -bor [System.Windows.Forms.AnchorStyles]::Left -bor [System.Windows.Forms.AnchorStyles]::Right
$logBox.Multiline = $true
$logBox.ReadOnly = $true
$logBox.ScrollBars = 'Vertical'
$logBox.Font = New-Object System.Drawing.Font('Consolas', 9)
$logBox.BackColor = [System.Drawing.Color]::FromArgb(248, 248, 248)
$form.Controls.Add($logBox)

function Write-Log([string]$Text) {
    $logBox.AppendText($Text + [Environment]::NewLine)
    $logBox.SelectionStart = $logBox.TextLength
    $logBox.ScrollToCaret()
    [System.Windows.Forms.Application]::DoEvents()
}

function Set-Status([string]$Text, [System.Drawing.Color]$Color) {
    $statusLabel.Text = $Text
    $statusLabel.ForeColor = $Color
}

function Test-RequiredFiles {
    if (-not (Test-Path -LiteralPath $script:ProgrammerPath -PathType Leaf)) {
        Set-Status 'ERROR: easypdkprog.exe is missing.' ([System.Drawing.Color]::Firebrick)
        $programButton.Enabled = $false
        $checkButton.Enabled = $false
        return $false
    }
    if (-not (Test-Path -LiteralPath $firmwareBox.Text -PathType Leaf)) {
        Set-Status 'Select a valid .ihx firmware file.' ([System.Drawing.Color]::DarkOrange)
        $programButton.Enabled = $false
        $checkButton.Enabled = $true
        return $false
    }
    Set-Status 'Ready. Connect the Easy PDK Programmer and the PCB.' ([System.Drawing.Color]::DarkGreen)
    $programButton.Enabled = $true
    $checkButton.Enabled = $true
    return $true
}

function Invoke-EasyPdk([string[]]$Arguments, [string]$Description) {
    $checkButton.Enabled = $false
    $programButton.Enabled = $false
    Set-Status $Description ([System.Drawing.Color]::DarkBlue)
    Write-Log ''
    Write-Log ('> easypdkprog.exe ' + ($Arguments -join ' '))

    try {
        $output = & $script:ProgrammerPath @Arguments 2>&1
        $exitCode = $LASTEXITCODE
        foreach ($line in $output) { Write-Log ([string]$line) }
        if ($exitCode -eq 0) {
            Set-Status 'SUCCESS' ([System.Drawing.Color]::DarkGreen)
        }
        else {
            Set-Status ('FAILED (exit code {0})' -f $exitCode) ([System.Drawing.Color]::Firebrick)
        }
        return $exitCode
    }
    catch {
        Write-Log $_.Exception.Message
        Set-Status 'FAILED to start programmer software.' ([System.Drawing.Color]::Firebrick)
        return -1
    }
    finally {
        $checkButton.Enabled = $true
        $programButton.Enabled = Test-Path -LiteralPath $firmwareBox.Text -PathType Leaf
    }
}

$browseButton.Add_Click({
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Title = 'Select MouseMinder firmware'
    $dialog.Filter = 'Intel HEX firmware (*.ihx)|*.ihx|All files (*.*)|*.*'
    $dialog.FileName = $firmwareBox.Text
    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $firmwareBox.Text = $dialog.FileName
        [void](Test-RequiredFiles)
    }
})

$firmwareBox.Add_TextChanged({ [void](Test-RequiredFiles) })
$clearButton.Add_Click({ $logBox.Clear() })

$checkButton.Add_Click({
    [void](Invoke-EasyPdk @('--frequency', '10000', '--phase', '20', '-n', 'PMS150C', 'probe') 'Checking programmer and target PCB...')
})

$programButton.Add_Click({
    if (-not (Test-RequiredFiles)) { return }

    $message = "PMS150C is one-time programmable (OTP).`r`n`r`nThis will permanently program:`r`n$($firmwareBox.Text)`r`n`r`nContinue?"
    $answer = [System.Windows.Forms.MessageBox]::Show(
        $form,
        $message,
        'Confirm OTP Programming',
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        [System.Windows.Forms.MessageBoxIcon]::Warning,
        [System.Windows.Forms.MessageBoxDefaultButton]::Button2
    )
    if ($answer -ne [System.Windows.Forms.DialogResult]::Yes) {
        Set-Status 'Programming cancelled.' ([System.Drawing.Color]::DimGray)
        return
    }

    $exitCode = Invoke-EasyPdk @('--frequency', '10000', '--phase', '20', '-n', 'PMS150C', 'write', $firmwareBox.Text) 'Programming and verifying...'
    if ($exitCode -eq 0) {
        [System.Media.SystemSounds]::Asterisk.Play()
        [System.Windows.Forms.MessageBox]::Show($form, 'Programming and verification completed successfully.', 'MouseMinder Programmer', 'OK', 'Information') | Out-Null
    }
})

[void](Test-RequiredFiles)
Write-Log 'MouseMinder Programmer ready.'
Write-Log ('Programmer: ' + $script:ProgrammerPath)
Write-Log ('Firmware:   ' + $firmwareBox.Text)
[void]$form.ShowDialog()

