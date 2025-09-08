/**
 * API Service Layer for Uganda Tech Connect
 * TypeScript implementation for API interactions
 */

import type {
    Program, Facility, Equipment, Project, Service, Participant, Outcome,
    ApiResponse, PaginatedResponse, SearchFilters, SortOptions
} from '../types/models';

// Base API configuration
interface ApiConfig {
    baseURL: string;
    timeout: number;
    headers: Record<string, string>;
}

// HTTP methods
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

// API request options
interface RequestOptions {
    method?: HttpMethod;
    headers?: Record<string, string>;
    body?: any;
    params?: Record<string, string | number | boolean>;
}

// Base API Service
class BaseApiService {
    private config: ApiConfig;

    constructor(config?: Partial<ApiConfig>) {
        this.config = {
            baseURL: '/api',
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            ...config
        };

        // Add CSRF token if available
        const csrfToken = this.getCSRFToken();
        if (csrfToken) {
            this.config.headers['X-CSRFToken'] = csrfToken;
        }
    }

    private getCSRFToken(): string | null {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        return cookieValue || null;
    }

    private buildURL(endpoint: string, params?: Record<string, string | number | boolean>): string {
        const url = new URL(endpoint, window.location.origin + this.config.baseURL);
        
        if (params) {
            Object.entries(params).forEach(([key, value]) => {
                url.searchParams.append(key, String(value));
            });
        }

        return url.toString();
    }

    private async request<T>(endpoint: string, options: RequestOptions = {}): Promise<ApiResponse<T>> {
        const url = this.buildURL(endpoint, options.params);
        const headers = { ...this.config.headers, ...options.headers };

        try {
            const response = await fetch(url, {
                method: options.method || 'GET',
                headers,
                body: options.body ? JSON.stringify(options.body) : undefined,
                signal: AbortSignal.timeout(this.config.timeout),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            return {
                success: true,
                data,
                message: data.message
            };
        } catch (error) {
            console.error('API Request Error:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error occurred'
            };
        }
    }

    // Public HTTP methods
    protected async get<T>(endpoint: string, params?: Record<string, string | number | boolean>): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, { method: 'GET', params });
    }

    protected async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, { method: 'POST', body });
    }

    protected async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, { method: 'PUT', body });
    }

    protected async patch<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, { method: 'PATCH', body });
    }

    protected async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
        return this.request<T>(endpoint, { method: 'DELETE' });
    }
}

// Generic CRUD Service
class CrudService<T extends { id: number }> extends BaseApiService {
    constructor(private endpoint: string) {
        super();
    }

    async list(filters?: SearchFilters, sort?: SortOptions): Promise<ApiResponse<PaginatedResponse<T>>> {
        const params: Record<string, string | number | boolean> = {};
        
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== '') {
                    params[key] = value;
                }
            });
        }
        
        if (sort) {
            params.ordering = sort.direction === 'desc' ? `-${sort.field}` : sort.field;
        }

        return this.get<PaginatedResponse<T>>(`${this.endpoint}/`, params);
    }

    async retrieve(id: number): Promise<ApiResponse<T>> {
        return this.get<T>(`${this.endpoint}/${id}/`);
    }

    async create(data: Omit<T, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<T>> {
        return this.post<T>(`${this.endpoint}/`, data);
    }

    async update(id: number, data: Partial<T>): Promise<ApiResponse<T>> {
        return this.put<T>(`${this.endpoint}/${id}/`, data);
    }

    async partialUpdate(id: number, data: Partial<T>): Promise<ApiResponse<T>> {
        return this.patch<T>(`${this.endpoint}/${id}/`, data);
    }

    async destroy(id: number): Promise<ApiResponse<void>> {
        return this.delete<void>(`${this.endpoint}/${id}/`);
    }
}

// Specific API Services
export class ProgramService extends CrudService<Program> {
    constructor() {
        super('programs');
    }

    async getStatistics(id: number): Promise<ApiResponse<any>> {
        return this.get<any>(`programs/${id}/statistics/`);
    }

    async getParticipants(id: number): Promise<ApiResponse<PaginatedResponse<Participant>>> {
        return this.get<PaginatedResponse<Participant>>(`programs/${id}/participants/`);
    }

    async addParticipant(programId: number, participantId: number): Promise<ApiResponse<void>> {
        return this.post<void>(`programs/${programId}/participants/`, { participant_id: participantId });
    }

    async removeParticipant(programId: number, participantId: number): Promise<ApiResponse<void>> {
        return this.delete<void>(`programs/${programId}/participants/${participantId}/`);
    }
}

export class FacilityService extends CrudService<Facility> {
    constructor() {
        super('facilities');
    }

    async getEquipment(id: number): Promise<ApiResponse<PaginatedResponse<Equipment>>> {
        return this.get<PaginatedResponse<Equipment>>(`facilities/${id}/equipment/`);
    }

    async getAvailability(id: number, date: string): Promise<ApiResponse<any>> {
        return this.get<any>(`facilities/${id}/availability/`, { date });
    }

    async bookFacility(id: number, bookingData: any): Promise<ApiResponse<any>> {
        return this.post<any>(`facilities/${id}/book/`, bookingData);
    }
}

export class EquipmentService extends CrudService<Equipment> {
    constructor() {
        super('equipment');
    }

    async getUsageHistory(id: number): Promise<ApiResponse<any[]>> {
        return this.get<any[]>(`equipment/${id}/usage-history/`);
    }

    async reportMaintenance(id: number, maintenanceData: any): Promise<ApiResponse<any>> {
        return this.post<any>(`equipment/${id}/maintenance/`, maintenanceData);
    }

    async requestTraining(id: number, userInfo: any): Promise<ApiResponse<any>> {
        return this.post<any>(`equipment/${id}/training-request/`, userInfo);
    }
}

export class ProjectService extends CrudService<Project> {
    constructor() {
        super('projects');
    }

    async getOutcomes(id: number): Promise<ApiResponse<PaginatedResponse<Outcome>>> {
        return this.get<PaginatedResponse<Outcome>>(`projects/${id}/outcomes/`);
    }

    async addOutcome(projectId: number, outcomeData: Omit<Outcome, 'id' | 'project' | 'created_at' | 'updated_at'>): Promise<ApiResponse<Outcome>> {
        return this.post<Outcome>(`projects/${projectId}/outcomes/`, outcomeData);
    }

    async getMilestones(id: number): Promise<ApiResponse<any[]>> {
        return this.get<any[]>(`projects/${id}/milestones/`);
    }

    async updateMilestone(projectId: number, milestoneId: number, data: any): Promise<ApiResponse<any>> {
        return this.patch<any>(`projects/${projectId}/milestones/${milestoneId}/`, data);
    }

    async getFunding(id: number): Promise<ApiResponse<any>> {
        return this.get<any>(`projects/${id}/funding/`);
    }
}

export class ServiceService extends CrudService<Service> {
    constructor() {
        super('services');
    }

    async bookService(id: number, bookingData: any): Promise<ApiResponse<any>> {
        return this.post<any>(`services/${id}/book/`, bookingData);
    }

    async getProviderServices(providerId: string): Promise<ApiResponse<PaginatedResponse<Service>>> {
        return this.get<PaginatedResponse<Service>>('services/', { provider: providerId });
    }

    async rateService(id: number, rating: number, review?: string): Promise<ApiResponse<any>> {
        return this.post<any>(`services/${id}/rate/`, { rating, review });
    }
}

export class ParticipantService extends CrudService<Participant> {
    constructor() {
        super('participants');
    }

    async getProfile(id: number): Promise<ApiResponse<any>> {
        return this.get<any>(`participants/${id}/profile/`);
    }

    async updateProfile(id: number, profileData: any): Promise<ApiResponse<any>> {
        return this.patch<any>(`participants/${id}/profile/`, profileData);
    }

    async getProjects(id: number): Promise<ApiResponse<PaginatedResponse<Project>>> {
        return this.get<PaginatedResponse<Project>>(`participants/${id}/projects/`);
    }

    async getNetworking(id: number): Promise<ApiResponse<any[]>> {
        return this.get<any[]>(`participants/${id}/networking/`);
    }
}

export class OutcomeService extends CrudService<Outcome> {
    constructor() {
        super('outcomes');
    }

    async verify(id: number, verificationData: any): Promise<ApiResponse<Outcome>> {
        return this.post<Outcome>(`outcomes/${id}/verify/`, verificationData);
    }

    async getImpactReport(id: number): Promise<ApiResponse<any>> {
        return this.get<any>(`outcomes/${id}/impact-report/`);
    }

    async exportData(filters?: SearchFilters): Promise<ApiResponse<Blob>> {
        const params: Record<string, string | number | boolean> = {};
        
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== '') {
                    params[key] = value;
                }
            });
        }

        return this.get<Blob>('outcomes/export/', params);
    }
}

// Search Service
export class SearchService extends BaseApiService {
    async globalSearch(query: string, filters?: SearchFilters): Promise<ApiResponse<any>> {
        const params: Record<string, string | number | boolean> = { q: query };
        
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== '') {
                    params[key] = value;
                }
            });
        }

        return this.get<any>('search/', params);
    }

    async getSuggestions(query: string): Promise<ApiResponse<string[]>> {
        return this.get<string[]>('search/suggestions/', { q: query });
    }

    async getRecentSearches(): Promise<ApiResponse<string[]>> {
        return this.get<string[]>('search/recent/');
    }
}

// Analytics Service
export class AnalyticsService extends BaseApiService {
    async getDashboardStats(): Promise<ApiResponse<any>> {
        return this.get<any>('analytics/dashboard/');
    }

    async getProgramAnalytics(programId?: number): Promise<ApiResponse<any>> {
        const params = programId !== undefined ? { program: programId } : undefined;
        return this.get<any>('analytics/programs/', params);
    }

    async getProjectAnalytics(timeframe: string = '6m'): Promise<ApiResponse<any>> {
        return this.get<any>('analytics/projects/', { timeframe });
    }

    async getParticipantAnalytics(): Promise<ApiResponse<any>> {
        return this.get<any>('analytics/participants/');
    }

    async getOutcomeAnalytics(): Promise<ApiResponse<any>> {
        return this.get<any>('analytics/outcomes/');
    }

    async exportReport(type: string, filters?: any): Promise<ApiResponse<Blob>> {
        return this.post<Blob>(`analytics/export/${type}/`, filters);
    }
}

// Export service instances
export const programService = new ProgramService();
export const facilityService = new FacilityService();
export const equipmentService = new EquipmentService();
export const projectService = new ProjectService();
export const serviceService = new ServiceService();
export const participantService = new ParticipantService();
export const outcomeService = new OutcomeService();
export const searchService = new SearchService();
export const analyticsService = new AnalyticsService();

// Export base classes for extension
export { BaseApiService, CrudService };

// Utility function to handle API errors
export function handleApiError(error: ApiResponse<any>): void {
    if (error.error) {
        // Show error message using the main app's alert system
        if ((window as any).UgandaTechConnect) {
            (window as any).UgandaTechConnect.showError(error.error);
        } else {
            console.error('API Error:', error.error);
            alert(error.error); // Fallback
        }
    }
}

// Utility function to handle successful operations
export function handleApiSuccess(response: ApiResponse<any>, message?: string): void {
    if (response.success && (message || response.message)) {
        if ((window as any).UgandaTechConnect) {
            (window as any).UgandaTechConnect.showSuccess(message || response.message || 'Operation successful');
        } else {
            console.log('Success:', message || response.message);
        }
    }
}
