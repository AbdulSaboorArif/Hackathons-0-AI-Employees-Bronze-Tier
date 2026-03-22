# Instagram Poster Skill

**Description**: Automatically post content on Instagram to generate business leads and engagement using Playwright automation.

## Capabilities

- Post photos with captions to Instagram
- Post to Instagram Feed
- Persistent browser session (login once)
- Human-in-the-loop approval workflow
- Screenshot verification
- Post tracking and logging

## Setup

1. **Install Dependencies**:
```bash
cd .claude/skills/instagram-poster
pip install -r requirements.txt
playwright install chromium
```

2. **Initial Login** (one-time):
```bash
python scripts/setup_instagram_session.py
```
This opens a browser where you log into Instagram. Session is saved for future use.

3. **Test Posting**:
```bash
python scripts/post_to_instagram.py \
  --vault "../../AI_Employee_Vault" \
  --session "../../watchers/instagram/.browser-session" \
  --approval-file "../../AI_Employee_Vault/Approved/INSTAGRAM_TEST.md"
```

## Approval File Format

Create files in `AI_Employee_Vault/Pending_Approval/` with this format:

```markdown
---
type: instagram_post
status: pending
created: 2026-03-21T20:00:00Z
image_path: path/to/image.jpg
---

# Instagram Post Caption

Your caption goes here. Can include:
- Multiple lines
- Emojis 🚀
- Hashtags #business #ai #entrepreneur
- Mentions @username

Keep under 2,200 characters (Instagram limit).
```

## Image Requirements

- **Format**: JPG, PNG
- **Size**: Max 8MB
- **Aspect Ratio**: 1:1 (square), 4:5 (portrait), or 1.91:1 (landscape)
- **Resolution**: Min 320px, recommended 1080px

## Workflow

1. **Create Post**: AI creates approval file with image path in `/Pending_Approval/`
2. **Human Review**: You review image and caption, move to `/Approved/`
3. **Auto-Post**: Watcher detects approved file and posts
4. **Verification**: Screenshot saved, logged to `/Logs/`
5. **Archive**: File moved to `/Done/`

## Usage in Claude Code

```python
# Claude creates approval request
approval_content = f"""---
type: instagram_post
status: pending
created: {datetime.now().isoformat()}
image_path: AI_Employee_Vault/Media/business_update.jpg
---

# Instagram Post

{caption_content}
"""

# Save to Pending_Approval
with open('AI_Employee_Vault/Pending_Approval/INSTAGRAM_POST_20260321.md', 'w') as f:
    f.write(approval_content)
```

## Security

⚠️ **Important**:
- Session stored locally only
- Never commit `.browser-session/` folder
- Review all posts before approval
- Instagram may detect automation - use responsibly
- Respect Instagram's Terms of Service
- Don't spam or violate community guidelines

## Troubleshooting

**Session expired**:
```bash
# Re-login
python scripts/setup_instagram_session.py
```

**Post failed**:
- Check screenshot in logs
- Verify Instagram UI hasn't changed
- Check for rate limiting
- Ensure account is in good standing
- Verify image format and size

**Image upload failed**:
- Check image path is correct
- Verify image format (JPG/PNG)
- Check file size (< 8MB)
- Try different aspect ratio

**Selectors not working**:
- Instagram frequently updates UI
- Update selectors in `post_to_instagram.py`
- Check browser console for errors

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Instagram Community Guidelines](https://help.instagram.com/477434105621119)
- [Instagram Image Specifications](https://help.instagram.com/1631821640426723)
