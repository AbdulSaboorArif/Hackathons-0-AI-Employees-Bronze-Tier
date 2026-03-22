# Twitter/X Poster Skill

**Description**: Automatically post content on Twitter/X to generate business leads and engagement using Playwright automation.

## Capabilities

- Post text tweets (up to 280 characters)
- Post threads (multiple tweets)
- Post with images/media
- Persistent browser session (login once)
- Human-in-the-loop approval workflow
- Screenshot verification
- Post tracking and logging

## Setup

1. **Install Dependencies**:
```bash
cd .claude/skills/twitter-poster
pip install -r requirements.txt
playwright install chromium
```

2. **Initial Login** (one-time):
```bash
python scripts/setup_twitter_session.py
```
This opens a browser where you log into Twitter/X. Session is saved for future use.

3. **Test Posting**:
```bash
python scripts/post_to_twitter.py \
  --vault "../../AI_Employee_Vault" \
  --session "../../watchers/twitter/.browser-session" \
  --approval-file "../../AI_Employee_Vault/Approved/TWITTER_TEST.md"
```

## Approval File Format

Create files in `AI_Employee_Vault/Pending_Approval/` with this format:

```markdown
---
type: twitter_post
status: pending
created: 2026-03-21T20:00:00Z
thread: false
---

# Twitter Post

Your tweet content goes here. Keep under 280 characters for single tweets.

For threads, separate tweets with ---

First tweet content here (280 chars max)

---

Second tweet content here (280 chars max)

---

Third tweet content here (280 chars max)
```

## Character Limits

- **Single Tweet**: 280 characters
- **Thread**: Multiple tweets, each 280 characters
- **With Media**: 280 characters + 4 images max

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
type: twitter_post
status: pending
created: {datetime.now().isoformat()}
thread: false
---

# Twitter Post

{tweet_content}
"""

# Save to Pending_Approval
with open('AI_Employee_Vault/Pending_Approval/TWITTER_POST_20260321.md', 'w') as f:
    f.write(approval_content)
```

## Thread Posting

For multi-tweet threads:

```markdown
---
type: twitter_post
status: pending
thread: true
---

# Twitter Thread

Tweet 1: Introduction to our new AI Employee system 🚀

---

Tweet 2: It handles email, WhatsApp, LinkedIn, and now Twitter automatically!

---

Tweet 3: Human-in-the-loop approval ensures safety. Learn more at example.com
```

## Security

⚠️ **Important**:
- Session stored locally only
- Never commit `.browser-session/` folder
- Review all posts before approval
- Twitter may detect automation - use responsibly
- Respect Twitter's Terms of Service
- Don't spam or violate rules

## Troubleshooting

**Session expired**:
```bash
# Re-login
python scripts/setup_twitter_session.py
```

**Post failed**:
- Check screenshot in logs
- Verify Twitter UI hasn't changed
- Check for rate limiting
- Ensure account is in good standing
- Check character count

**Rate limited**:
- Twitter has strict rate limits
- Wait before retrying
- Don't post too frequently
- Consider spacing out posts

**Selectors not working**:
- Twitter frequently updates UI
- Update selectors in `post_to_twitter.py`
- Check browser console for errors

## Best Practices

1. **Character Count**: Always verify tweets are under 280 characters
2. **Timing**: Space out posts (at least 5 minutes apart)
3. **Content**: Provide value, don't spam
4. **Engagement**: Monitor replies and engagement
5. **Compliance**: Follow Twitter rules and guidelines

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Twitter Rules](https://help.twitter.com/en/rules-and-policies/twitter-rules)
- [Twitter Automation Rules](https://help.twitter.com/en/rules-and-policies/twitter-automation)
