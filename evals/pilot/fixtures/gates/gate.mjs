export function gate(sample) {
  const latencyMs = sample.latencyMs ?? 0;
  const participants = sample.response?.participants ?? [];
  return { ok: latencyMs <= 200 && Array.isArray(participants), latencyMs };
}
