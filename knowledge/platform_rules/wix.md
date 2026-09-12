# Wix Rules

> Last updated: 2026-09-12
> Owner: Brett Sjoberg
> Scope: All Wix website and blog operations by the Contents Generator Workforce

---

## 1. Platform Overview

Wix is a cloud-based web development platform that uses drag-and-drop tools to create websites. It includes a built-in CMS for blog posts, a business management suite, and a code platform called Velo for advanced customization.

For the Contents Generator Workforce, Wix serves as a **complete website and blog publishing platform** — ideal for landing pages, portfolios, business websites, and blog content with built-in SEO and mobile optimization.

---

## 2. Content Requirements

### 2.1 Blog Post Structure

| Element | Requirement |
|---------|------------|
| **Title** | Engaging, keyword-rich, under 70 characters |
| **Featured Image** | Required for all posts |
| **Categories** | At least 1 |
| **Tags** | 3-8 relevant tags |
| **Meta Description** | Auto-generated or manual, under 160 characters |
| **Content** | Mobile-optimized, responsive |
| **SEO Score** | Wix SEO Wiz score of 80%+ |

### 2.2 Content Types

```text
blog_post          — Standard blog articles
page               — Static pages (About, Services, Contact)
portfolio          — Showcasing work/projects
gallery            — Image galleries
product            — Product listings (Wix Stores)
event              — Events and appointments
testimonial        — Customer reviews
book               — Bookable services
```

### 2.3 SEO Requirements

- **Title tag** under 60 characters
- **Meta description** under 160 characters
- **SEO Wiz** optimization score of 80%+
- **Heading tags** properly structured
- **Image alt text** on all media
- **Mobile responsive** design
- **Fast page load** (under 3 seconds)
- **Custom URL** with keywords

---

## 3. Publishing Workflow

### 3.1 Standard Workflow

```text
DRAFT → QA PASS → SEO CHECK → APPROVAL → PUBLISH
```

### 3.2 Workflow Steps

1. **Generate** content via Content/Social/Article agents
2. **Fact Check** all claims
3. **SEO Audit** using Wix SEO Wiz
4. **QA** — brand voice, grammar, formatting
5. **Design layout** — Ensure mobile responsive
6. **Add meta tags and SEO settings**
7. **Publish** via Composio Wix integration

### 3.3 Scheduled Publishing

- Wix supports scheduling posts for future dates
- Best posting times (Australia/Sydney):
  - **07:00** — Morning audience
  - **13:00** — Lunch break
  - **19:00** — Evening readers
- Frequency: 1-2 posts per week
- Always use Wix scheduling feature

---

## 4. Content Rules

### 4.1 Required Practices

- [ ] Use Wix SEO Wiz for optimization
- [ ] Enable mobile responsive design
- [ ] Add alt text to all images
- [ ] Use proper heading structure (H1, H2, H3)
- [ ] Set custom URLs with keywords
- [ ] Add meta titles and descriptions
- [ ] Include internal linking
- [ ] Use Wix Analytics to track performance

### 4.2 Prohibited Practices

- [ ] No non-responsive designs
- [ ] No missing meta tags
- [ ] No excessive animations that slow page load
- [ ] No auto-playing videos (user consent required)
- [ ] No duplicate content
- [ ] No broken links

---

## 5. Wix-Specific Considerations

### 5.1 Wix Editor

- Use **Wix Editor** for visual page creation
- Use **Wix Velo** for custom code and logic
- Use **Wix ADI** (Artificial Design Intelligence) for quick setups
- Use **Wix Blocks** for reusable design components
- All content must be **mobile responsive** by default

### 5.2 Media Management

- Upload images at optimized web resolution
- Wix automatically optimizes for mobile
- Use WebP format when possible
- Maximum media file size: 50MB
- Use Wix Media Manager for organization

### 5.3 Wix Business Suite

For business-oriented content:
- **Wix Bookings** — Schedule appointments
- **Wix Payments** — Accept payments
- **Wix Restaurants** — Menu and reservations
- **Wix Chat** — Live chat integration
- **Wix Business Manager** — Central dashboard

---

## 6. Analytics & Monitoring

### 6.1 Key Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Page views | Track daily | Wix Analytics |
| Unique visitors | Track weekly | Wix Analytics |
| Bounce rate | < 50% | Wix Analytics |
| SEO Score | > 80% | Wix SEO Wiz |
| Mobile score | > 90% | Google PageSpeed |
| Conversion rate | Track monthly | Wix Analytics |

### 6.2 Monitoring via Composio

```text
wix_get_analytics
wix_get_traffic
wix_get_seo_score
wix_get_visitors
wix_get_conversions
wix_get_performance
```

---

## 7. Composio Integration

### 7.1 Available Tools

```text
wix_create_blog_post
wix_update_blog_post
wix_publish_blog_post
wix_upload_media
wix_get_blog_posts
wix_get_pages
wix_get_analytics
wix_get_seo_wiz
wix_create_page
wix_manage_menu
wix_manage_settings
wix_get_visitors
wix_get_conversions
```

### 7.2 Authentication

```text
1. Create a Wix Business account at https://www.wix.com/business
2. Register for Wix Velo API access
3. Use OAuth 2.0 authentication via Composio
4. Store credentials securely in .env
5. Use session management via ComposioSessionManager
```

---

## 8. Integration with Other Platforms

Wix content can be repurposed across the entire workforce:

| Source | Repurposed To | Format |
|--------|--------------|--------|
| Wix blog post | X thread | 8-15 tweet thread |
| Wix blog post | LinkedIn article | Summary + link |
| Wix blog post | Facebook post | Excerpt + link |
| Wix blog post | TikTok video | Key points as script |
| Wix portfolio | Instagram gallery | Visual highlights |
| Wix page | Newsletter | Weekly digest |
| Wix landing page | Facebook ad | Ad copy + link |

---

## 9. Agent Access

| Agent | Access Level | Tools |
|-------|-------------|-------|
| Content Strategy | Read/Write | wix_create_page, wix_manage_settings |
| Social Content | Read | wix_get_blog_posts |
| Publishing Agent | Write | wix_publish_blog_post |
| Analytics Agent | Read | wix_get_analytics |
| SEO Agent | Read/Write | wix_get_seo_wiz, wix_update_blog_post |
| Repurposing Agent | Read | wix_get_blog_posts |

---

## 10. Best Practices Summary

1. **Always use mobile responsive** — 60%+ traffic is mobile
2. **Run Wix SEO Wiz** — Ensure 80%+ optimization score
3. **Use scheduling** — Consistent publishing builds audience
4. **Monitor Wix Analytics** — Track what works
5. **Repurpose across platforms** — Maximum content ROI
6. **Use Velo for customization** — Advanced logic when needed
7. **Use Composio for integration** — No manual API calls

---

> **Last updated:** 2026-09-12
> **Owner:** Brett Sjoberg
> **Scope:** All Wix operations for the Contents Generator Workforce