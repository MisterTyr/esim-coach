# -*- coding: utf-8 -*-
"""Evergreen and legal page content for eSIM Coach.

Each entry: filename -> {title, desc, body}. The builder wraps every body in
the shared header/footer and prepends an <h1> from `title`, so bodies start
with the intro paragraph. Edit copy here; run build_static.py to regenerate.
"""

PAGES = {
    "what-is-esim.html": {
        "title": "What is an eSIM?",
        "desc": "A plain-English guide to eSIMs: what they are, how they differ from a physical SIM, and when to use one for travel.",
        "body": """
<p>An eSIM is a SIM card built into your phone. Instead of sliding a plastic card into a tray, you download a mobile plan straight to the device. The "e" stands for embedded. Most phones released since 2019 support it, including recent iPhones, Google Pixels and Samsung Galaxy models.</p>

<h2>How it differs from a physical SIM</h2>
<p>A physical SIM is a chip you swap by hand. An eSIM is a profile you install from a QR code or an app, usually in a couple of minutes. You can store several eSIM profiles at once and switch between them in settings, so your home number stays active while a travel plan handles data abroad.</p>

<h2>Why travellers use them</h2>
<p>You buy a local or regional data plan before you land, install it over Wi-Fi, and arrive with working data. No hunting for a SIM kiosk, no roaming charges, no swapping your home SIM out and losing your number. When the trip ends you delete the profile.</p>

<h2>What to check before buying</h2>
<p>Confirm three things: your phone is eSIM-capable, it is carrier-unlocked, and the plan covers the countries you're visiting. Data-only eSIMs (the most common travel type) give you internet but not a local phone number — fine for messaging apps, maps and calls over the internet.</p>

<p>Ready to compare? <a href="/">See today's best-value plans</a> or read the <a href="/how-to-install-esim.html">install guide</a>.</p>
"""
    },
    "how-to-install-esim.html": {
        "title": "How to install an eSIM",
        "desc": "Step-by-step: install and activate a travel eSIM on iPhone and Android in a few minutes.",
        "body": """
<p>Installing an eSIM takes about five minutes. Do it over Wi-Fi before you travel, then switch it on when you land. Here's the general flow, with the exact menu names for iPhone and Android.</p>

<h2>Before you start</h2>
<p>Check your phone supports eSIM and is unlocked. Buy your plan — the provider emails you a QR code or activates it inside their app. Keep that email or app handy.</p>

<h2>On iPhone</h2>
<p>Open Settings, then Cellular (or Mobile Data), then Add eSIM. Choose "Use QR Code" and scan the code from the provider, or tap "Enter Details Manually" and paste the activation info. Label the plan (e.g. "Travel"), then choose whether it handles your data. Turn on Data Roaming for the travel eSIM only — that's needed for it to connect abroad, and it won't cost extra because the plan is prepaid.</p>

<h2>On Android</h2>
<p>Open Settings, then Network &amp; internet, then tap the + next to SIMs (wording varies by brand). Choose to download a SIM, scan the QR code, and follow the prompts. Set the travel eSIM as your data SIM and enable roaming for it.</p>

<h2>When you land</h2>
<p>Set the travel eSIM as your active data line and leave your home SIM on for calls and texts if you want. If data doesn't start automatically, toggle Airplane mode off and on, or restart the phone. Most issues come from roaming being switched off for the travel line.</p>

<p>Not sure which plan to pick yet? <a href="/">Compare ranked plans by value</a>.</p>
"""
    },
    "why-esim.html": {
        "title": "Why use an eSIM for travel?",
        "desc": "The case for travel eSIMs: cost, convenience and coverage versus roaming and local SIM cards.",
        "body": """
<p>The pitch is simple: an eSIM usually beats both carrier roaming and buying a local SIM on arrival. Here's where each option lands.</p>

<h2>Versus carrier roaming</h2>
<p>Roaming from your home carrier is the most convenient and often the most expensive route. Daily roaming fees add up fast on a two-week trip. A prepaid travel eSIM is typically a fraction of the cost, and you know the price up front with no bill-shock.</p>

<h2>Versus a local SIM on arrival</h2>
<p>A local SIM can be cheap, but it means finding a shop, showing ID, swapping your card and losing your home number for the trip. An eSIM installs before you leave and keeps your home line active alongside it.</p>

<h2>Where eSIMs shine</h2>
<p>Short trips, multi-country routes and anyone who wants data working the moment they land. Regional plans (all of Europe or Asia on one eSIM) remove the hassle of buying a new plan at each border.</p>

<h2>The trade-offs</h2>
<p>Most travel eSIMs are data-only, so you won't get a local phone number. Coverage depends on which networks the provider partners with in each country. And you need an eSIM-capable, unlocked phone. For most travellers those are easy to live with.</p>

<p><a href="/">Browse today's best-value eSIM plans</a>, ranked by cost per GB.</p>
"""
    },
    "about.html": {
        "title": "About eSIM Coach",
        "desc": "What eSIM Coach does and how it ranks travel eSIM plans.",
        "body": """
<p>eSIM Coach helps travellers find a good-value data plan without wading through dozens of provider sites. We pull plan data, work out the real cost per gigabyte and per day, and rank what's actually good value.</p>

<h2>How ranking works</h2>
<p>For capped plans we sort by price per GB; for unlimited plans, by price per day. Longer validity breaks ties. We cap how many plans each provider can occupy so the list stays varied. The data refreshes daily.</p>

<h2>How we're funded</h2>
<p>Some outbound links are affiliate links, meaning we may earn a commission when you buy, at no extra cost to you. The ranking itself is value maths: price per GB, or price per day for unlimited plans. One exception. Honest Mobile pays for the top three slots on the homepage. Their plans are labelled "Paid placement" wherever they sit there, and the plan that wins on value keeps the "Top pick" badge regardless. See our <a href="/affiliate-disclosure.html">affiliate disclosure</a> for the detail.</p>

<h2>A note on accuracy</h2>
<p>Prices and plan terms change constantly. We do our best to keep the data fresh, but always confirm the final price and coverage on the provider's own site before buying.</p>
"""
    },
    "privacy-policy.html": {
        "title": "Privacy Policy",
        "desc": "How eSIM Coach handles data and privacy.",
        "body": """
<p>This policy explains what data eSIM Coach collects and how it's used. Last updated when this page was built.</p>

<h2>What we collect</h2>
<p>eSIM Coach is a static site. We don't ask you to create an account or submit personal details to browse. If we use privacy-friendly analytics, it records aggregate, non-identifying usage (pages viewed, country, device type) to help us improve the site.</p>

<h2>Cookies and affiliate links</h2>
<p>When you click an affiliate link, the destination provider may set a cookie to attribute a purchase to us. That's controlled by them, under their privacy policy, not ours.</p>

<h2>Email</h2>
<p>If you join our email list you provide your address voluntarily. We use it only to send the updates you signed up for, and you can unsubscribe at any time via the link in every email.</p>

<h2>Contact</h2>
<p>Questions about privacy? Reach us via the contact details on our <a href="/about.html">About page</a>.</p>
"""
    },
    "terms.html": {
        "title": "Terms of Use",
        "desc": "Terms governing use of eSIM Coach.",
        "body": """
<p>By using eSIM Coach you agree to these terms.</p>

<h2>Information only</h2>
<p>eSIM Coach provides comparison information for convenience. We are not a mobile carrier and do not sell eSIM plans directly. Purchases happen on third-party provider sites under their terms.</p>

<h2>No guarantee of accuracy</h2>
<p>We work to keep pricing and plan details current, but they change frequently and may be out of date or contain errors. Always confirm price, data allowance and coverage on the provider's site before buying. We are not liable for decisions made on the basis of information here.</p>

<h2>Affiliate relationships</h2>
<p>We earn commissions on some outbound links. This does not affect the price you pay or how we rank plans. See our <a href="/affiliate-disclosure.html">affiliate disclosure</a>.</p>

<h2>Changes</h2>
<p>We may update these terms at any time. Continued use of the site means you accept the current version.</p>
"""
    },
    "affiliate-disclosure.html": {
        "title": "Affiliate Disclosure",
        "desc": "How eSIM Coach uses affiliate links.",
        "body": """
<p>Honesty first: eSIM Coach earns money through affiliate links.</p>

<h2>What that means</h2>
<p>Some links to eSIM providers are affiliate links. If you click one and buy a plan, we may receive a commission. You pay exactly the same price — the provider funds the commission out of their margin, not by charging you more.</p>

<h2>How it affects rankings</h2>
<p>Partly, and here is exactly how. Plans are ranked by value, price per GB or price per day for unlimited, with a per-provider cap so one brand cannot fill the page. Having an affiliate programme does not move a plan up that list. Separately from the ranking, Honest Mobile pays us for the top three positions on the homepage. Their plans sit there because they paid, they are labelled "Paid placement", and the arrangement is open to any provider on the same terms. The "Top pick" badge is not for sale. It goes to whichever plan wins the value maths.</p>

<h2>Why we tell you</h2>
<p>Because it's the right thing to do, and because disclosure is required by advertising rules in most countries. If you'd rather not use our links, you can always go directly to any provider's site.</p>
"""
    },
}
