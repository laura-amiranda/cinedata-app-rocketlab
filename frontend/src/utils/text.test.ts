import { describe, expect, it } from 'vitest';
import { limparTitulo } from './text';

describe('limparTitulo', () => {
  it('mantém um título normal sem alterações', () => {
    expect(limparTitulo('O Poderoso Chefão')).toBe('O Poderoso Chefão');
  });

  it('remove aspas duplicadas de artefato do CSV', () => {
    expect(limparTitulo('""stone Cold""')).toBe('stone Cold');
  });

  it('remove aspas simples que envolvem o título inteiro', () => {
    expect(limparTitulo('"""blessed"""')).toBe('blessed');
  });

  it('tira espaços em branco nas pontas', () => {
    expect(limparTitulo('  Matrix  ')).toBe('Matrix');
  });
});