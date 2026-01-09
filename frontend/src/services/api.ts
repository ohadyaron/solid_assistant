/**
 * API Client Service
 * Provides a reusable Axios-based client for communicating with the backend API
 */
import axios, { type AxiosInstance, AxiosError } from 'axios';
import type { components } from '../types/api';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Type definitions from OpenAPI
export type InterpretRequest = components['schemas']['InterpretRequest'];
export type InterpretResponse = components['schemas']['InterpretResponse'];
export type CadPart = components['schemas']['CadPart'];
export type PartGenerationResult = components['schemas']['PartGenerationResult'];
export type PartIntent = components['schemas']['PartIntent'];
export type Dimensions = components['schemas']['Dimensions'];
export type Hole = components['schemas']['Hole'];
export type Fillet = components['schemas']['Fillet'];
export type Position = components['schemas']['Position'];

// API Error type
export interface ApiError {
  message: string;
  detail?: string;
  status?: number;
}

// Create Axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if needed
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const apiError: ApiError = {
      message: error.message,
      status: error.response?.status,
    };

    if (error.response?.data) {
      const data = error.response.data as Record<string, unknown>;
      apiError.detail = (data.detail as string) || (data.message as string);
    }

    return Promise.reject(apiError);
  }
);

/**
 * API Service Methods
 */
export const api = {
  /**
   * Health check
   */
  health: async () => {
    const response = await apiClient.get<{ status: string; service: string }>('/health');
    return response.data;
  },

  /**
   * Interpret natural language into structured intent
   */
  interpret: async (text: string): Promise<InterpretResponse> => {
    const response = await apiClient.post<InterpretResponse>(
      '/api/v1/interpret',
      { text } as InterpretRequest
    );
    return response.data;
  },

  /**
   * Generate CAD part from specification
   */
  generatePart: async (part: CadPart): Promise<PartGenerationResult> => {
    const response = await apiClient.post<PartGenerationResult>(
      '/api/v1/parts',
      part
    );
    return response.data;
  },
};

export default apiClient;
