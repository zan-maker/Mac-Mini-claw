# OpenUtter Authentication Guide

## Why Authenticate?

Without authentication, OpenUtter joins as a guest and waits in the lobby for host approval. This often fails if:
- Host doesn't notice the guest
- Meeting has guest restrictions
- Host rejects unknown guests

With authentication, OpenUtter joins as your Google account, which is much more reliable.

## Setup Authentication

1. **Run authentication command:**
   ```bash
   npx openutter auth
   ```

2. **Browser opens:** Sign in to your Google account

3. **Return to terminal:** Press Enter when done

## Files Created

- `~/.openutter/auth.json` - Encrypted session
- `~/.openutter/auth-meta.json` - Session metadata
- `~/.openutter/chrome-profile/` - Persistent browser profile

## Joining Meetings

**With authentication (recommended):**
```bash
npx openutter join https://meet.google.com/abc-defg-hij --auth
```

**As guest (less reliable):**
```bash
npx openutter join https://meet.google.com/abc-defg-hij --anon --bot-name "Investor Bot"
```

## Troubleshooting Authentication

### Session Expired
Run `npx openutter auth` again to refresh.

### Authentication Failed
1. Check you're signed into Google in the browser
2. Ensure you have permission to join the meeting
3. Try incognito/private browsing mode

### Browser Doesn't Open
Run with `--headed` flag:
```bash
npx openutter auth --headed
```

## Security Notes

- Session is encrypted and stored locally
- Only used for meeting joins
- Can be deleted anytime: `rm -rf ~/.openutter/`
