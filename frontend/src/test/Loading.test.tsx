/**
 * Tests for the Loading component
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Loading } from '../components/Loading';

describe('Loading', () => {
  it('renders with default message', () => {
    render(<Loading />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders with custom message', () => {
    render(<Loading message="Please wait..." />);
    expect(screen.getByText('Please wait...')).toBeInTheDocument();
  });

  it('renders with different sizes', () => {
    const { container, rerender } = render(<Loading size="small" />);
    expect(container.querySelector('.loading-small')).toBeInTheDocument();

    rerender(<Loading size="medium" />);
    expect(container.querySelector('.loading-medium')).toBeInTheDocument();

    rerender(<Loading size="large" />);
    expect(container.querySelector('.loading-large')).toBeInTheDocument();
  });
});
