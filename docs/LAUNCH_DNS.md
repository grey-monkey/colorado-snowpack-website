# ColoradoSnowpack.com - website launch instructions

Updated September 21, 2026. Website launch is NOT authorized.

Squarespace remains the registrar. The approved email setup moved authoritative DNS to Cloudflare (`cloe.ns.cloudflare.com` and `matt.ns.cloudflare.com`). Cloudflare email routing and Kit authentication records are active. Keep that delegation: switching back to Squarespace or Sedo would interrupt branded email.

The website remains parked. The apex, www and wildcard A records are DNS-only and point to `64.190.63.222`. No website custom domain or recurring job has been activated.

## Only after separate owner launch approval

1. In GitHub Settings > Pages, retain GitHub Actions as the build source and set the custom domain to `coloradosnowpack.com`. Deploy the reviewed production build, removing rehearsal/noindex notices and enabling the tested signup configuration.
2. In Cloudflare DNS, replace only the apex and www parking records with the following GitHub Pages records. Keep them DNS-only during certificate setup. Preserve all Kit CNAMEs, Cloudflare MX/SPF/DKIM, DMARC, and the hello forwarding rule. Do not change nameservers.

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | grey-monkey.github.io |

3. Configure the backend's allowed origins for the final website and its tested public signup mode. Weekly delivery and refresh remain separately controlled; initialize the accepted-history state branch and verify workflow secrets before activating either schedule.
4. Wait for GitHub's certificate, enable Enforce HTTPS, and verify apex/www, downloads, form confirmation and unsubscribe on the final domain. No new paid service is required. Existing domain renewal is separate.

Rollback: disable signup and weekly sending, then restore only the website A records to the parking address if needed. Keep Cloudflare nameservers and mail records so branded email continues working. Do not clear durable delivery reservations.

This supersedes earlier instructions that proposed switching to Squarespace nameservers. The temporary GitHub Pages rehearsal has no custom domain or recurring schedule.

Reference: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
