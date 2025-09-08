/**
 * API Service Layer for Uganda Tech Connect
 * TypeScript implementation for API interactions
 */
// Base API Service
class BaseApiService {
    constructor(config) {
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
    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || null;
    }
    buildURL(endpoint, params) {
        const url = new URL(endpoint, window.location.origin + this.config.baseURL);
        if (params) {
            Object.entries(params).forEach(([key, value]) => {
                url.searchParams.append(key, String(value));
            });
        }
        return url.toString();
    }
    async request(endpoint, options = {}) {
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
        }
        catch (error) {
            console.error('API Request Error:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error occurred'
            };
        }
    }
    // Public HTTP methods
    async get(endpoint, params) {
        return this.request(endpoint, { method: 'GET', params });
    }
    async post(endpoint, body) {
        return this.request(endpoint, { method: 'POST', body });
    }
    async put(endpoint, body) {
        return this.request(endpoint, { method: 'PUT', body });
    }
    async patch(endpoint, body) {
        return this.request(endpoint, { method: 'PATCH', body });
    }
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}
// Generic CRUD Service
class CrudService extends BaseApiService {
    constructor(endpoint) {
        super();
        this.endpoint = endpoint;
    }
    async list(filters, sort) {
        const params = {};
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
        return this.get(`${this.endpoint}/`, params);
    }
    async retrieve(id) {
        return this.get(`${this.endpoint}/${id}/`);
    }
    async create(data) {
        return this.post(`${this.endpoint}/`, data);
    }
    async update(id, data) {
        return this.put(`${this.endpoint}/${id}/`, data);
    }
    async partialUpdate(id, data) {
        return this.patch(`${this.endpoint}/${id}/`, data);
    }
    async destroy(id) {
        return this.delete(`${this.endpoint}/${id}/`);
    }
}
// Specific API Services
export class ProgramService extends CrudService {
    constructor() {
        super('programs');
    }
    async getStatistics(id) {
        return this.get(`programs/${id}/statistics/`);
    }
    async getParticipants(id) {
        return this.get(`programs/${id}/participants/`);
    }
    async addParticipant(programId, participantId) {
        return this.post(`programs/${programId}/participants/`, { participant_id: participantId });
    }
    async removeParticipant(programId, participantId) {
        return this.delete(`programs/${programId}/participants/${participantId}/`);
    }
}
export class FacilityService extends CrudService {
    constructor() {
        super('facilities');
    }
    async getEquipment(id) {
        return this.get(`facilities/${id}/equipment/`);
    }
    async getAvailability(id, date) {
        return this.get(`facilities/${id}/availability/`, { date });
    }
    async bookFacility(id, bookingData) {
        return this.post(`facilities/${id}/book/`, bookingData);
    }
}
export class EquipmentService extends CrudService {
    constructor() {
        super('equipment');
    }
    async getUsageHistory(id) {
        return this.get(`equipment/${id}/usage-history/`);
    }
    async reportMaintenance(id, maintenanceData) {
        return this.post(`equipment/${id}/maintenance/`, maintenanceData);
    }
    async requestTraining(id, userInfo) {
        return this.post(`equipment/${id}/training-request/`, userInfo);
    }
}
export class ProjectService extends CrudService {
    constructor() {
        super('projects');
    }
    async getOutcomes(id) {
        return this.get(`projects/${id}/outcomes/`);
    }
    async addOutcome(projectId, outcomeData) {
        return this.post(`projects/${projectId}/outcomes/`, outcomeData);
    }
    async getMilestones(id) {
        return this.get(`projects/${id}/milestones/`);
    }
    async updateMilestone(projectId, milestoneId, data) {
        return this.patch(`projects/${projectId}/milestones/${milestoneId}/`, data);
    }
    async getFunding(id) {
        return this.get(`projects/${id}/funding/`);
    }
}
export class ServiceService extends CrudService {
    constructor() {
        super('services');
    }
    async bookService(id, bookingData) {
        return this.post(`services/${id}/book/`, bookingData);
    }
    async getProviderServices(providerId) {
        return this.get('services/', { provider: providerId });
    }
    async rateService(id, rating, review) {
        return this.post(`services/${id}/rate/`, { rating, review });
    }
}
export class ParticipantService extends CrudService {
    constructor() {
        super('participants');
    }
    async getProfile(id) {
        return this.get(`participants/${id}/profile/`);
    }
    async updateProfile(id, profileData) {
        return this.patch(`participants/${id}/profile/`, profileData);
    }
    async getProjects(id) {
        return this.get(`participants/${id}/projects/`);
    }
    async getNetworking(id) {
        return this.get(`participants/${id}/networking/`);
    }
}
export class OutcomeService extends CrudService {
    constructor() {
        super('outcomes');
    }
    async verify(id, verificationData) {
        return this.post(`outcomes/${id}/verify/`, verificationData);
    }
    async getImpactReport(id) {
        return this.get(`outcomes/${id}/impact-report/`);
    }
    async exportData(filters) {
        const params = {};
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== '') {
                    params[key] = value;
                }
            });
        }
        return this.get('outcomes/export/', params);
    }
}
// Search Service
export class SearchService extends BaseApiService {
    async globalSearch(query, filters) {
        const params = { q: query };
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== '') {
                    params[key] = value;
                }
            });
        }
        return this.get('search/', params);
    }
    async getSuggestions(query) {
        return this.get('search/suggestions/', { q: query });
    }
    async getRecentSearches() {
        return this.get('search/recent/');
    }
}
// Analytics Service
export class AnalyticsService extends BaseApiService {
    async getDashboardStats() {
        return this.get('analytics/dashboard/');
    }
    async getProgramAnalytics(programId) {
        const params = programId !== undefined ? { program: programId } : undefined;
        return this.get('analytics/programs/', params);
    }
    async getProjectAnalytics(timeframe = '6m') {
        return this.get('analytics/projects/', { timeframe });
    }
    async getParticipantAnalytics() {
        return this.get('analytics/participants/');
    }
    async getOutcomeAnalytics() {
        return this.get('analytics/outcomes/');
    }
    async exportReport(type, filters) {
        return this.post(`analytics/export/${type}/`, filters);
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
export function handleApiError(error) {
    if (error.error) {
        // Show error message using the main app's alert system
        if (window.UgandaTechConnect) {
            window.UgandaTechConnect.showError(error.error);
        }
        else {
            console.error('API Error:', error.error);
            alert(error.error); // Fallback
        }
    }
}
// Utility function to handle successful operations
export function handleApiSuccess(response, message) {
    if (response.success && (message || response.message)) {
        if (window.UgandaTechConnect) {
            window.UgandaTechConnect.showSuccess(message || response.message || 'Operation successful');
        }
        else {
            console.log('Success:', message || response.message);
        }
    }
}
