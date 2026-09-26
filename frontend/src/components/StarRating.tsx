interface StarRatingProps {
  /** Nota de 0 a 10 (escala usada pelo backend). */
  notaSobreDez: number | null;
}

/** Exibe uma nota (escala 0-10) como estrelas de 1 a 5, apenas para visualização. */
export function StarRatingDisplay({ notaSobreDez }: StarRatingProps) {
  if (notaSobreDez === null) {
    return <span className="stars stars-empty">Sem avaliações</span>;
  }
  const estrelas = Math.round(notaSobreDez / 2);
  return (
    <span className="stars" title={`${notaSobreDez.toFixed(1)} / 10`}>
      {'★'.repeat(estrelas)}
      {'☆'.repeat(5 - estrelas)}
    </span>
  );
}