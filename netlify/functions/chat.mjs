// POST /api/chat  {pergunta, historico?, nova?}  ->  {resposta, citacoes[]}
import { chat, json, erro, configured, rateLimited, badOrigin } from "../lib/copom.mjs";

export default async (req) => {
  if (req.method !== "POST") return json({ erro: "Use POST." }, 405);
  if (badOrigin(req)) return json({ erro: "Origem não permitida." }, 403);
  if (!configured()) return json({ erro: "O chat ainda não tem chave de API configurada no Netlify." }, 503);
  if (rateLimited(req)) return json({ erro: "Muitas perguntas seguidas. Espere um minuto." }, 429);
  try { return json(await chat(await req.json())); } catch (e) { return erro(e); }
};

export const config = { path: "/api/chat" };
