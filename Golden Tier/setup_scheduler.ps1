# Setup Windows Task Scheduler for AI Employee Automation
# This uses EXISTING skills - no new automation layer

$WorkingDir = "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier"

Write-Host "=========================================="
Write-Host "AI Employee - Task Scheduler Setup"
Write-Host "=========================================="
Write-Host ""

# Task 1: Process Needs_Action every 5 minutes
Write-Host "Creating task: AI_Process_Tasks..."
$action1 = New-ScheduledTaskAction `
    -Execute "claude" `
    -Argument "/ai-employee-processor" `
    -WorkingDirectory $WorkingDir

$trigger1 = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).Date `
    -RepetitionInterval (New-TimeSpan -Minutes 5) `
    -RepetitionDuration ([TimeSpan]::MaxValue)

$settings1 = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

try {
    Unregister-ScheduledTask -TaskName "AI_Process_Tasks" -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask `
        -TaskName "AI_Process_Tasks" `
        -Action $action1 `
        -Trigger $trigger1 `
        -Settings $settings1 `
        -Description "Process AI Employee tasks from Needs_Action folder" | Out-Null
    Write-Host "✅ AI_Process_Tasks created"
} catch {
    Write-Host "❌ Failed to create AI_Process_Tasks: $_"
}

# Task 2: Execute Approved actions every 5 minutes
Write-Host "Creating task: AI_Execute_Approvals..."
$action2 = New-ScheduledTaskAction `
    -Execute "claude" `
    -Argument "/approval-manager" `
    -WorkingDirectory $WorkingDir

$trigger2 = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).Date `
    -RepetitionInterval (New-TimeSpan -Minutes 5) `
    -RepetitionDuration ([TimeSpan]::MaxValue)

$settings2 = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

try {
    Unregister-ScheduledTask -TaskName "AI_Execute_Approvals" -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask `
        -TaskName "AI_Execute_Approvals" `
        -Action $action2 `
        -Trigger $trigger2 `
        -Settings $settings2 `
        -Description "Execute approved AI Employee actions" | Out-Null
    Write-Host "✅ AI_Execute_Approvals created"
} catch {
    Write-Host "❌ Failed to create AI_Execute_Approvals: $_"
}

Write-Host ""
Write-Host "=========================================="
Write-Host "✅ Setup Complete"
Write-Host "=========================================="
Write-Host ""
Write-Host "Scheduled Tasks Created:"
Write-Host "  1. AI_Process_Tasks (every 5 min)"
Write-Host "  2. AI_Execute_Approvals (every 5 min)"
Write-Host ""
Write-Host "To start watchers manually:"
Write-Host "  cd watchers"
Write-Host "  python orchestrator.py --config config.json"
Write-Host ""
Write-Host "To view scheduled tasks:"
Write-Host "  Get-ScheduledTask | Where-Object {`$_.TaskName -like 'AI_*'}"
Write-Host ""
Write-Host "To remove scheduled tasks:"
Write-Host "  Unregister-ScheduledTask -TaskName 'AI_Process_Tasks' -Confirm:`$false"
Write-Host "  Unregister-ScheduledTask -TaskName 'AI_Execute_Approvals' -Confirm:`$false"
Write-Host "=========================================="
