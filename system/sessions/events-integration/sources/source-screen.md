# Ocharo unranked source screen (SR02)

*Screened and probed 2026-11-21 by lane `src-probe` for [`ocharo-sources-plan.md`](ocharo-sources-plan.md) task SR02. Input: the 277 unranked host buckets under `archive.unranked_source_buckets` of the read-only source archive (378 URLs); hosts compared with the registry's 108 hosts; nothing from the archive is copied beyond hosts and public URLs, tracking query strings stripped.*

- Date: 2026-11-21
- User-Agent: `Harvest/0.1 (SCFD source probe)`
- Pacing: one request every 2.1 s overall, one connection at a time, 15 s timeout, no cookies, login, proxy or retries; `robots.txt` read once per host and obeyed for `Harvest` and `*` (no host has a `Harvest` group); one GET of the page, redirects followed only within the same site (at most 3 hops, each paced); a 403, 429 or 503, a challenge or a failed connection ended a host. 71 requests in all. No registry host was fetched.
- Counts: 277 buckets, 32 `keep` and 245 `drop`. Keeps by route: generic-site 12, manual 8, generic-feed 7, cannot 5. Keeps by country: UZ 12, KZ 7, RU 7, KG 2, TJ 2, AZ 1, multi 1.
- Hosts that challenged: `namangan-tourism.uz` answered 503 (a plain nginx Service Unavailable page, possibly an outage). No 403, 429 or interstitial page appeared.

How the screen ran:

- `drop` from the URL alone: forms, PDFs and shared files, chat and short links, single news articles, past-edition and single-edition pages, standards and reference pages, social posts, mirrors of Telegram and Instagram, foreign sites outside the Central Asia and CIS footprint, and hosts the registry holds (reason `in registry`, parent hosts included). A root-only URL whose purpose the URL does not show is dropped with that reason.
- `keep`: a host that publishes events, fairs, fashion, design, craft, culture listings or ticketing on a recurring basis, or a recurring fashion or design event brand with its own editions and news.
- Four hosts were kept from the URL and dropped once the probe showed what they are; they count as `drop` below and have no Table B row: `banksy.uz` (finance news), `ticket.uz` (business-travel agency), `showpro.uz` (a Yamaha audio shop whose blog is product news; the plan named it as an example, so the orchestrator may overrule), `yunusobod.tashkent.uz` (serves the `tashkent.uz` portal, whose host the registry holds).
- `t.me` is a registry host, so the brief bars fetching it: the two Telegram keeps carry route `manual` and were not fetched.
- A bucket is one archive key: several buckets share a host (`forms.gle`, `gov.uz`, `t.me`, `telemetr.io`), so Table A has one row per bucket; the 277 buckets hold 248 distinct hosts after the `www.` prefix is dropped.
- Probed pages are home pages or the archive's listing page. No probed page carried JSON-LD `Event`, so no keep routes `generic-structured`; event detail pages were not probed, so a read of those may still find it.
- `generic-feed` rows are marked unverified: the feed URL was read from an alternate link and not fetched.


## Table A: 277 host buckets

| Host | URLs in bucket | Verdict | Reason |
|---|---|---|---|
| 24.kg | 1 | drop | single news article |
| 4textile.com | 1 | drop | trade-fair portal, single fair page |
| 98mag.kz | 1 | keep | Kazakh fashion and lifestyle magazine |
| affta.ab.ca | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| aitshoes.kz | 1 | drop | single news article |
| anhor.uz | 1 | keep | independent news site with a culture section |
| api-portal.gov.uz | 1 | drop | PDF or document download |
| api-portal.gov.uz | 1 | drop | PDF or document download |
| api-portal.gov.uz | 1 | drop | PDF or document download |
| app.entrythingy.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| app.panneaupocket.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| app.uzbekistan.travel | 1 | drop | in registry (parent host) |
| art-blog.uz | 1 | keep | art and culture blog, recurring posts |
| artdom-design.ru | 3 | drop | single-edition event page |
| arthead.world | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| asianculturalcouncil.org | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| asiaplus.news | 1 | drop | general newsroom, not events-led |
| atr.one | 1 | drop | root URL only, purpose not evident from the URL |
| austapestry.com.au | 2 | drop | foreign site outside the Central Asia and CIS footprint |
| b2match.com | 3 | drop | form or registration page |
| banksy.uz | 1 | drop | probe: finance news site; the design-week article was a one-off |
| bbstravel.uz | 1 | drop | single news article |
| bee-lifestyle.ru | 1 | drop | root URL only, purpose not evident from the URL |
| bestfares.airastana.com | 1 | drop | travel or ticket-sales page, not events |
| bigasia.ru | 1 | drop | single news article |
| bishkekft.com | 1 | keep | recurring Bishkek fashion and textile fair |
| bookind.ru | 1 | drop | single news article |
| booking.com | 1 | drop | travel or ticket-sales page, not events |
| burg-halle.de | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| businessmir.kz | 1 | drop | single article on a business newsroom |
| buxoro-yoshlari.uz | 1 | drop | PDF or document download |
| cahp.uz | 1 | drop | root URL only, purpose not evident from the URL |
| catalog.texworld.uz | 1 | drop | in registry (parent host) |
| cca.uz | 1 | drop | single press release |
| ccaforum.uz | 1 | drop | single delegate profile page on a forum site |
| chatcrawler.link | 1 | drop | third-party mirror of Telegram channels |
| cis-fashion.ru | 3 | keep | recurring fashion trade show with news |
| cis.visa.com | 2 | drop | corporate promo page |
| clck.ru | 1 | drop | link shortener |
| clck.ru | 1 | drop | link shortener |
| clck.ru | 1 | drop | link shortener |
| confartigianatolecce.it | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| core.telegram.org | 2 | drop | reference or standards page |
| cortexfrontal.org | 6 | drop | form or registration page |
| cpm-moscow.com | 2 | keep | recurring fashion trade fair with press releases |
| craftprize.loewe.com | 3 | drop | foreign site outside the Central Asia and CIS footprint |
| craftwork4all.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| denim.premierevision.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| designoutlook.ru | 2 | keep | annual young-designers contest site with news and a sitemap |
| developers.cloudflare.com | 2 | drop | reference or standards page |
| developers.google.com | 3 | drop | reference or standards page |
| digital.gov.uz | 1 | drop | in registry (gov.uz) |
| digitalbusiness.kz | 1 | drop | single article on a business newsroom |
| disk.360.yandex.ru | 1 | drop | shared file |
| disk.yandex.ru | 2 | drop | shared file |
| dmibf.ru | 1 | drop | root URL only, purpose not evident from the URL |
| docs.google.com | 1 | drop | form |
| doodles.google | 1 | drop | reference or standards page |
| drive.google.com | 1 | drop | shared file or folder |
| e-flux.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| earthpartner.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| echipta.tj | 1 | keep | Tajik e-ticketing with event listings |
| eco.gov.uz | 1 | drop | PDF or document download |
| economycreativedays.ru | 1 | drop | single-edition event page |
| egov.kz | 1 | drop | reference or standards page |
| elenamilberger.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| elle.com.kz | 1 | keep | fashion magazine, Kazakhstan edition |
| emkp.flexigrant.com | 1 | drop | form or registration page |
| en.antaranews.com | 1 | drop | single news article |
| en.genomics.uz | 1 | drop | single news article |
| en.jufair.com | 3 | drop | trade-fair portal, single fair page |
| eng.khovar.tj | 1 | drop | single news article |
| esquire.kz | 1 | keep | lifestyle and fashion magazine, recurring |
| eurasianstar.com | 1 | drop | single news article |
| euronews.com | 2 | drop | single news article |
| eventseye.com | 2 | keep | trade-show directory with country and topic listings |
| expoassist.net | 1 | drop | third-party listing of a registry venue |
| expobeds.com | 1 | drop | trade-fair portal, single fair page |
| expoclub.ru | 1 | drop | trade-fair portal, single fair page |
| expodat.uz | 1 | drop | registration form |
| expomap.ru | 1 | drop | trade-fair portal, single fair page |
| exponet.ru | 4 | keep | fair directory with fashion and country listings |
| fibre2fashion.com | 1 | drop | trade-fair portal, single fair page |
| folkartmarket.org | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| forms.gle | 1 | drop | form |
| forms.gle | 1 | drop | form |
| forms.gle | 1 | drop | form |
| forms.gle | 1 | drop | form |
| forms.gle | 1 | drop | form |
| forms.gle | 1 | drop | form |
| forms.gle | 1 | drop | form |
| forms.monday.com | 1 | drop | form or registration page |
| forms.yandex.ru | 2 | drop | form or registration page |
| ftp.yuz.uz | 1 | drop | in registry (parent host) |
| ghpa.ru | 1 | drop | single contest or announcement site |
| go-go.uz | 1 | drop | root URL only, purpose not evident from the URL |
| go.palmbeachculture.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| gov.uz | 1 | drop | in registry (gov.uz) |
| gov.uz | 2 | drop | in registry (gov.uz) |
| gov.uz | 1 | drop | in registry (gov.uz) |
| gov.uz | 1 | drop | in registry (gov.uz) |
| gov.uz | 1 | drop | in registry (gov.uz) |
| gtdib.org | 3 | drop | about and contacts pages only |
| hometex-deco.kz | 2 | drop | fair site off the fashion and culture focus |
| html.spec.whatwg.org | 1 | drop | reference or standards page |
| iacis.ru | 1 | drop | form or registration page |
| iana.org | 1 | drop | reference or standards page |
| icac.org | 1 | drop | single news article |
| ich.unesco.org | 3 | drop | in registry (parent host) |
| ied.edu | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| ifas.com.tr | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| ifco.com.tr | 3 | drop | foreign site outside the Central Asia and CIS footprint |
| ihkib.org.tr | 1 | drop | PDF or document download |
| imginn.com | 1 | drop | third-party mirror of Instagram posts |
| imginn.com | 1 | drop | third-party mirror of Instagram posts |
| in2motionfest.com | 3 | drop | single-edition event page |
| inbusiness.kz | 1 | drop | single article on a business newsroom |
| instagram.com | 1 | drop | social-network post |
| internationalapparelandtextilefair.com | 2 | drop | single-edition event page |
| intertexmilano.com | 4 | drop | foreign site outside the Central Asia and CIS footprint |
| italianfairservice.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| jewelryfair.uz | 1 | keep | recurring jewelry fair, edition and exhibitor pages |
| kaktus.media | 1 | drop | single article on a general newsroom |
| kassir.kg | 1 | keep | ticketing platform |
| kassir.kz | 1 | keep | ticketing platform |
| kemlu.go.id | 1 | drop | PDF or document download |
| kidsworldca.uz | 1 | drop | fair site off the fashion and culture focus |
| kktd.ru | 2 | drop | single contest or announcement site |
| knuh.ac.kr | 1 | drop | PDF or document download |
| kuenstlerbund.org | 4 | drop | foreign site outside the Central Asia and CIS footprint |
| kultura55.ru | 2 | drop | single news article |
| kun.uz | 1 | drop | single news article |
| lachapellebouexic.fr | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| landingaflive.artigianoinfiera.it | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| lifex.az | 3 | drop | single-edition event page |
| lift-bf.ru | 1 | drop | single-edition event page |
| linkedin.com | 5 | drop | social-network post or profile |
| loewecraftprize.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| luminik.io | 1 | drop | third-party listing of a registry venue |
| maison-objet.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| mantilityresidency.com | 2 | drop | foreign site outside the Central Asia and CIS footprint |
| mdis.uz | 1 | drop | institution page or blog, not events-led |
| mfa.tj | 1 | drop | single news article |
| mffrussia.com | 1 | keep | Moscow fashion festival site |
| mibf.info | 1 | drop | single news article |
| moscowfashion.ru | 1 | keep | Moscow fashion week site |
| msfd.ru | 1 | drop | root URL only, purpose not evident from the URL |
| mus38.ru | 1 | drop | single news article |
| myticket.uz | 1 | keep | ticketing site |
| namangan-tourism.uz | 1 | keep | regional tourism board with a festivals section |
| nampravda.uz | 1 | drop | single news article |
| naqshschoolofcrafts.uz | 1 | drop | institution page or blog, not events-led |
| news-kherson.ru | 1 | drop | single news article |
| newscentralasia.net | 1 | drop | single news article |
| note.com | 1 | drop | social-network post or profile |
| np.admin.appstrakt.world | 1 | drop | PDF or document download |
| oecongroup.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| old.muctr.uz | 1 | drop | single news article |
| old.quva.uz | 1 | drop | single news article |
| om.tomskvoi.ru | 1 | drop | root URL only, purpose not evident from the URL |
| omgtu.ru | 1 | drop | single news article |
| omskartresidence.ru | 1 | drop | single-edition event page |
| paris.premierevision.com | 4 | drop | foreign site outside the Central Asia and CIS footprint |
| pixnoy.com | 1 | drop | social-network post or profile |
| podium.uz | 1 | keep | shopping-mall site with recurring fashion shows |
| polotnokongress.tilda.ws | 1 | drop | single contest or announcement site |
| portalbilet.uz | 1 | keep | ticketing site |
| premierevision.com | 2 | drop | foreign site outside the Central Asia and CIS footprint |
| president.uz | 2 | drop | single article on a general newsroom |
| press.natlib.uz | 1 | drop | PDF or document download |
| proart.uz | 1 | keep | event agency (concerts, festivals, exhibitions) with a news feed |
| prodvigenie.net | 6 | drop | single-edition event page |
| pyramidsfair.com | 1 | drop | trade-fair portal, single fair page |
| qazaqculture.com | 1 | drop | single news article |
| redbull.com | 1 | drop | single news article |
| register.internationalapparelandtextilefair.com | 1 | drop | form or registration page |
| repost.uz | 1 | drop | single event page on a minor media site |
| rfc-editor.org | 3 | drop | reference or standards page |
| riamoda.ru | 1 | keep | fashion news agency, recurring |
| ru.kabar.kg | 1 | drop | in registry (parent host) |
| ru.linkedin.com | 1 | drop | social-network post or profile |
| sanat.orexca.com | 1 | drop | single news article |
| showpro.uz | 1 | drop | probe: Yamaha audio shop; the blog is product news, not events |
| showsbee.com | 4 | drop | trade-fair portal, single fair page |
| sibiz.eu | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| site.picter.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| siximuseum.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| smartwearrevolution.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| sof-expo.com | 2 | drop | fair site off the fashion and culture focus |
| souvenirexpoturkiye.com.tr | 3 | drop | foreign site outside the Central Asia and CIS footprint |
| sport24.ru | 1 | drop | single news article |
| storage.academy.uz | 1 | drop | PDF or document download |
| strazy-solea.ru | 1 | drop | single-edition event page |
| stv.uz | 1 | drop | single news article |
| styleofeurasia.com | 1 | keep | Eurasian style and fashion media, recurring |
| sublimation.uz | 1 | drop | commercial company site, not events |
| sxodim.uz | 1 | keep | Uzbek edition of the Sxodim guide; registry holds only sxodim.com |
| t.me/aydatuda | 1 | keep | recurring Telegram events channel |
| t.me | 2 | drop | Telegram channel not event-led, bot or embassy |
| t.me | 1 | drop | Telegram channel not event-led, bot or embassy |
| t.me | 1 | drop | Telegram channel not event-led, bot or embassy |
| t.me | 1 | drop | Telegram channel not event-led, bot or embassy |
| t.me | 1 | drop | Telegram channel not event-led, bot or embassy |
| t.me | 1 | drop | Telegram channel not event-led, bot or embassy |
| tada-residency.ch | 2 | drop | foreign site outside the Central Asia and CIS footprint |
| tashkentdesignweek.uz | 1 | keep | annual design week site with programme and news |
| tatlerasia.kz | 1 | keep | fashion and society magazine, Kazakhstan edition |
| telegram.me | 2 | keep | recurring Telegram art channel (proartworld); the bukhtourism handle in the same bucket is in registry |
| telemetr.io | 1 | drop | third-party mirror of Telegram channels |
| telemetr.io | 1 | drop | third-party mirror of Telegram channels |
| telemetr.io | 1 | drop | third-party mirror of Telegram channels |
| telemetr.io | 1 | drop | third-party mirror of Telegram channels |
| telemetr.io | 1 | drop | third-party mirror of Telegram channels |
| telemetr.io | 1 | drop | third-party mirror of Telegram channels |
| telemetr.io | 1 | drop | third-party mirror of Telegram channels |
| telemetr.me | 3 | drop | third-party mirror of Telegram channels |
| tersu.uz | 1 | drop | single news article |
| test.lex.uz | 2 | drop | in registry (parent host) |
| texhibitionist.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| textiellab.nl | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| tft.expocentr.ru | 1 | drop | form or registration page |
| tginsider.app | 1 | drop | third-party mirror of Telegram channels |
| the-steppe.com | 1 | drop | single article on a general newsroom |
| ticket.uz | 1 | drop | probe: business-travel agency, not event ticketing |
| ticketon.tj | 1 | keep | ticketing site; Ticketon is in the registry on .kz and .uz only |
| tomskvoi.ru | 1 | drop | PDF or document download |
| tourismboard.az | 1 | keep | tourism board events calendar |
| tpp.tj | 2 | drop | chamber of commerce site, business events only |
| trade.gov | 1 | drop | reference or standards page |
| tradeindia.com | 1 | drop | trade-fair portal, single fair page |
| tranoi.com | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| trans.uz | 1 | drop | about and contacts pages only |
| trend.az | 1 | drop | single news article |
| tripadvisor.com | 1 | drop | social-network post or profile |
| u-enter.uz | 3 | drop | institution page or blog, not events-led |
| uedpescara.it | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| uk.tmembassy.gov.tm | 1 | drop | single news article |
| unesco.se | 1 | drop | PDF or document download |
| unevoc.unesco.org | 1 | drop | in registry (parent host) |
| uniticket.uz | 1 | drop | travel or ticket-sales page, not events |
| uz.osiyoramzi.uz | 1 | drop | in registry (parent host) |
| uzairways.com | 2 | drop | PDF or document download |
| uzbekheritage.org | 1 | drop | root URL only, purpose not evident from the URL |
| uzconsulrnd.ru | 1 | drop | consulate site |
| uzdaily.ru | 1 | drop | single news article |
| uzlidep.uz | 1 | drop | off-topic site (party or finance) |
| uznews.uz | 1 | drop | general newsroom, not events-led |
| uzreport.news | 1 | drop | single article on a general newsroom |
| vallonsenbretagne.fr | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| vam.ac.uk | 6 | drop | foreign site outside the Central Asia and CIS footprint |
| vatupdate.com | 2 | drop | single article on a business newsroom |
| visa.com.kz | 2 | drop | corporate promo page |
| vm.ee | 1 | drop | single news article |
| vogueadria.com | 1 | drop | single news article |
| vostockcapital.ru | 1 | drop | off-topic site (party or finance) |
| vostockcapital.zoom.us | 1 | drop | form or registration page |
| w3.org | 3 | drop | reference or standards page |
| wa.me | 1 | drop | chat link |
| wa.me | 1 | drop | chat link |
| wam.ae | 1 | drop | single news article |
| warsawexpo.eu | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| warsawhometextile.com | 2 | drop | foreign site outside the Central Asia and CIS footprint |
| wccapr.org | 1 | drop | PDF or document download |
| wcoomd.org | 1 | drop | single news article |
| weproject.media | 2 | keep | Almaty events guide and fashion news, recurring |
| womanmade.org | 1 | drop | foreign site outside the Central Asia and CIS footprint |
| worldcottonday.com | 1 | drop | single-edition event page |
| wsn-events.com | 2 | drop | foreign site outside the Central Asia and CIS footprint |
| xn--j1aaidmgm0e.xn--p1ai | 1 | drop | single contest or announcement site |
| yiltanlovi.uz | 5 | drop | single contest or announcement site |
| your.tj | 1 | drop | single news article |
| youtube.com | 1 | drop | video |
| youtube.com | 1 | drop | video |
| yunusobod.tashkent.uz | 1 | drop | probe: serves the tashkent.uz portal, robots Sitemap points at tashkent.uz (in registry) |
| yunusobodtumani.uz | 1 | drop | single news article |
| zakon.kz | 2 | drop | single article on a general newsroom |
| zayedfestival.ae | 1 | drop | foreign site outside the Central Asia and CIS footprint |

## Table B: probe row per keep

| Host | Probed URL | Route | Feed or sitemap URL | Robots | HTTP status | Probed on | Proposed group id | Tier | Country | Note |
|---|---|---|---|---|---|---|---|---|---|---|
| podium.uz | https://podium.uz/ | generic-site | https://podium.uz/sitemap.xml | allowed | 200 | 2026-11-21 | podium-uz | P3 | UZ | Shopping-mall site with fashion shows; DDoS-Guard in front, page complete; no feed or JSON-LD Event; probed the home page, the archive URL was an edition page |
| tashkentdesignweek.uz | https://www.tashkentdesignweek.uz/ | generic-site | https://www.tashkentdesignweek.uz/sitemap.xml | allowed | 200 | 2026-11-21 | tashkentdesignweek-uz | P2 | UZ | Wix site for Tashkent Design Week 26 Oct-1 Nov 2026; same event as registry group tashkent-design-week (designweek.uz), so SR17 may add it as a channel there; JSON-LD has WebSite and LocalBusiness only |
| jewelryfair.uz | https://jewelryfair.uz/en/ | generic-feed | https://jewelryfair.uz/en/feed/ (unverified) | allowed | 200 | 2026-11-21 | jewelry-fair | P3 | UZ | Global Jewelry Fair 2026 site on WordPress; /en/feed/ is the posts feed, robots also lists wp-sitemap.xml |
| anhor.uz | https://anhor.uz/ | generic-site | https://anhor.uz/sitemap-index.xml | allowed | 200 | 2026-11-21 | anhor | P3 | UZ | News site with a culture section; the probe followed a 307 to /uzl; the culture section URL was not guessed and needs picking; robots also lists a news sitemap https://anhor.uz/api/sitemap-news |
| art-blog.uz | https://art-blog.uz/ | generic-feed | https://art-blog.uz/feed (unverified) | allowed | 200 | 2026-11-21 | art-blog-uz | P3 | UZ | Art blog on WordPress; robots has no Sitemap line |
| myticket.uz | https://myticket.uz/ | generic-site | https://myticket.uz/sitemap.xml | allowed | 200 | 2026-11-21 | myticket | P3 | UZ | Ticketing site; home page JSON-LD is WebSite and SearchAction only, no Event; event pages not probed |
| portalbilet.uz | https://portalbilet.uz/ru | cannot | - | not read (no response) | - | 2026-11-21 | portalbilet | P3 | UZ | cannot: no response, TLS certificate hostname mismatch on the robots.txt fetch; not in the route list, so recorded as cannot; not retried or bypassed |
| sxodim.uz | https://sxodim.uz/ | cannot | - | allowed | 200 | 2026-11-21 | sxodim-uz | P3 | UZ | cannot: render-only page, no renderer bound (Vite shell, empty root div); robots Sitemap https://sxodim.uz/sitemap.xml exists but the shell rule comes first; Uzbek edition of the registry sxodim group |
| proart.uz | https://proart.uz/ | generic-feed | https://proart.uz/feed/ (unverified) | allowed | 200 | 2026-11-21 | proart-uz | P3 | UZ | Event agency (concerts, festivals, exhibitions); WordPress feed; posts may cover only its own productions |
| namangan-tourism.uz | https://namangan-tourism.uz/ | cannot | - | allowed | 503 | 2026-11-21 | namangan-tourism | P3 | UZ | cannot: challenge per the route rule; the 503 is a plain nginx Service Unavailable page, not a challenge page, so it may be an outage; robots Sitemap https://namangan-tourism.uz/sitemap.xml not fetched; re-probe later |
| 98mag.kz | https://www.98mag.kz/ | generic-site | https://www.98mag.kz/sitemap_index.xml | allowed | 200 | 2026-11-21 | 98mag | P3 | KZ | Culture, style and city magazine; sitemap index; no feed or JSON-LD Event |
| elle.com.kz | https://elle.com.kz/ | generic-site | https://elle.com.kz/sitemap.xml | allowed | 200 | 2026-11-21 | elle-kz | P3 | KZ | passive script: Cloudflare challenge-platform on a complete 200 page, read as content; no feed or JSON-LD Event; the registry holds ELLE Uzbekistan, not this edition |
| esquire.kz | https://esquire.kz/ | generic-site | https://esquire.kz/sitemap.xml | allowed | 200 | 2026-11-21 | esquire-kz | P3 | KZ | Sitemap only; JSON-LD is organization types, no Event |
| tatlerasia.kz | https://tatlerasia.kz/ | manual | - | allowed | 200 | 2026-11-21 | tatler-kz | P3 | KZ | 301 to /ru; no robots Sitemap line, feed or JSON-LD Event; needs a page reader over its fashion section |
| weproject.media | https://weproject.media/ | generic-site | https://weproject.media/sitemap.xml | allowed | 200 | 2026-11-21 | weproject | P3 | KZ | passive script on a complete 200 page, read as content; weekend event guides and fashion news; sitemap only |
| kassir.kz | https://kassir.kz/en/all/page/organizers | manual | - | none (404) | 200 | 2026-11-21 | kassir-kz | P3 | KZ | Probed the archive page, which is the organizers info page and not a listing; robots.txt 404; no feed, sitemap or JSON-LD; needs an events listing URL and a page reader |
| kassir.kg | https://kassir.kg/ | manual | - | allowed | 200 | 2026-11-21 | kassir-kg | P3 | KG | 307 and 308 to /ru; no robots Sitemap line, feed or JSON-LD Event; needs a page reader over its event listing |
| bishkekft.com | https://bishkekft.com/ | generic-feed | https://bishkekft.com/feed/ (unverified) | allowed | 200 | 2026-11-21 | bishkek-fashion-textile | P3 | KG | Fair site on WordPress; JSON-LD CollectionPage, no Event |
| echipta.tj | https://echipta.tj/ | cannot | - | no rules (robots.txt returns the app HTML) | 200 | 2026-11-21 | echipta-tj | P3 | TJ | cannot: render-only page, no renderer bound (Vite shell, empty app div); robots.txt answers the app HTML, no rules |
| ticketon.tj | https://ticketon.tj/ | generic-site | https://ticketon.tj/sitemap.xml | allowed | 200 | 2026-11-21 | ticketon-tj | P3 | TJ | passive script: Cloudflare challenge-platform on a complete 200 page, read as content; the registry ticketon group answered 403 on .kz and .uz, this host did not |
| tourismboard.az | https://www.tourismboard.az/ | manual | - | allowed | 200 | 2026-11-21 | azerbaijan-tourism-board | P3 | AZ | passive script on a complete 200 page, read as content; probed the home page, not the /event section the archive cited; no Sitemap line, feed or JSON-LD Event; needs a page reader |
| moscowfashion.ru | https://moscowfashion.ru/ | cannot | - | not read (no response) | - | 2026-11-21 | moscow-fashion-week | P3 | RU | cannot: no response, connection reset by peer on the robots.txt fetch; not retried |
| mffrussia.com | https://www.mffrussia.com/ | generic-feed | https://www.mffrussia.com/blog-feed.xml (unverified) | allowed | 200 | 2026-11-21 | moscow-fashion-fair | P3 | RU | Wix site, Moscow Fashion Fair 2026; /blog-feed.xml is the blog feed; robots lists 12 language sitemaps, the main one is given |
| cis-fashion.ru | https://cis-fashion.ru/news | generic-site | http://cis-fashion.ru/sitemap.xml | allowed | 200 | 2026-11-21 | cis-fashion | P3 | RU | DDoS-Guard in front, page complete; the probed page is /news; robots Sitemap is given as http:// |
| cpm-moscow.com | https://cpm-moscow.com/press/ | manual | - | allowed | 200 | 2026-11-21 | cpm-moscow | P3 | RU | Fashion trade fair; the probed page is /press/; no Sitemap line, feed or JSON-LD Event; needs a page reader |
| designoutlook.ru | https://designoutlook.ru/ | generic-site | https://designoutlook.ru/sitemap.xml | allowed | 200 | 2026-11-21 | design-outlook | P3 | RU | DDoS-Guard in front, page complete; annual young-designers contest site (Design-Perspective); sitemap only |
| riamoda.ru | https://riamoda.ru/ | generic-feed | https://riamoda.ru/rss.xml (unverified) | allowed | 200 | 2026-11-21 | riamoda | P3 | RU | Fashion news agency; RSS advertised; robots Sitemap is http://www.riamoda.ru/site_map.xml |
| exponet.ru | https://exponet.ru/exhibitions/area/cis/topics/moda/dates/future/index.en.html | generic-site | https://www.exponet.ru/sitemap.xml | allowed | 200 | 2026-11-21 | exponet | P3 | RU | Fair directory; probed the CIS fashion future-dates listing; sitemap on the www host; no feed or JSON-LD |
| eventseye.com | https://www.eventseye.com/fairs/cst1_trade-shows_kyrgyzstan_fabrics-clothing-textiles.html | manual | - | none (404) | 200 | 2026-11-21 | eventseye | P3 | multi | Trade-show directory; probed the Kyrgyzstan fabrics-clothing-textiles listing; robots.txt 404; no feed, sitemap or JSON-LD; needs a listing reader per country page |
| styleofeurasia.com | https://www.styleofeurasia.com/ | generic-feed | https://www.styleofeurasia.com/?format=feed&type=rss (unverified) | allowed | 200 | 2026-11-21 | style-of-eurasia | P3 | KZ | Style and fashion magazine on Joomla; RSS and Atom both advertised (the Atom twin is ?format=feed&type=atom); no robots Sitemap line |
| t.me/aydatuda | https://t.me/s/aydatuda (not fetched) | manual | - | t.me/robots.txt 404 per plan #2, not fetched | not fetched | 2026-11-21 | aydatuda | P3 | UZ (unconfirmed) | Not fetched: t.me is a registry host, which the brief bars; needs one paced GET of t.me/s/aydatuda to confirm dated messages, then telegram-preview; country unconfirmed |
| telegram.me | https://t.me/s/proartworld (not fetched) | manual | - | t.me/robots.txt 404 per plan #2, not fetched | not fetched | 2026-11-21 | proart-world-tg | P3 | UZ | Not fetched: t.me is a registry host, which the brief bars; the archive cites the telegram.me alias; needs one paced GET of t.me/s/proartworld to confirm dated messages, then telegram-preview |

## Left for a later pass

- Dropped from the URL alone with reason "root URL only, purpose not evident from the URL": `atr.one`, `bee-lifestyle.ru`, `cahp.uz`, `dmibf.ru`, `go-go.uz`, `msfd.ru`, `om.tomskvoi.ru`, `uzbekheritage.org`. One paced probe each would settle them.
- `namangan-tourism.uz` (503) wants a re-probe on another day; the two Telegram keeps want one `t.me/s/{name}` check once `t.me` is cleared.
- Table B tiers are `P3` except `tashkentdesignweek.uz`, which carries the same event as the registry's P2 group `tashkent-design-week`. Group ids avoid every registry id.

