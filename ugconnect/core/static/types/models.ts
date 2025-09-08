/**
 * TypeScript type definitions for Uganda Tech Connect Django models
 */

// Base model interface
interface BaseModel {
    id: number;
    created_at: string;
    updated_at: string;
}

// Program model
export interface Program extends BaseModel {
    name: string;
    description: string;
    start_date: string;
    end_date: string;
    status: 'planning' | 'active' | 'completed' | 'on_hold';
    coordinator: string;
    max_participants: number;
    current_participants: number;
    budget: number;
    objectives: string;
    expected_outcomes: string;
}

// Facility model
export interface Facility extends BaseModel {
    name: string;
    location: string;
    facility_type: 'incubator' | 'accelerator' | 'fab_lab' | 'co_working' | 'research_lab' | 'training_center';
    capacity: number;
    current_occupancy: number;
    contact_person: string;
    contact_email: string;
    contact_phone: string;
    amenities: string;
    availability_schedule: string;
    booking_requirements: string;
}

// Equipment model
export interface Equipment extends BaseModel {
    name: string;
    facility: number; // Foreign key to Facility
    equipment_type: '3d_printer' | 'laser_cutter' | 'cnc_machine' | 'electronics' | 'computer' | 'measurement' | 'other';
    model: string;
    manufacturer: string;
    specifications: string;
    status: 'available' | 'in_use' | 'maintenance' | 'out_of_order';
    location_in_facility: string;
    usage_cost_per_hour: number;
    maintenance_schedule: string;
    user_manual_url?: string;
    training_required: boolean;
}

// Project model
export interface Project extends BaseModel {
    title: string;
    description: string;
    program: number; // Foreign key to Program
    project_lead: string;
    team_members: string;
    start_date: string;
    expected_completion: string;
    status: 'concept' | 'development' | 'testing' | 'completed' | 'commercialized';
    innovation_area: 'fintech' | 'agritech' | 'healthtech' | 'edtech' | 'cleantech' | 'other';
    target_market: string;
    funding_received: number;
    funding_goal: number;
    milestones: string;
    challenges: string;
    potential_impact: string;
    commercialization_plan: string;
}

// Service model
export interface Service extends BaseModel {
    name: string;
    description: string;
    service_type: 'mentorship' | 'training' | 'consultation' | 'technical_support' | 'funding' | 'networking';
    provider: string;
    provider_contact: string;
    cost: number;
    duration_hours: number;
    availability: string;
    requirements: string;
    target_audience: string;
    booking_process: string;
    facility?: number; // Optional foreign key to Facility
}

// Participant model
export interface Participant extends BaseModel {
    name: string;
    email: string;
    phone: string;
    organization?: string;
    role: string;
    program: number; // Foreign key to Program
    participation_type: 'entrepreneur' | 'mentor' | 'investor' | 'partner' | 'facilitator';
    skills: string;
    interests: string;
    experience_level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
    linkedin_profile?: string;
    github_profile?: string;
    website?: string;
    bio: string;
}

// Outcome model
export interface Outcome extends BaseModel {
    project: number; // Foreign key to Project
    outcome_type: 'product_launched' | 'patent_filed' | 'funding_secured' | 'jobs_created' | 'partnership_formed' | 'award_received';
    description: string;
    date_achieved: string;
    quantitative_measure: number;
    unit_of_measure: string;
    impact_description: string;
    verification_method: string;
    verified: boolean;
    commercial_value?: number;
    social_impact_score: number;
    sustainability_rating: 'low' | 'medium' | 'high';
}

// API Response types
export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
    message?: string;
}

export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

// Form data types
export interface ProgramFormData {
    name: string;
    description: string;
    start_date: string;
    end_date: string;
    status: string;
    coordinator: string;
    max_participants: number;
    budget: number;
    objectives: string;
    expected_outcomes: string;
}

export interface FacilityFormData {
    name: string;
    location: string;
    facility_type: string;
    capacity: number;
    contact_person: string;
    contact_email: string;
    contact_phone: string;
    amenities: string;
    availability_schedule: string;
    booking_requirements: string;
}

export interface EquipmentFormData {
    name: string;
    facility: number;
    equipment_type: string;
    model: string;
    manufacturer: string;
    specifications: string;
    status: string;
    location_in_facility: string;
    usage_cost_per_hour: number;
    maintenance_schedule: string;
    user_manual_url?: string;
    training_required: boolean;
}

export interface ProjectFormData {
    title: string;
    description: string;
    program: number;
    project_lead: string;
    team_members: string;
    start_date: string;
    expected_completion: string;
    status: string;
    innovation_area: string;
    target_market: string;
    funding_received: number;
    funding_goal: number;
    milestones: string;
    challenges: string;
    potential_impact: string;
    commercialization_plan: string;
}

export interface ServiceFormData {
    name: string;
    description: string;
    service_type: string;
    provider: string;
    provider_contact: string;
    cost: number;
    duration_hours: number;
    availability: string;
    requirements: string;
    target_audience: string;
    booking_process: string;
    facility?: number;
}

export interface ParticipantFormData {
    name: string;
    email: string;
    phone: string;
    organization?: string;
    role: string;
    program: number;
    participation_type: string;
    skills: string;
    interests: string;
    experience_level: string;
    linkedin_profile?: string;
    github_profile?: string;
    website?: string;
    bio: string;
}

export interface OutcomeFormData {
    project: number;
    outcome_type: string;
    description: string;
    date_achieved: string;
    quantitative_measure: number;
    unit_of_measure: string;
    impact_description: string;
    verification_method: string;
    verified: boolean;
    commercial_value?: number;
    social_impact_score: number;
    sustainability_rating: string;
}

// Search and filter types
export interface SearchFilters {
    query?: string;
    status?: string;
    type?: string;
    date_from?: string;
    date_to?: string;
    location?: string;
    innovation_area?: string;
}

export interface SortOptions {
    field: string;
    direction: 'asc' | 'desc';
}

// Dashboard and analytics types
export interface DashboardStats {
    programs: {
        total: number;
        active: number;
        completed: number;
    };
    facilities: {
        total: number;
        available: number;
        occupied: number;
    };
    projects: {
        total: number;
        in_development: number;
        commercialized: number;
    };
    participants: {
        total: number;
        entrepreneurs: number;
        mentors: number;
    };
}

export interface AnalyticsData {
    labels: string[];
    datasets: {
        label: string;
        data: number[];
        backgroundColor?: string[];
        borderColor?: string[];
    }[];
}

// Notification types
export interface Notification {
    id: number;
    type: 'info' | 'success' | 'warning' | 'error';
    title: string;
    message: string;
    timestamp: string;
    read: boolean;
    action_url?: string;
}

// User and authentication types
export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    is_staff: boolean;
    is_active: boolean;
    date_joined: string;
    profile?: UserProfile;
}

export interface UserProfile {
    user: number;
    organization?: string;
    role: string;
    phone?: string;
    bio?: string;
    avatar?: string;
    linkedin_profile?: string;
    github_profile?: string;
    website?: string;
}

// Event and calendar types
export interface Event {
    id: number;
    title: string;
    description: string;
    start_datetime: string;
    end_datetime: string;
    location: string;
    event_type: 'workshop' | 'networking' | 'pitch' | 'training' | 'meeting';
    organizer: string;
    max_attendees?: number;
    current_attendees: number;
    registration_required: boolean;
    registration_deadline?: string;
    cost?: number;
}

// File and media types
export interface FileUpload {
    id: number;
    name: string;
    file: string;
    size: number;
    upload_date: string;
    content_type: string;
}

// All types are exported through their interface/type declarations above
