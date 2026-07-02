# Deploy

Release flow:

1. identify component, environment, image/artifact authority, and deployment script
2. dry-run where supported
3. deploy dev or staging first
4. run smoke checks that match the change
5. promote to prod only after dev is clean
6. update the default artifact authority after acceptance when required

Do not broaden rollout scope beyond the target component without approval.

