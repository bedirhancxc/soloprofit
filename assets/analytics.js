/*
 * SoloProfit private web analytics. INACTIVE until a public project token is
 * set at deployment from GitHub Actions variables. Never commit phx_ keys.
 * Analytics configuration is a generated public browser file and never includes
 * personal tokens, login keys or anything confidential. No public dashboard.
 */
(function () {
  "use strict";
  const config = window.SOLOPROFIT_ANALYTICS_CONFIG || {};
  const PROJECT_TOKEN = typeof config.token === "string" ? config.token : "";
  const API_HOST = typeof config.host === "string" ? config.host : "";
  if (!/^phc_[A-Za-z0-9]+$/.test(PROJECT_TOKEN)) return;
  if (!["https://eu.i.posthog.com", "https://us.i.posthog.com"].includes(API_HOST)) return;
  if (window.location.hostname !== "bedirhancxc.github.io" ||
      !window.location.pathname.startsWith("/soloprofit/")) return;

  // Standard PostHog browser SDK loader. Load only after configuration.
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],o="init capture register register_once unregister getFeatureFlag isFeatureEnabled reloadFeatureFlags identify reset get_distinct_id alias set_config opt_in_capturing opt_out_capturing".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  let referrer = "";
  try {
    if (document.referrer) referrer = new URL(document.referrer).hostname;
  } catch (ignored) {
    // Do not allow malformed referral URLs to disrupt the calculators.
  }
  window.posthog.init(PROJECT_TOKEN, {
    api_host: API_HOST,
    defaults: "2026-05-30",
    cookieless_mode: "always",
    person_profiles: "never",
    autocapture: false,
    capture_pageview: false,
    capture_pageleave: false,
    disable_session_recording: true,
    disable_surveys: true,
    disable_web_experiments: true,
    advanced_disable_feature_flags: true,
    loaded: function (client) {
      client.capture("$pageview", {
        $current_url: window.location.origin + window.location.pathname,
        $pathname: window.location.pathname,
        $referring_domain: referrer || "$direct"
      });
    }
  });
})();
