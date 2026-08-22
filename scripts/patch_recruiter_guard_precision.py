from pathlib import Path

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')
print('VERCEL_FREE_TIER_PATCH_START')


def replace_between(src: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = src.find(start_marker)
    if start < 0:
        raise SystemExit(f'start marker not found: {start_marker}')
    end = src.find(end_marker, start)
    if end < 0:
        raise SystemExit(f'end marker not found: {end_marker}')
    return src[:start] + replacement.rstrip() + '\n\n' + src[end:]


# Version.
text = text.replace('v2026.16: final recruiter-facing factual precision.', 'v2026.17: Vercel free-tier routing and provider diagnostics.', 1)
text = text.replace("const SERVICE_VERSION = '2026.16';", "const SERVICE_VERSION = '2026.17';", 1)

# Vercel currently exposes dedicated zero-cost model listings. Use those instead
# of paid-credit models so the portfolio is not blocked by free-credit restrictions.
text = text.replace(
    "const VERCEL_PRIMARY_MODEL = 'openai/gpt-oss-20b';",
    "const VERCEL_PRIMARY_MODEL = 'poolside/laguna-s-2.1-free';",
    1
)
text = text.replace(
    "const VERCEL_FALLBACK_MODELS = ['google/gemini-2.5-flash-lite', 'meta/llama-3.3-70b'];",
    "const VERCEL_FALLBACK_MODELS = ['inclusionai/ling-3.0-tiny-free', 'inclusionai/ling-3.0-flash-free'];",
    1
)

call_json = r'''function classifyProviderError(status, providerBody) {
  const q = normalizeText(providerBody);
  if (status === 403) {
    if (q.includes('customer_verification_required') || q.includes('requires a valid credit card')) return 'provider_403_customer_verification_required';
    if (q.includes('restrictedmodelserror') || q.includes('free tier users do not have access to this model')) return 'provider_403_model_restricted';
    if (q.includes('free credits temporarily have restricted access') || q.includes('paid credits continue to have unrestricted access')) return 'provider_403_free_credit_restricted';
    if (q.includes('access_denied') || q.includes('forbidden')) return 'provider_403_access_denied';
  }
  return `provider_${status}`;
}

async function callJsonEndpoint(url, apiKey, payload, timeoutMs, extraHeaders = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
        ...extraHeaders
      },
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    if (!response.ok) {
      const providerBody = await response.text().catch(() => '');
      return {
        ok: false,
        status: response.status,
        error: classifyProviderError(response.status, providerBody),
        providerBody: providerBody.slice(0, 500)
      };
    }
    return { ok: true, status: response.status, data: await response.json() };
  } catch (error) {
    return { ok: false, status: 0, error: error?.name === 'AbortError' ? 'timeout' : 'network_error' };
  } finally {
    clearTimeout(timer);
  }
}'''
text = replace_between(text, 'async function callJsonEndpoint(url, apiKey, payload, timeoutMs, extraHeaders = {}) {', 'async function callGateway(candidate, credentials, payload, timeoutOverride = null) {', call_json)

worker.write_text(text, encoding='utf-8')
print('VERCEL_FREE_TIER_PATCH_COMPLETE')
