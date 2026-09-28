-- Workspace rules wiki https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/
-- Add your workspace rules here. Increment the workspace number as you go. Do not have duplicate workspaces.
hl.workspace_rule({ workspace = "name:gaming", monitor = PRIMARY_MONITOR })
hl.workspace_rule({ workspace = "1", monitor = MONITOR1, default = true, persistent = true })
for workspace = 2, 5 do
    hl.workspace_rule({ workspace = tostring(workspace), monitor = MONITOR1, persistent = true })
end

hl.workspace_rule({ workspace = "6", monitor = MONITOR2, default = true, persistent = true })
for workspace = 7, 10 do
    hl.workspace_rule({ workspace = tostring(workspace), monitor = MONITOR2, persistent = true })
end
