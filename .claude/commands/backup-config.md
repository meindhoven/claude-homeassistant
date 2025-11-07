# Backup Home Assistant Configuration

Create a timestamped backup of the current configuration before making changes.

## What to do:

1. **Create Backup**:
   - Execute: `make backup`
   - This creates a timestamped tar.gz archive in the backups/ directory
   - Format: `backups/config-YYYYMMDD-HHMMSS.tar.gz`

2. **Verify Backup**:
   - Check that backup file was created successfully
   - Show backup file location and size
   - List what's included in the backup

3. **Backup Information**:
   - Show timestamp of backup
   - Show disk space used
   - List recent backups if multiple exist
   - Recommend keeping backups for key milestones

4. **Remind User**:
   - Backups are local only (not synced to HA)
   - Consider periodic archival to external storage
   - Can use backups for quick rollback if needed

## When to Use:

- **Before major changes**: Adding complex automations
- **Before bulk edits**: Renaming many entities
- **Before experiments**: Testing new configurations
- **After milestones**: Working configuration you want to preserve
- **Manual safety**: When you want extra peace of mind

## Backup Contents:

The backup includes:
- All configuration YAML files
- Entity registry data
- Scripts, automations, scenes
- Custom configurations

The backup excludes:
- secrets.yaml (not backed up for security)
- Temporary files
- Cache files

## Restore Process:

If you need to restore from backup:
```bash
# Extract backup
tar -xzf backups/config-YYYYMMDD-HHMMSS.tar.gz -C /tmp/restore

# Review extracted files
ls -la /tmp/restore/config/

# Copy files back (carefully!)
cp -r /tmp/restore/config/* config/

# Validate before deploying
make validate
```

## Output Format:

```
💾 Creating backup of Home Assistant configuration...

✅ Backup created successfully!

📦 Backup Details:
   Location: backups/config-20231107-143530.tar.gz
   Size: 2.4 MB
   Timestamp: 2023-11-07 14:35:30

📁 Contents:
   - config/*.yaml (23 files)
   - config/.storage/core.entity_registry
   - config/blueprints/ (12 files)
   - config/packages/ (5 files)

💡 Tip: Keep this backup safe. You can restore from it if needed.

Recent backups:
   1. config-20231107-143530.tar.gz (just created)
   2. config-20231106-095412.tar.gz (1 day ago)
   3. config-20231105-183021.tar.gz (2 days ago)
```

## Important:

- Backups are created before `make push` automatically
- You can create manual backups anytime with this command
- Old backups are not auto-deleted - manage them manually
- Consider external backup strategy for critical configs
