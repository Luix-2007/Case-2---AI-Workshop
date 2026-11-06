// GET /api/saude  ->  {ok, modelo}: o site usa para saber se o chat pode ser ligado (não expõe a chave).
import { json, configured, MODEL } from "../lib/copom.mjs";

export default async () => json({ ok: configured(), modelo: MODEL });

export const config = { path: "/api/saude" };
