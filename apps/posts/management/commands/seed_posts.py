from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.authors.models import AuthorProfile
from apps.posts.models import Post, PostStatus

User = get_user_model()

POSTS = [
    {
        "title": "NVIDIA: The AI Infrastructure King Powering the Next Decade",
        "excerpt": "NVIDIA's GPU dominance has evolved far beyond gaming into the backbone of AI training and inference, making it the most critical hardware company of the 2020s.",
        "tags": ["NVDA", "AI", "semiconductors", "GPU"],
        "body": """## Why NVIDIA Is More Than a Chip Company

NVIDIA (NASDAQ: NVDA) has undergone one of the most remarkable transformations in tech history. What started as a graphics card company for gamers is now the **essential infrastructure layer for artificial intelligence**.

### The Numbers Speak for Themselves

| Metric | FY2023 | FY2024 | YoY Growth |
|--------|--------|--------|------------|
| Revenue | $26.9B | $60.9B | +126% |
| Data Center Revenue | $15.0B | $47.5B | +217% |
| Net Income | $4.4B | $29.8B | +581% |
| Gross Margin | 56.9% | 72.7% | +18pp |

### The CUDA Moat

NVIDIA's real competitive advantage isn't just the H100 or B100 chips — it's **CUDA**, the parallel computing platform that has a 15-year head start over any competitor. Tens of thousands of AI researchers and engineers have built their workflows around CUDA. Switching costs are enormous.

### Risks to Watch

- **AMD** is closing the gap with MI300X chips and ROCm software stack
- **Custom silicon** from Google (TPUs), Amazon (Trainium), Microsoft (Maia) threatens to commoditize training workloads
- **China export restrictions** cut off a significant addressable market
- Valuation: trading at 35x forward revenue requires flawless execution

### The Bull Case

The global AI infrastructure buildout is measured in **hundreds of billions of dollars**. Every hyperscaler — AWS, Azure, GCP, Oracle, Meta — is racing to provision GPU capacity. NVIDIA captures the overwhelming majority of this spend.

> "We are at the beginning of a new industrial revolution. AI factories are being built worldwide, and NVIDIA is the pick-and-shovel play." — Jensen Huang, CEO

### Conclusion

NVIDIA is not cheap. But for investors with a 5-year horizon, the question isn't whether AI compute demand will grow — it's whether anyone can displace CUDA's ecosystem lock-in before the next paradigm shift arrives.

**Disclosure:** This is not financial advice. Do your own research.
""",
    },
    {
        "title": "Microsoft: The Quiet AI Winner Hiding in Plain Sight",
        "excerpt": "While the market fixates on Nvidia's GPU sales, Microsoft is quietly becoming the most diversified AI monetization engine in the world through Azure, Copilot, and its OpenAI partnership.",
        "tags": ["MSFT", "cloud", "AI", "Azure", "Copilot"],
        "body": """## Microsoft's AI Strategy Is Working

Microsoft (NASDAQ: MSFT) made the boldest bet in tech history when it invested $13 billion into OpenAI. That bet is now paying off across every product line.

### Azure AI: The Monetization Engine

Azure's AI services — including exclusive access to GPT-4 and GPT-4o through Azure OpenAI Service — are driving a reacceleration in cloud revenue growth that analysts didn't see coming.

- **Azure grew 29% YoY** in the most recent quarter, with AI contributing 7 percentage points
- **Azure OpenAI Service** now serves over 65,000 customers
- Microsoft 365 Copilot has crossed **1 million paid seats** in enterprise

### The Copilot Flywheel

The genius of Microsoft's strategy is that Copilot is embedded in products people already pay for. This creates **zero-friction upsell** paths:

1. Office 365 customer → Microsoft 365 Copilot ($30/user/month premium)
2. Azure customer → Azure OpenAI API calls
3. GitHub user → GitHub Copilot ($10-19/month per developer)
4. LinkedIn user → AI-assisted recruiting and job matching

### Financial Snapshot

| Segment | Revenue (TTM) | Growth |
|---------|---------------|--------|
| Productivity & Business | $77B | +13% |
| Intelligent Cloud | $87B | +21% |
| More Personal Computing | $54B | +8% |

### Risks

- **OpenAI dependency**: If the relationship sours or OpenAI goes public with different terms, Azure's AI differentiation shrinks
- **Antitrust scrutiny** around the OpenAI relationship is intensifying in the EU and UK
- AWS and GCP are not sitting still — both have competitive foundation model offerings

### Why Microsoft Wins Long-Term

Microsoft has something no startup can replicate: **enterprise trust**. Fortune 500 CIOs have been buying Microsoft software for 40 years. When they need to deploy AI, they default to vendors they already trust with their data. Microsoft is that vendor.

**Disclosure:** This is not financial advice. Do your own research.
""",
    },
    {
        "title": "Apple: The Services Flywheel and Why the Hardware Plateau Doesn't Matter",
        "excerpt": "iPhone unit growth has stalled, but Apple's services business is compounding at 15%+ annually with 90%+ gross margins. The market may be undervaluing the platform.",
        "tags": ["AAPL", "services", "iPhone", "ecosystem"],
        "body": """## Rethinking the Apple Investment Thesis

Apple (NASDAQ: AAPL) is one of the most debated stocks on Wall Street. Bears point to slowing iPhone growth in China and a lack of a clear AI strategy. Bulls see an unassailable ecosystem with 2.2 billion active devices.

### The Services Business Is the Story

Most investors still think of Apple as a hardware company. That's a mistake.

| Metric | FY2022 | FY2023 | FY2024E |
|--------|--------|--------|---------|
| Services Revenue | $78B | $85B | $98B |
| Services Gross Margin | 71% | 74% | 75%+ |
| Hardware Gross Margin | 36% | 37% | 37% |

Services — including the App Store, iCloud, Apple TV+, Apple Arcade, Apple Pay, and licensing deals with Google — now represents **~25% of revenue but ~40% of gross profit**.

### The Google Deal: A Hidden Asset

Apple reportedly receives **$18-20 billion per year** from Google to be the default search engine on Safari. This is essentially free money — a toll road on user intent. When this deal faces antitrust risk, Apple stock dips. But the structural value of Safari's default position remains regardless of who pays for it.

### Apple Intelligence: Late but Not Lost

Apple's AI strategy (Apple Intelligence) focuses on **on-device processing** for privacy — a differentiated positioning when consumers are increasingly concerned about cloud AI data practices. Integration with ChatGPT for complex queries gives users the best of both worlds.

### China Risk Is Real

China represents ~19% of Apple's revenue, and Huawei's comeback with the Mate 60 Pro has demonstrated that premium Android alternatives are viable. However, Apple's ecosystem switching costs remain high even in China.

### The Buyback Machine

Apple has returned over **$700 billion to shareholders** since 2012 through buybacks and dividends. With $162 billion in cash and equivalents, the program is far from over. Every year, the share count drops ~3%, mechanically lifting EPS.

**Disclosure:** This is not financial advice. Do your own research.
""",
    },
    {
        "title": "Alphabet: Is the Search Giant's Moat Wider or Narrower Than You Think?",
        "excerpt": "The AI search threat to Google is real but overstated. Alphabet's advertising business, YouTube, and Google Cloud make it one of the most diversified AI beneficiaries in the market.",
        "tags": ["GOOGL", "search", "advertising", "Google Cloud", "YouTube"],
        "body": """## The Google Search Disruption Debate

Alphabet (NASDAQ: GOOGL) faces an existential question: can AI-powered search competitors like Perplexity, ChatGPT, and even Microsoft Bing erode Google's 90%+ search market share?

The short answer: not quickly, and probably not as much as the bears fear.

### Why Google's Search Moat Persists

1. **Index depth**: Google has crawled and indexed the web for 25 years. Competitors cannot replicate this overnight.
2. **Distribution**: Google is the default on Android (3 billion devices), Chrome (3.3 billion users), and most carrier agreements.
3. **AI Overviews**: Google's own AI search integration is rolling out to billions of users already within the existing search interface.
4. **Advertiser relationships**: Hundreds of thousands of businesses have built entire marketing stacks around Google Ads. Switching costs are enormous.

### The Cloud Acceleration

Google Cloud is the most under-appreciated part of Alphabet's business.

| Quarter | Google Cloud Revenue | YoY Growth | Operating Margin |
|---------|---------------------|------------|-----------------|
| Q1 2023 | $7.5B | +28% | -7% |
| Q1 2024 | $9.6B | +28% | +17% |
| Q2 2024 | $10.3B | +29% | +11% |

Cloud went from loss-making to generating **$1B+ in quarterly operating profit** in just 12 months. This inflection is significant.

### YouTube: The Attention Economy Anchor

YouTube is the #1 streaming platform by watch time in the US, surpassing Netflix on connected TVs. YouTube Shorts is competing effectively with TikTok. Advertising revenue from YouTube is recovering after the 2022 downturn.

### Valuation

At ~22x forward earnings, Alphabet trades at a discount to the S&P 500 on an ex-cash basis. For a company with Google Search, YouTube, Google Cloud, Waymo, and DeepMind under one roof, that discount is difficult to justify fundamentally.

**Disclosure:** This is not financial advice. Do your own research.
""",
    },
    {
        "title": "Amazon: AWS Reacceleration and the Retail Margin Expansion Story",
        "excerpt": "Amazon's AWS is back to 17%+ growth after its 2023 optimization headwinds. Meanwhile, the retail business is achieving margin levels that would have seemed impossible five years ago.",
        "tags": ["AMZN", "AWS", "cloud", "retail", "logistics"],
        "body": """## Amazon's Two-Engine Growth Machine

Amazon (NASDAQ: AMZN) is often misunderstood because investors try to value it as either a retailer or a cloud company. It's both — and the interplay between the two creates competitive advantages neither could achieve alone.

### AWS: The Margin Engine

AWS generates roughly **$100B in annualized revenue** and operates at ~38% operating margins. That means AWS alone generates more operating profit than most Fortune 100 companies make in total revenue.

After a challenging 2023 where enterprise customers optimized cloud spend, AWS has reaccelerated:

- **Q2 2024**: +19% YoY, up from 12% at the trough
- **Backlog**: $157 billion in committed future revenue
- **AI**: Bedrock (foundation model API), Trainium/Inferentia chips, and SageMaker are winning AI workloads

### The Retail Transformation

Amazon's retail business looked permanently margin-constrained until 2023. Then something changed: **advertising**.

Amazon's advertising business now generates **$50B+ annually** at high margins, effectively subsidizing the cost of fulfillment and making retail profitable for the first time.

| Segment | Revenue | Operating Income | Margin |
|---------|---------|-----------------|--------|
| AWS | $25B/Q | $9.3B/Q | 37% |
| Advertising | $12B/Q | ~$8B/Q | ~67% |
| North America Retail | $90B/Q | $5B/Q | 5.5% |
| International | $31B/Q | $1.3B/Q | 4% |

### Logistics: The Infrastructure Nobody Talks About

Amazon has built the world's most sophisticated consumer logistics network — 1,000+ fulfillment centers, a last-mile delivery fleet larger than UPS, and its own air cargo network. This infrastructure is now being offered to third parties through **Amazon Logistics Services**.

### The Thesis

Amazon is a toll road on e-commerce, cloud computing, digital advertising, and increasingly logistics. Each business reinforces the others. At ~35x forward earnings, it's not cheap — but the growth runway across all three segments is measured in decades.

**Disclosure:** This is not financial advice. Do your own research.
""",
    },
    {
        "title": "Meta: The Comeback Nobody Expected and the AI Infrastructure Bet",
        "excerpt": "Meta went from the 'year of efficiency' cost-cutting in 2023 to announcing $37B+ in capex for 2024. The advertising business is booming, but the AI spend is raising questions about returns.",
        "tags": ["META", "advertising", "AI", "social media", "Llama"],
        "body": """## Meta's Remarkable Reinvention

Two years ago, Meta Platforms (NASDAQ: META) was being written off. The metaverse pivot looked delusional, TikTok was eating Reels' lunch, and the iOS privacy changes had broken its core advertising model.

Then something remarkable happened: **Meta fixed it**.

### The Advertising Machine Rebuilt

Meta's engineering teams spent 18 months rebuilding their ad targeting infrastructure on top of AI models that don't rely on individual user tracking data. Instead of tracking *you*, Meta now predicts *who is likely to convert* based on aggregate patterns.

The results have been extraordinary:

| Quarter | Revenue | YoY Growth | Operating Margin |
|---------|---------|------------|-----------------|
| Q2 2023 | $32B | +11% | 29% |
| Q4 2023 | $40B | +25% | 41% |
| Q2 2024 | $39B | +22% | 38% |

Reels is now **fully monetized** at the same rate as Feed and Stories, eliminating a major drag that existed in 2022.

### The AI Infrastructure Question

Mark Zuckerberg has committed to spending **$37-40 billion in capex in 2024**, and suggesting 2025 will be even higher. This is funding:

- **Llama 3 and beyond**: Open-source models that are deployed across Meta's products and available for the world to use
- **GPU clusters**: Meta is building one of the largest AI compute clusters in the world
- **AI assistants**: Meta AI integrated across WhatsApp, Instagram, Facebook, and Messenger

The bear case is that this capex never generates adequate returns. The bull case is that Meta is building an AI-native advertising platform that will dominate digital marketing for the next decade.

### WhatsApp: The Undermonetized Giant

WhatsApp has **3 billion monthly active users** and generates almost no revenue today. Business messaging, WhatsApp Pay, and click-to-WhatsApp ads represent a massive untapped opportunity, particularly in emerging markets.

**Disclosure:** This is not financial advice. Do your own research.
""",
    },
    {
        "title": "Tesla: Beyond Cars — The Energy and AI Optionality Debate",
        "excerpt": "Tesla's automotive margins are under pressure from price cuts and competition. But the bull case increasingly rests on energy storage, Autopilot/FSD, and the Optimus robot — none of which are priced conventionally.",
        "tags": ["TSLA", "EV", "autonomous", "energy", "AI"],
        "body": """## Tesla's Identity Crisis — and Why It Matters for Valuation

Tesla (NASDAQ: TSLA) is the most polarizing stock in the Magnificent 7. At any given time, the bear case and the bull case seem to describe completely different companies.

### The Bear Case: Automotive Margin Collapse

| Quarter | Automotive Gross Margin | Change |
|---------|------------------------|--------|
| Q1 2023 | 19.3% | -400bps |
| Q3 2023 | 16.3% | -300bps |
| Q1 2024 | 16.4% | ~flat |
| Q2 2024 | 18.0% | +160bps |

Price cuts taken throughout 2023 to stimulate demand have structurally reset margins. Chinese competitors (BYD, Li Auto, NIO) have gotten good — fast. The legacy automakers have launched credible EVs. The market has gotten more competitive, not less.

### The Bull Case: This Isn't a Car Company

Elon Musk has been insistent: **Tesla should be valued on AI and robotics**, not automotive. The argument:

1. **Full Self-Driving (FSD)**: ~6 million Tesla vehicles on the road collecting real-world driving data. If FSD achieves Level 4/5 autonomy, each car could become a robotaxi — generating ride-sharing revenue rather than one-time sale revenue.

2. **Energy Storage**: Megapack (utility-scale battery storage) is a high-margin business growing 100%+ YoY. As renewable energy penetration increases, storage becomes critical infrastructure. This business alone could be worth $50B+.

3. **Optimus Robot**: Elon claims this is Tesla's most important product ever. Humanoid robots for manufacturing and eventually consumer use. Incredibly speculative, but if it works, the TAM is measured in trillions.

### The Valuation Problem

At ~60x forward earnings, Tesla is priced for perfection across multiple optionality bets simultaneously. If FSD doesn't achieve autonomy, if Energy doesn't scale, and if Optimus is vaporware, the stock is dramatically overvalued relative to its automotive business alone.

### The Key Question

Is Tesla a car company that happens to do AI, or an AI company that happens to make cars? Your answer determines whether the stock is cheap or expensive.

**Disclosure:** This is not financial advice. Do your own research.
""",
    },
]


class Command(BaseCommand):
    help = "Seed the blog with Magnificent 7 stock analysis posts"

    def handle(self, *args: object, **options: object) -> None:
        user, created = User.objects.get_or_create(
            email="analyst@blog.local",
            defaults={
                "username": "stockanalyst",
                "display_name": "Stock Analyst",
                "is_staff": False,
            },
        )
        if created:
            user.set_password("analyst123")
            user.save()
            self.stdout.write("Created user: stockanalyst")

        AuthorProfile.objects.get_or_create(
            user=user,
            defaults={
                "bio": "Independent equity analyst covering technology stocks and the AI megatrend. Not a financial advisor.",
                "twitter_handle": "stockanalyst",
                "location": "New York, NY",
                "is_verified": True,
            },
        )

        created_count = 0
        for i, post_data in enumerate(POSTS):
            if Post.all_objects.filter(title=post_data["title"]).exists():
                self.stdout.write(f"  Skipping (exists): {post_data['title'][:60]}")
                continue

            post = Post(
                author=user,
                title=post_data["title"],
                excerpt=post_data["excerpt"],
                body=post_data["body"],
                status=PostStatus.PUBLISHED,
                published_at=timezone.now(),
                is_featured=(i == 0),
                allow_comments=True,
            )
            post.save()
            post.tags.add(*post_data["tags"])
            created_count += 1
            self.stdout.write(f"  Created: {post.title[:60]}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. Created {created_count} posts."))
