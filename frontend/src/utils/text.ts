/**
 * Alguns títulos vieram do CSV de origem com aspas duplicadas ("") como
 * artefato de escape de exportação — ex: `"""blessed"""` deveria ser
 * apenas `blessed`, e `""stone Cold""` deveria ser `"stone Cold"`.
 * Esta função desfaz esse padrão só para exibição, sem alterar o dado no banco.
 */
export function limparTitulo(titulo: string): string {
  let t = titulo.replace(/"{2,}/g, '"').trim();
  if (t.startsWith('"') && t.endsWith('"') && t.length > 1) {
    t = t.slice(1, -1);
  }
  return t;
}