# WordPress Rules

> Last updated: 2026-09-12
> Owner: Brett Sjoberg
> Scope: All WordPress posting and content management by the Contents Generator Workforce

---

## 1. Platform Overview

WordPress is the world's most popular content management system, powering over 40% of all websites. It supports flexible content types (posts, pages, custom post types), extensive plugin ecosystem, and robust SEO capabilities through plugins like Yoast and Rank Math.

For the Contents Generator Workforce, WordPress serves as a **primary publishing destination** for long-form content, articles, blog posts, and landing pages.

---

## 2. Content Requirements

### 2.1 Post Structure

| Element | Requirement |
|---------|------------|
| **Title** | Compelling, keyword-rich, under 60 characters |
| **Featured Image** | Required for all posts (1200x630px recommended) |
| **Categories** | At least 1, maximum 5 |
| **Tags** | 3-10 relevant tags |
| **Excerpt** | Auto-generated or manual, under 160 characters |
| **Content** | Well-structured with headings, paragraphs, and blocks |
| **SEO** | Yoast/Rank Math score of 70+ required |

### 2.2 Content Types

```text
blog_post          — Standard articles (default type)
page               — Static pages (About, Services, Contact)
portfolio          — Showcasing work
testimonial        — Customer reviews/reviews
product_review     — Product evaluation posts
tutorial           — Step-by-step guides
comparison         — Head-to-head comparisons
news               — Industry news updates
lifestyle          — Personal/storytelling content
```

### 2.3 SEO Requirements

- **Primary keyword** in title, first paragraph, and meta description
- **Meta title** under 60 characters
- **Meta description** under 160 characters
- **Internal links** to at least 2 related posts
- **Image alt text** on all featured images
- **Heading hierarchy** (H1 → H2 → H3)
- **Word count** minimum 800 words for blog posts

---

## 3. Publishing Workflow

### 3.1 Standard Workflow

```text
DRAFT → QA PASS → SEO CHECK → APPROVAL → PUBLISH
```

### 3.2 Workflow Steps

1. **Generate** article via Article Writer Agent
2. **Fact Check** all claims
3. **SEO Audit** — keyword placement, meta tags, headings
4. **QA** — brand voice, grammar, formatting
5. **Set featured image** via Composio Wix/WordPress media upload
6. **Add categories and tags**
7. **Set publish date** (scheduled publishing)
8. **Publish** via Composio WordPress integration

### 3.3 Scheduled Publishing

- Best posting times (Australia/Sydney):
  - **06:00** — Early morning readers
  - **12:00** — Lunch break audience
  - **18:00** — Evening readers
- Frequency: 1-2 posts per week minimum
- Always publish consistently

---

## 4. Content Rules

### 4.1 Required Practices

- [ ] Use featured images on every post
- [ ] Add proper categories and tags
- [ ] Include internal links (2-5 per post)
- [ ] Optimize for SEO (Yoast/Rank Math)
- [ ] Use heading hierarchy (H1, H2, H3)
- [ ] Add alt text to images
- [ ] Write compelling meta descriptions
- [ ] Include calls-to-action

### 4.2 Prohibited Practices

- [ ] No keyword stuffing
- [ ] No duplicate content
- [ ] No thin content (under 300 words)
- [ ] No broken links
- [ ] No excessive plugin usage that slows page speed
- [ ] No auto-generated content without human review

---

## 5. WordPress-Specific Considerations

### 5.1 Block Editor (Gutenberg)

- Use block-based formatting (paragraph, heading, image, quote, list)
- Avoid classic editor formatting
- Use columns and group blocks sparingly
- Add custom HTML blocks only when necessary

### 5.2 Media Management

- Upload images at proper resolution (max 2500px wide)
- Compress images before upload (use Composio media tools)
- Add descriptive file names and alt text
- Use WebP format when possible
- Set featured images from the media library

### 5.3 Custom Post Types

For specialized content, the workforce can use custom post types:
- `portfolio` — Showcasing projects
- `testimonial` — Customer reviews
- `product_review` — Product evaluations
- `case_study` — Detailed case studies

---

## 6. Analytics & Monitoring

### 6.1 Key Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Page views | Track weekly | WordPress admin |
| Time on page | > 3 minutes | Google Analytics |
| Bounce rate | < 60% | Google Analytics |
| SEO score | > 70% | Yoast/Rank Math |
| Social shares | Track per post | Social sharing plugins |
| Lead conversions | Track monthly | Contact form submissions |

### 6.2 Monitoring via Composio

```text
wordpress_get_post_analytics
wordpress_get_traffic_sources
wordpress_get_search_console_data
wordpress_get_reader_stats
```

---

## 7. Composio Integration

### 7.1 Available Tools

```text
wordpress_create_post
wordpress_update_post
wordpress_publish_post
wordpress_upload_media
wordpress_get_posts
wordpress_get_categories
wordpress_get_tags
wordpress_get_post_analytics
wordpress_get_comments
wordpress_manage_revisions
wordpress_create_page
wordpress_manage_media
```

### 7.2 Authentication

```text
1. Create a WordPress app at https://wordpress.com/apps
2. Use OAuth 2.0 authentication via Composio
3. Store credentials securely in .env
4. Use session management via ComposioSessionManager
```

---

## 8. Integration with Other Platforms

WordPress content can be repurposed to other platforms:

| Source | Repurposed To | Format |
|--------|--------------|--------|
| Long article | X thread | 8-15 tweet thread |
| Long article | LinkedIn post | Short summary + link |
| Long article | Facebook post | Excerpt + link |
| Long article | TikTok script | Key points as video script |
| Long article | Blog summary | Newsletter format |
| Long article | Instagram carousel | Key points as slides |
| Long article | Medium repost | Cross-post excerpt |

---

## 9. Agent Access

| Agent | Access Level | Tools |
|-------|-------------|-------|
| Article Writer | Read/Write | wordpress_create_post, wordpress_upload_media |
| SEO Agent | Read/Write | wordpress_update_post, wordpress_get_posts |
| Publishing Agent | Write | wordpress_publish_post, wordpress_manage_media |
| Analytics Agent | Read | wordpress_get_post_analytics |
| Repurposing Agent | Read | wordpress_get_posts |

---

## 10. Best Practices Summary

1. **Always use featured images** — Increases engagement by 2-3x
2. **SEO optimize every post** — Rank on page 1 of Google
3. **Use categories and tags** — Improves site organization
4. **Schedule consistently** — Build audience trust
5. **Repurpose across platforms** — Maximum content ROI
6. **Monitor analytics** — Learn what works
7. **Use Composio for integration** — No manual API calls

---

> **Last updated:** 2026-09-12
> **Owner:** Brett Sjoberg
> **Scope:** All WordPress operations for the Contents Generator Workforce