import { describe, it, expect } from 'vitest';
import { formatInr } from './formatInr';

describe('formatInr', () => {
  it('formats large numbers using Indian grouping', () => {
    expect(formatInr(1234567.89)).toBe('12,34,567.89');
  });

  it('formats a single decimal digit with two decimal places', () => {
    expect(formatInr(12345.6)).toBe('12,345.60');
  });

  it('does not add grouping separators below 1000', () => {
    expect(formatInr(500)).toBe('500.00');
  });

  it('formats if the input is 0', () => {
    expect(formatInr(0)).toBe('0.00');
  });

  it('formats if the input is 1000', () => {
    expect(formatInr(1000)).toBe('1,000.00');
  });

  it('formats if the input is 100000', () => {
    expect(formatInr(100000)).toBe('1,00,000.00');
  });

  it('formats if the input is 10000000', () => {
    expect(formatInr(10000000)).toBe('1,00,00,000.00');
  });
});
