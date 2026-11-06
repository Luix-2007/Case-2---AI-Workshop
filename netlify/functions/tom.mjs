// POST /api/tom  {reuniao, paragrafos: {n: {secao, texto}}}  ->  [{n, nota, tema, trecho}]
import { tom, json, erro, configured, rateLimited, badOrigin } from "../lib/copom.mjs";

export default async (req) => {
  if (req.method !== "POST") return json({ erro: "Use POST." }, 405);
  if (badOrigin(req)) return json({ erro: "Origem não permitida." }, 403);
  if (!configured()) return json({ erro: "O servidor ainda não tem chave de API configurada no Netlify." }, 503);
  if (rateLimited(req, 4)) return json({ erro: "Muitas medições seguidas. Espere um minuto." }, 429);
  try { return json(await tom(await req.json())); } catch (e) { return erro(e); }
};

export const config = { path: "/api/tom" };
