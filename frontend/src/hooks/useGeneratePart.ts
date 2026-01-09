/**
 * Custom hook for generating CAD parts
 */
import { useMutation } from '@tanstack/react-query';
import { api, type CadPart, type PartGenerationResult, type ApiError } from '../services/api';

export function useGeneratePart() {
  return useMutation<PartGenerationResult, ApiError, CadPart>({
    mutationFn: (part: CadPart) => api.generatePart(part),
  });
}
