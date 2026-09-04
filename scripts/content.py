# -*- coding: utf-8 -*-
"""Evergreen and legal page content for eSIM Sorted.

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
        "title": "About eSIM Sorted",
        "desc": "What eSIM Sorted does and how it ranks travel eSIM plans.",
        "body": """
<p>eSIM Sorted helps travellers find a good-value data plan without wading through dozens of provider sites. We pull plan data, work out the real cost per gigabyte and per day, and rank what's actually good value.</p>

<h2>How ranking works</h2>
<p>For capped plans we sort by price per GB; for unlimited plans, by price per day. Longer validity breaks ties. We cap how many plans each provider can occupy so the list stays varied.</p>

<h2>How we're funded</h2>
<p>Some outbound links are affiliate links, meaning we may earn a commission when you buy, at no extra cost to you. The ranking itself is value maths: price per gigabyte of full-speed data, with plans that have no cap at all ranked separately on price per day. One exception. Honest Mobile pays for the top three slots on the homepage. Their plans are labelled "Paid placement" wherever they sit there, and the plan that wins on value keeps the "Top pick" badge regardless. See our <a href="/affiliate-disclosure.html">affiliate disclosure</a> for the detail.</p>

<h2>A note on accuracy</h2>
<p>Prices and plan terms change constantly. We do our best to keep the data fresh, but always confirm the final price and coverage on the provider's own site before buying.</p>
"""
    },
    "privacy-policy.html": {
        "title": "Privacy Policy",
        "desc": "How eSIM Sorted handles data and privacy.",
        "body": """
<p>This policy explains what data eSIM Sorted collects and how it's used. Last updated when this page was built.</p>

<h2>What we collect</h2>
<p>eSIM Sorted is a static site. We don't ask you to create an account or submit personal details to browse. If we use privacy-friendly analytics, it records aggregate, non-identifying usage (pages viewed, country, device type) to help us improve the site.</p>

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
        "desc": "Terms governing use of eSIM Sorted.",
        "body": """
<p>By using eSIM Sorted you agree to these terms.</p>

<h2>Information only</h2>
<p>eSIM Sorted provides comparison information for convenience. We are not a mobile carrier and do not sell eSIM plans directly. Purchases happen on third-party provider sites under their terms.</p>

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
        "desc": "How eSIM Sorted uses affiliate links.",
        "body": """
<p>Honesty first: eSIM Sorted earns money through affiliate links.</p>

<h2>What that means</h2>
<p>Some links to eSIM providers are affiliate links. If you click one and buy a plan, we may receive a commission. You pay exactly the same price — the provider funds the commission out of their margin, not by charging you more.</p>

<h2>How it affects rankings</h2>
<p>Partly, and here is exactly how. Plans are ranked on what a pound actually buys: price per gigabyte of full-speed data, with a per-provider cap so one brand cannot fill the page. A plan sold as unlimited but capped at, say, 3GB a day is scored on that allowance rather than on its headline. A plan with no cap at all cannot be compared that way, so it sits below the sized plans and is ranked on price per day. Having an affiliate programme does not move a plan up that list. Separately from the ranking, Honest Mobile pays us for the top three positions on the homepage. Their plans sit there because they paid, and they are labelled "Paid placement". The "Top pick" badge is not for sale. It goes to whichever plan wins the value maths.</p>

<h2>Why we tell you</h2>
<p>Because it's the right thing to do, and because disclosure is required by advertising rules in most countries. If you'd rather not use our links, you can always go directly to any provider's site.</p>
"""
    },
}


# --- Destination guides, added 4 September 2026 -------------------------------
# Deliberately light on prices. Prices go stale and this site has already been
# burned by claims that stopped being true; the live table on the homepage is
# the place for numbers. What goes here is how the products differ, which
# changes slowly. Any price quoted carries the date it was checked.

PAGES.update({
    "esim-japan.html": {
        "title": "The best eSIM for Japan",
        "desc": "How to pick a travel eSIM for Japan: what the unlimited plans actually give you, why data-only matters, and what to check before you buy.",
        "body": """
<p>Japan is one of the easiest places in the world to use a travel eSIM. Coverage is excellent almost everywhere a visitor goes, including the shinkansen and most of the metro network, and every major provider sells a Japan plan. The choice is not about coverage. It is about what "unlimited" means, and whether you need to make phone calls.</p>

<h2>Unlimited in Japan usually means a daily allowance</h2>
<p>Nearly every provider selling an "unlimited" Japan eSIM caps your full-speed data per day and then slows you down until midnight. The allowances differ by more than most people realise:</p>
<ul>
<li><strong>Airalo</strong> gives 3GB a day, then 1Mbps.</li>
<li><strong>Saily</strong> gives 5GB a day, then 1Mbps.</li>
<li><strong>Nomad</strong> gives 2GB a day, then 512kbps.</li>
<li><strong>Ubigi</strong> works differently again: it caps the whole plan rather than the day, and its Japan plans do not all use the same figure.</li>
<li><strong>Holafly</strong> publishes no figure at all. Their terms say only that speed may be subject to a fair use policy.</li>
</ul>
<p>A 3GB daily allowance is a lot for maps, messaging and a few hours of scrolling. It is not a lot if you are working from a laptop or streaming. And 1Mbps still loads maps and WhatsApp, so a throttled plan is far from useless, but it will not stream video.</p>
<p>This is why the table on this site scores a capped plan on what it actually gives you at full speed rather than on price per day. A 30-day plan with a 3GB daily cap is a 90GB plan, and it should be compared with one.</p>

<h2>Travel eSIMs in Japan do not make phone calls</h2>
<p>Almost every travel eSIM sold for Japan is data-only. You get internet, so WhatsApp, FaceTime, Signal and Google Voice all work, but you have no Japanese number and you cannot dial an ordinary phone number.</p>
<p>That matters more in Japan than in most places, because restaurant bookings, ryokan check-ins and taxi firms still expect a phone call, and some booking sites will not accept a foreign mobile number. If you know you need to ring people, either keep your home SIM active for outgoing calls or look at a plan that includes real cellular voice.</p>

<h2>What to check before you buy</h2>
<ul>
<li><strong>Tethering.</strong> If you are travelling with a laptop or sharing with someone, check the plan allows hotspot use and whether it is capped. Some providers limit sharing to a small daily amount even on an unlimited plan.</li>
<li><strong>Which network it uses.</strong> Japan's networks are NTT Docomo, SoftBank, KDDI au and Rakuten. Coverage differences barely matter in cities and can matter in the mountains.</li>
<li><strong>Install before you fly.</strong> Install the profile at home over Wi-Fi. Most plans start counting when the eSIM first connects to a network in Japan, not when you install it, but check that on the provider's page rather than assuming.</li>
</ul>

<p><a href="/">Compare the current Japan plans</a>, or read the <a href="/how-to-install-esim.html">install guide</a> first.</p>
"""
    },
    "esim-europe.html": {
        "title": "The best eSIM for Europe",
        "desc": "Travel eSIMs for Europe compared with UK pay-as-you-go roaming, and why the cheapest answer for a UK traveller is often not a travel eSIM at all.",
        "body": """
<p>Europe is the one destination where a UK traveller should stop and ask whether they need a travel eSIM at all. For most other places the answer is obvious. For a week in Spain it very often is not.</p>

<h2>Check your own contract first</h2>
<p>Plenty of UK mobile plans still include EU roaming at no extra cost, and several UK pay-as-you-go packs include a chunk of roaming data across a long list of destinations. Three's pay-as-you-go range, for instance, includes roaming across more than 70 destinations with your UK calls and texts, though the roaming data allowance is much smaller than the UK one, so read that number rather than the headline.</p>
<p>If your existing plan covers you, a travel eSIM is a second thing to manage for no gain. Check before you buy anything.</p>

<h2>When a travel eSIM does win</h2>
<p>Three situations:</p>
<ul>
<li>Your plan charges for EU roaming, which many post-2021 UK contracts do.</li>
<li>Your roaming allowance is small and you will burn through it. A few gigabytes disappears fast on maps and photo uploads.</li>
<li>You are going somewhere outside the usual roaming zone. Turkey, Switzerland and the Balkans are frequently excluded from UK roaming deals and are covered by most regional Europe eSIMs.</li>
</ul>

<h2>The unlimited plans are capped, and the caps differ</h2>
<p>As everywhere, "unlimited" in Europe usually means a full-speed allowance and then a slowdown. Airalo gives 3GB a day before dropping to 1Mbps. Saily's Europe plan gives 3GB a day, which is less than the 5GB it gives on several single-country plans. Ubigi caps the whole plan instead, at 25GB over seven days. Holafly does not publish a figure.</p>
<p>Regional plans also differ on which countries they cover. A "Europe" plan is typically 30 to 40 countries, and the borderline ones are the ones you need to check: Switzerland, Turkey, Ukraine, the Balkan states and the Channel Islands are all commonly in one provider's list and not another's.</p>

<h2>Calls and a real number</h2>
<p>Most travel eSIMs for Europe are data-only. The exception worth knowing about is Orange, whose European travel plans include real cellular calls and texts along with a European phone number, rather than only internet calling. If you need to ring a hotel or a hire car desk, that is a different product from a data eSIM, and it is priced accordingly.</p>

<p><a href="/">Compare the current Europe plans</a>.</p>
"""
    },
    "esim-usa.html": {
        "title": "The best eSIM for the USA",
        "desc": "How to choose a travel eSIM for the United States, including why a US phone number is harder to get than you would expect.",
        "body": """
<p>The United States has the widest gap between what a travel eSIM costs and what your own network charges to roam. UK roaming rates for the US are usually painful, and a travel eSIM is almost always the cheaper answer. The question is which one.</p>

<h2>Coverage is about which network you land on</h2>
<p>American coverage is a network question rather than a provider question. The three networks are AT&amp;T, T-Mobile and Verizon, and every travel eSIM sold for the US rides on one or more of them. Coverage is good in cities on all three. It diverges in rural areas, on long drives and in the national parks, which is exactly where you are most likely to need it.</p>
<p>If your trip is a road trip, check which network the plan uses before you buy rather than comparing headline prices. If your trip is New York and Chicago, it barely matters.</p>

<h2>Unlimited, again, is a daily allowance</h2>
<p>Airalo's US plans are unlimited-only now, with 3GB a day at full speed and 1Mbps after that, and tethering is not restricted. Saily gives 5GB a day. Ubigi caps the plan rather than the day. The pattern is the same as everywhere else, and the differences are large enough to change which plan is actually the best value once you account for them.</p>

<h2>Getting a US phone number is the hard part</h2>
<p>Most travel eSIMs give you data and nothing else. That is usually fine, but the US is one place where it bites: some restaurant bookings, ride-hailing verifications, delivery services and hotel systems want to send you a text, and a UK number roaming can receive those while a data-only eSIM cannot.</p>
<p>There are three ways round it. Keep your home SIM switched on for texts and use the eSIM for data, which is what most people do. Buy a plan that includes a US number, which a small number of providers offer, sometimes as a paid add-on. Or use an internet calling app with a US number, which works for most services but is rejected by some as a virtual number.</p>

<h2>One thing to check</h2>
<p>Confirm your phone supports the right bands and that the plan covers 5G if you care about it. An older handset bought outside the US can end up on slower networks even where the plan itself is fine.</p>

<p><a href="/">Compare the current USA plans</a>.</p>
"""
    },
    "esim-thailand.html": {
        "title": "The best eSIM for Thailand",
        "desc": "Choosing a travel eSIM for Thailand: what the plans cost, what unlimited really gives you, and what to know about island coverage.",
        "body": """
<p>Thailand is the cheapest of the popular long-haul destinations for travel data, by a clear margin. The same providers that charge £50 or more for a month in Japan or the US will do Thailand for a good deal less, because local wholesale data is cheap and competition is fierce.</p>

<h2>It is cheap, so buy for the trip rather than the week</h2>
<p>Because the prices are low, the usual advice to buy the smallest plan that will do is weaker here. The step up from a short plan to a month is often small enough that it is not worth the risk of running out halfway through. Airalo's 30-day unlimited Thailand plan was £37.50 when we checked it on 4 September 2026, against £16 for seven days, so a three-week trip costs barely more than two one-week plans.</p>
<p>Prices move, so treat that as an illustration and check the live table.</p>

<h2>Coverage: the mainland is easy, the islands less so</h2>
<p>Bangkok, Chiang Mai and the main tourist routes have excellent coverage on all three Thai networks, AIS, TrueMove and dtac. The gaps show up on the smaller islands, on boats between them, and in the national parks. If your trip is island-heavy, that is a reason to prefer a provider that uses AIS, which generally has the widest rural and island reach, though no travel eSIM company guarantees which network you land on.</p>

<h2>Unlimited plans and the daily cap</h2>
<p>The same pattern as everywhere: an unlimited Thailand plan almost always means a full-speed daily allowance and then a slowdown. Airalo gives 3GB a day then 1Mbps, Saily gives 5GB a day, Nomad gives 2GB a day then 512kbps. For a beach holiday, any of those is more than enough. For working remotely, the difference between 2GB and 5GB a day is the whole decision.</p>

<h2>Worth knowing</h2>
<ul>
<li><strong>Most Thailand travel eSIMs are data-only</strong>, so you will have no Thai number. Grab, Foodpanda and most booking apps work fine on a foreign number, but a few local services will want a Thai one.</li>
<li><strong>Buying locally is genuinely competitive here.</strong> Tourist SIMs sold at Suvarnabhumi and Don Mueang airports are cheap. An eSIM wins on convenience and on landing with data already working, not always on price.</li>
<li><strong>Install before you fly.</strong> Airport Wi-Fi in Bangkok is fine but the queue at the SIM counter is not.</li>
</ul>

<p><a href="/">Compare the current Thailand plans</a>.</p>
"""
    },
})
