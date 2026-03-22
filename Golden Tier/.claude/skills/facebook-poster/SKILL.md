# Facebook Poster Skill

**Description**: Automatically post content on Facebook to generate business leads and engagement using Playwright automation.

## Capabilities

- Post text updates to Facebook
- Post with images/media
- Persistent browser session (login once)
- Human-in-the-loop approval workflow
- Screenshot verification
- Post tracking and logging

## Setup

1. **Install Dependencies**:
```bash
cd .claude/skills/facebook-poster
pip install -r requirements.txt
playwright install chromium
```

2. **Initial Login** (one-time):
```bash
python scripts/setup_facebook_session.py
```
This opens a browser where you log into Facebook. Session is saved for future use.

3. **Test Posting**:
```bash
python scripts/post_to_facebook.py \
  --vault "../../AI_Employee_Vault" \
  --session "../../watchers/facebook/.browser-session" \
  --approval-file "../../AI_Employee_Vault/Approved/FACEBOOK_TEST.md"
```

## Approval File Format

Create files in `AI_Employee_Vault/Pending_Approval/` with this format:

```markdown
---
type: facebook_post
status: pending
created: 2026-03-21T20:00:00Z
---

# Facebook Post Content

Your post content goes here. Can include:
- Multiple paragraphs
- Emojis 🚀
- Hashtags #business #ai
- Links https://example.com

Keep under 63,206 characters (Facebook limit).
```

## Workflow

1. **Create Post**: AI creates approval file in `/Pending_Approval/`
2. **Human Review**: You review and move to `/Approved/`
3. **Auto-Post**: Watcher detects approved file and posts
4. **Verification**: Screenshot saved, logged to `/Logs/`
5. **Archive**: File moved to `/Done/`

## Usage in Claude Code

```python
# Claude creates approval request
approval_content = f"""---
type: facebook_post
status: pending
created: {datetime.now().isoformat()}
---

# Facebook Post

{post_content}
"""

# Save to Pending_Approval
with open('AI_Employee_Vault/Pending_Approval/FACEBOOK_POST_20260321.md', 'w') as f:
    f.write(approval_content)
```

## Security

⚠️ **Important**:
- Session stored locally only
- Never commit `.browser-session/` folder
- Review all posts before approval
- Facebook may detect automation - use responsibly
- Respect Facebook's Terms of Service

## Troubleshooting

**Session expired**:
```bash
# Re-login
python scripts/setup_facebook_session.py
```

**Post failed**:
- Check screenshot in logs
- Verify Facebook UI hasn't changed
- Check for rate limiting
- Ensure account is in good standing

**Selectors not working**:
- Facebook frequently updates UI
- Update selectors in `post_to_facebook.py`
- Check browser console for errors

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Facebook Community Standards](https://transparency.fb.com/policies/community-standards/)
