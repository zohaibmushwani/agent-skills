#!/usr/bin/env node
// gplay_probe.mjs - Google Play lookups as JSON, using the MIT-licensed google-play-scraper.
// Setup: npm i google-play-scraper   (Node 18+)
// Usage: node gplay_probe.mjs suggest "<term>" [--country us] [--lang en]
//        node gplay_probe.mjs search  "<term>" [--num 10] [--country us] [--lang en]
//        node gplay_probe.mjs app     <appId>  [--country us] [--lang en]
//        node gplay_probe.mjs reviews <appId>  [--num 50] [--sort newest|helpful|rating]
// Be polite: a few requests per second at most; cache results. Output is MEASURED data with the date/country attached.
import gplay from 'google-play-scraper';

const [cmd, arg, ...rest] = process.argv.slice(2);
const opt = (k, d) => { const i = rest.indexOf('--' + k); return i >= 0 ? rest[i + 1] : d; };
const country = opt('country', 'us'), lang = opt('lang', 'en'), num = Number(opt('num', 10));
const stamp = { country, lang, fetched: new Date().toISOString().slice(0, 10) };
if (!cmd || !arg) { console.error('usage: gplay_probe.mjs suggest|search|app|reviews <term|appId> [--country us] [--lang en] [--num N]'); process.exit(2); }
try {
  let out;
  if (cmd === 'suggest') out = { ...stamp, term: arg, suggestions: await gplay.suggest({ term: arg, country, lang }) };
  else if (cmd === 'search') {
    const r = await gplay.search({ term: arg, num, country, lang });
    out = { ...stamp, term: arg, results: r.map((a, i) => ({ rank: i + 1, appId: a.appId, title: a.title, developer: a.developer, score: a.score, free: a.free })) };
  } else if (cmd === 'app') {
    const a = await gplay.app({ appId: arg, country, lang });
    out = { ...stamp, appId: a.appId, title: a.title, summary: a.summary, description: a.description, score: a.score, ratings: a.ratings,
            installs: a.installs, minInstalls: a.minInstalls, genre: a.genre, updated: a.updated ? new Date(a.updated).toISOString().slice(0, 10) : null, developer: a.developer };
  } else if (cmd === 'reviews') {
    const sortMap = { newest: gplay.sort.NEWEST, helpful: gplay.sort.HELPFULNESS, rating: gplay.sort.RATING };
    const r = await gplay.reviews({ appId: arg, num, sort: sortMap[opt('sort', 'newest')] ?? gplay.sort.NEWEST, country, lang });
    out = { ...stamp, appId: arg, reviews: (r.data ?? r).map(x => ({ score: x.score, text: x.text, date: x.date })) };
  } else { console.error('unknown command ' + cmd); process.exit(2); }
  console.log(JSON.stringify(out, null, 1));
} catch (e) { console.error('error: ' + (e.message || e)); process.exit(1); }
