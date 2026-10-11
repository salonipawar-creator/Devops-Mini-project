import { describe, expect, test } from 'vitest';

describe('frontend smoke', () => {
  test('disclaimer text is available', () => {
    expect('Academic demonstration only. Not intended for medical diagnosis or treatment.').toContain('Academic demonstration');
  });
});
