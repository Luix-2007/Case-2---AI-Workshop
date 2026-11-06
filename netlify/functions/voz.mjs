// POST /api/voz  {pergunta, historico?, resumo?, nova?}  ->  texto em streaming, uma linha JSON por bloco
import { voz, json, erro, configured, rateLimited, badOrigin } from "../lib/copom.mjs";

export default async (req) => {
  if (req.method !== "POST") return json({ erro: "Use POST." }, 405);
  if (badOrigin(req)) return json({ erro: "Origem não permitida." }, 403);
  if (!configured()) return json({ erro: "A conversa ainda não tem chave de API configurada no Netlify." }, 503);
  if (rateLimited(req)) return json({ erro: "Muitas perguntas seguidas. Espere um minuto." }, 429);
  try {
    const body = voz(await req.json());
    return new Response(body, { headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store", "x-content-type-options": "nosniff" } });
  } catch (e) { return erro(e); }
};

export const config = { path: "/api/voz" };
