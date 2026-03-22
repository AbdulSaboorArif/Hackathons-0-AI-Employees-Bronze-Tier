---
name: linkedin-poster
description: |
  Automatically post content on LinkedIn to generate business leads and engagement.
  Creates posts from templates, schedules content, and tracks engagement. Use this
  skill when you need to maintain LinkedIn presence, share business updates, or
  generate sales leads through social media.
---

# LinkedIn Poster

Automate LinkedIn posting for business development and lead generation.

## Core Workflow

1. **Read** post templates from `/LinkedIn_Content` folder
2. **Generate** engaging posts based on business context
3. **Create** approval requests for posts in `/Pending_Approval`
4. **Post** to LinkedIn after approval using Playwright MCP
5. **Track** engagement and update Dashboard

## Usage

```bash
# Post a business update
/linkedin-poster

# Or invoke directly
claude "Create and post a LinkedIn update about our latest project"
```

## What This Skill Does

### Content Generation
- Reads business context from Company_Handbook.md
- Generates professional LinkedIn posts
- Follows LinkedIn best practices (hashtags, length, tone)
- Creates engaging content for lead generation

### Post Management
- Creates draft posts in /LinkedIn_Content/Drafts
- Requests approval before posting
- Schedules posts for optimal times
- Tracks post performance

### Lead Generation
- Identifies trending topics in your industry
- Suggests content that drives engagement
- Monitors comments for potential leads
- Creates follow-up tasks for warm leads

## Post Templates

### Business Update Template
```markdown
---
type: linkedin_post
category: business_update
status: draft
---

🚀 Exciting news from [Your Business]!

[Main announcement or update]

Key highlights:
• [Benefit 1]
• [Benefit 2]
• [Benefit 3]

[Call to action]

#YourIndustry #BusinessGrowth #Innovation
```

### Thought Leadership Template
```markdown
---
type: linkedin_post
category: thought_leadership
status: draft
---

💡 [Insightful question or statement]

After [X years/months] in [industry], I've learned that:

[Key insight 1]
[Key insight 2]
[Key insight 3]

What's your experience with this? Let me know in the comments!

#Leadership #Industry #ProfessionalDevelopment
```

## Approval Workflow

Before posting, the skill creates an approval file:

```markdown
# /Pending_Approval/LINKEDIN_POST_2026-03-15.md
---
type: approval_request
action: linkedin_post
created: 2026-03-15T10:00:00Z
expires: 2026-03-15T18:00:00Z
status: pending
---

## Post Content

🚀 Exciting news from our team!

We just completed a major project milestone...

[Full post content]

## Engagement Strategy
- Best time to post: 9:00 AM Tuesday
- Target audience: Business owners, entrepreneurs
- Expected reach: 500-1000 impressions

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder or add feedback.
```

## LinkedIn Automation via Playwright

The skill uses Playwright MCP to interact with LinkedIn:

```bash
# 1. Start Playwright server
bash .claude/skills/browsing-with-playwright/scripts/start-server.sh

# 2. Navigate to LinkedIn
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://www.linkedin.com"}'

# 3. Login (first time only - session persists)
# Use browser_snapshot to find login elements
# Use browser_type and browser_click to login

# 4. Create post
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Start a post", "ref": "e10"}'

# 5. Type content
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_type \
  -p '{"element": "Post text area", "ref": "e15", "text": "Your post content here"}'

# 6. Click Post button
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Post button", "ref": "e20"}'

# 7. Take screenshot for verification
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": false}'
```

## Content Strategy

### Posting Frequency
- Minimum: 3 posts per week
- Optimal: 1 post per day
- Maximum: 2 posts per day

### Best Times to Post
- Tuesday-Thursday: 9:00 AM - 11:00 AM
- Tuesday-Wednesday: 12:00 PM - 1:00 PM
- Avoid: Weekends, early mornings, late evenings

### Content Mix (80/20 Rule)
- 80% Value: Tips, insights, industry news
- 20% Promotion: Services, products, offers

## Engagement Tracking

The skill monitors post performance:

```markdown
# /LinkedIn_Content/Analytics/2026-03-15_post.md
---
post_date: 2026-03-15T09:00:00Z
post_url: https://linkedin.com/posts/...
---

## Metrics (24 hours)
- Impressions: 847
- Likes: 23
- Comments: 5
- Shares: 2
- Profile views: 12

## Lead Indicators
- 3 connection requests from target audience
- 2 direct messages about services
- 1 comment expressing interest

## Follow-up Actions
- [ ] Respond to all comments
- [ ] Connect with engaged users
- [ ] Follow up on DMs
```

## Configuration

Edit `Company_Handbook.md` to customize:

```markdown
## LinkedIn Strategy

### Brand Voice
- Professional but approachable
- Focus on practical value
- Share real experiences

### Target Audience
- Business owners
- Entrepreneurs
- [Your specific audience]

### Topics to Cover
- Industry insights
- Project case studies
- Tips and best practices
- Company updates

### Topics to Avoid
- Politics
- Controversial subjects
- Overly promotional content
```

## Silver Tier Capabilities

✅ Generate LinkedIn posts from templates
✅ Request approval before posting
✅ Post via Playwright automation
✅ Track basic engagement metrics
✅ Create follow-up tasks for leads
✅ Schedule posts for optimal times

## Future Enhancements (Gold Tier)

- AI-generated content based on trending topics
- Automated comment responses
- Lead scoring and CRM integration
- A/B testing for post formats
- Multi-platform posting (Twitter, Facebook)

## Security Notes

- LinkedIn session stored in persistent browser context
- Never share login credentials in posts or logs
- Review all posts before publishing
- Monitor for unusual activity

## Troubleshooting

**Post not appearing:**
- Check if LinkedIn flagged it as spam
- Verify you're logged in
- Check character limits (3000 max)

**Low engagement:**
- Review posting times
- Improve content quality
- Use relevant hashtags (3-5 max)
- Engage with others' content first

**Automation detected:**
- Add random delays between actions
- Don't post too frequently
- Vary content and timing
- Use human-like interaction patterns

---
*Part of the Silver Tier AI Employee implementation*
