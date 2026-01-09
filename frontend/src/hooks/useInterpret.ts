/**
 * Custom hook for interpreting natural language
 */
import { useMutation } from '@tanstack/react-query';
import { api, type InterpretResponse, type ApiError } from '../services/api';

export function useInterpret() {
  return useMutation<InterpretResponse, ApiError, string>({
    mutationFn: (text: string) => api.interpret(text),
  });
}
