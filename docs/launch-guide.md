# Launching the Tumbleweeds website

A step-by-step guide for putting the site on tumbleweedsvolleyball.com. It is written for a club volunteer. Where a step needs a developer (Chez Koop), it says so.

**Where things stand today.** tumbleweedsvolleyball.com is a Squarespace "Coming soon" page. A DNS lookup shows the domain's nameservers are Squarespace's (`nsd1` to `nsd4.squarespacedns.com`), `www` points to `ext-sq.squarespace.com`, and email is handled by Google (one MX record, `smtp.google.com`). So: the domain is managed in Squarespace, and **email must keep working through the move**. Section 4 protects it.

## 1. Choose a host (managed WordPress, Canada)

The theme needs WordPress 6.4 or newer and PHP 8.1 or newer. Pick a host that is "managed WordPress" so updates, backups and SSL are handled for you.

| Option | Why it fits | Check before buying |
|---|---|---|
| Kinsta | Managed WordPress with Canadian data centres (Montreal, Toronto) | Current plan price, and that the data centre you pick is in Canada |
| WP Engine | Managed WordPress, Canadian region available | Same two checks |
| Cloudways | Cheaper, you choose a Toronto server, a little more hands-on | Support level, backups are paid add-ons on some plans |
| HostPapa or Web Hosting Canada | Canadian companies, low cost, phone support | That the plan is WordPress-managed with PHP 8.1 or newer |

Prices and data centre lists change, so confirm both on the host's own page. For a club site with a few hundred visits a day, the smallest plan is enough. Ask Chez Koop if the club would rather host it with them.

## 2. Install WordPress and the theme

1. Create the WordPress site at the host. Use a temporary address (the host gives you one, like `club.examplehost.com`) until section 4.
2. Log in to WordPress. Go to **Appearance, Themes, Add New, Upload Theme**. Upload `tumbleweeds-vbc.zip` (from the GitHub repository: Code, Download ZIP, then rename the top folder to `tumbleweeds-vbc` before zipping, or ask Chez Koop for the ready zip). Click **Activate**.
3. A bar appears asking to install plugins. Click **Begin installing plugins**, select all, **Install**, then **Activate**. The plugins:

| Plugin | Needed? | What it does |
|---|---|---|
| Secure Custom Fields (or ACF Pro if the club owns it) | **Required** | The boxes you fill in on every page |
| Classic Editor | Recommended | The simple editor the boxes are designed for |
| Contact Form 7 | Recommended | The contact form and the footer sign-up |
| Yoast SEO | Recommended | Page titles, search descriptions and the share picture |

4. **Settings, Permalinks**: choose **Post name** and Save.

## 3. Load the starting content (the seed)

The seed builds all pages, the two coach pages, two news posts, both menus, Club settings and the contact form. Run it **once, on a fresh site**. It overwrites seeded content, and it refuses to run again on a site that is open to search engines.

- With the host's SSH or WP-CLI (ask Chez Koop, 5 minutes): `wp eval-file wp-content/themes/tumbleweeds-vbc/seed/import.php`
- Without SSH: ask Chez Koop to run it. It cannot be run from the WordPress screens.

After it runs, open **Club settings** and check every tab. Then follow section 6.

## 4. Point tumbleweedsvolleyball.com at the new host

Do this in a quiet hour, not on a tryout or info-session day. Nothing is lost if you do it in the order below.

1. **Write down what is there first.** In Squarespace, open **Domains**, click tumbleweedsvolleyball.com, then **DNS Settings**. Take a screenshot of every record. Keep the **MX** records (email) and any **TXT** records (Google email verification, SPF, and a DKIM key if the club set one up). These must still be there at the end.
2. **Get the host's address.** Your host shows an **IP address** for the site (an A record) or a hostname (a CNAME). Kinsta, WP Engine and others call it "DNS records" in the site's domain screen.
3. **Disconnect the domain from the Squarespace "Coming soon" site.** In Squarespace, open the website's **Settings, Domains** and disconnect or remove tumbleweedsvolleyball.com from the site (if the domain is registered through Squarespace, as it appears to be, it stays registered there; check under Domains). If you skip this, Squarespace keeps serving the parking page.
4. **Edit the DNS records** (Squarespace, Domains, DNS Settings):
   - Delete the Squarespace default `A` records for `@` (the four `198.x.x.x` addresses) and the `CNAME` for `www` that points to `ext-sq.squarespace.com`.
   - Add an **A record**: Host `@`, value = the host's IP address.
   - Add a **CNAME record**: Host `www`, value = the host's hostname (or an A record to the same IP if the host says so).
   - **Do not touch MX or TXT records.**
5. **Tell the host the domain.** In the host's dashboard, add tumbleweedsvolleyball.com and www.tumbleweedsvolleyball.com to the site.
6. **Wait.** Most changes show within an hour, sometimes up to 24 hours. Check progress at dnschecker.org (search the domain, record type A).
7. **Set the WordPress address.** In WordPress: **Settings, General**, set both the WordPress Address and the Site Address to `https://tumbleweedsvolleyball.com`.
8. **Test email.** Send an email to info@tumbleweedsvolleyball.com from outside the club and confirm it arrives.

*Alternative* (if the host prefers to manage DNS): in Squarespace, **DNS Settings, Nameservers**, set the host's nameservers. Then you must re-create the MX and TXT records at the host. Use this only if the host's support walks you through it.

## 5. SSL (the padlock)

Managed hosts issue the free certificate (Let's Encrypt) by themselves once the domain points to them. In the host's dashboard find **SSL** or **HTTPS** and click **Enable** or **Force HTTPS**. Then open the site: it must show the padlock on every page. If WordPress shows mixed-content warnings, ask Chez Koop to run a search-replace from `http://` to `https://`.

## 6. Settings to change at launch

1. **Settings, Reading**: untick **Discourage search engines from indexing this site**. (The seed turns it on so the staging copy stays out of Google.)
2. **Settings, General**: Site Title and Tagline (Tumbleweeds Volleyball Club, and "Kamloops youth volleyball. Developing athletes from the ground up.").
3. **Club settings**, tab **Contact and social**: confirm the club email, then confirm **Contact form** has the shortcode filled in.
4. **Club settings**, tab **Registration** (section 9).
5. **Club settings**, tab **Sharing and analytics** (section 7).
6. **Contact, Contact Forms**: open **Contact form**, tab **Mail**, confirm **To** is the real club inbox.
7. **Email delivery.** WordPress's built-in email often lands in spam. Install **WP Mail SMTP** (free), connect it to the club's Google email account, and send the test message from the Contact form settings. Without this step, form messages can go missing.
8. **Remove the "Placeholder photography" line**: Club settings, tab Footer, Small print, once real photos are in.

## 7. Analytics and sharing

- **Google Analytics.** Create a GA4 property at analytics.google.com, copy the **Measurement ID** (starts with `G-`), and paste it into Club settings, tab **Sharing and analytics**. Empty means nothing loads and nothing is tracked. By default it runs **without cookies** (counts visits only). Turn on **Allow analytics cookies** only if the club adds a cookie notice and updates the privacy page. Visits by logged-in editors are not counted.
- **Share picture.** The theme ships a 1200 by 630 picture (logo and "Developing athletes from the ground up."). Yoast uses it as the default for every page (set by the seed; change under **SEO, Settings, Social**). Without Yoast the theme uses it, or the picture chosen in Club settings. Test a page at the Facebook Sharing Debugger.
- **Search titles.** Each page has its own title and description (the seed fills them in). Edit them in the **Yoast SEO** box under each page.
- **Search Console.** Add the site at search.google.com/search-console and submit `https://tumbleweedsvolleyball.com/sitemap_index.xml` (Yoast makes it).

## 8. Forms

- **Contact form.** Contact Form 7 sends each message to the club email and shows a confirmation on the page. Edit the fields under **Contact, Contact Forms**. The page itself reads the form from Club settings, tab Contact and social.
- **Footer sign-up.** Three choices, in this order of priority:
  1. **Embed code** from Mailchimp or Flodesk (Club settings, tab Footer): paste it and it replaces everything else.
  2. **Sign-up form** (Contact Form 7, ready-made): each sign-up is emailed to the club, who adds the address to its mailing list by hand. Fine for a small list.
  3. If both are empty, a simple form opens the visitor's email app.
  
  Canadian anti-spam law (CASL) needs permission before sending club news. A Mailchimp or Flodesk form handles consent and unsubscribe properly, so use one once the list grows.
- **Without the plugin**, the contact form and sign-up only open the visitor's email app. They are not real forms, so install Contact Form 7 before launch.
- **Spam.** Contact Form 7 supports reCAPTCHA or Cloudflare Turnstile (**Contact, Integration**) if spam shows up.

## 9. Registration (TeamSnap or Volleyball BC)

Club settings, tab **Registration**:
- **Registration link**: paste the address of the registration page (the club's TeamSnap registration page, or the Volleyball BC one).
- **Words on the registration buttons**: for example Register now.

While the link is empty, nothing changes on the site. Once it is filled in, these buttons use it (and open in a new tab):
- the yellow **menu button**, if "Menu button is the registration button" is on in Club settings (on in the seed),
- the **main button at the top of a page**, on pages that have "Main button is the registration button" switched on (the Tryouts page in the seed),
- any **Call to action** section with "Button is the registration button" switched on (the "Register for tryouts" section on the Fees page in the seed). Its "Coming soon" tag then hides.

Then edit the words around the buttons (for example "Registration opens before tryouts") so they match.

## 10. Privacy policy

A plain-language draft is on the site at **/privacy-policy/** and linked in the footer. It is marked **Club to review**. A board member should read it, fix anything untrue (which email service, how long messages are kept, whether analytics is on), and then delete the "Club to review" paragraph and the "Club to review" label in the page's top section. Update the "Last updated" date whenever the text changes. It is not legal advice.

## 11. Backups

Managed hosts take daily backups. Confirm in the host dashboard: how many days are kept, and how to restore. Also: **before any big edit or plugin update, click "Back up now"** in the host dashboard. Keep a copy of the theme and the seed in the GitHub repository (it is there already).

## 12. Pre-launch checklist

Tick every line before pointing the domain.

**Facts**
- [ ] Every "Coming soon" tag is either filled in or deliberately left
- [ ] Info session date, time and place correct (Club settings, Info session)
- [ ] Club complaints contact named (or "coming soon" is intentional)
- [ ] Fees, tryout dates, practice location confirmed before they are written down
- [ ] The award line reads exactly: 2024 U Sports Men's Volleyball Coach of the Year
- [ ] No TRU or WolfPack logos anywhere

**Photos**
- [ ] Placeholder (Unsplash) photos replaced after club photo day, with alt text
- [ ] Coach headshots are the real ones
- [ ] Footer small print about placeholder photos removed

**Forms**
- [ ] Contact form sent a test message and it arrived in the club inbox (check spam too)
- [ ] Footer sign-up tested (embed code or ready-made form)
- [ ] WP Mail SMTP connected and tested

**Analytics and search**
- [ ] GA4 Measurement ID entered and a visit shows in Realtime
- [ ] "Discourage search engines" is OFF
- [ ] Sitemap submitted in Search Console
- [ ] A shared link shows the picture and title

**Privacy and legal**
- [ ] Privacy policy reviewed by the club and the review notes removed
- [ ] Cookie notice added if analytics cookies were switched on

**Registration**
- [ ] Registration link entered and every registration button tested

**Technical**
- [ ] HTTPS padlock on every page, www and non-www both work
- [ ] Club email still arrives after the DNS change
- [ ] Checked on a phone and a computer
- [ ] Backups confirmed
