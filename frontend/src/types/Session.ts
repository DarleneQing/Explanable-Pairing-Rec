import { Item } from "./item";

export class Session {
    session_id: string;
    created_at: Date;
    is_active: boolean;
    query_item: Item | null;
    recommendations: Item[] | null;

    constructor(session_id: string, created_at: Date | string, is_active: boolean) {
        this.session_id = session_id;
        this.created_at = created_at instanceof Date ? created_at : new Date(created_at);
        this.is_active = is_active;
    }

    // Static factory method to create Session from API response
    static fromApiResponse(apiData: any): Session {
        return new Session(
            apiData.session_id,
            apiData.created_at,
            apiData.is_active
        );
    }

    // Method to convert back to plain object for API calls
    toApiData(): object {
        return {
            session_id: this.session_id,
            created_at: this.created_at.toISOString(),
            is_active: this.is_active
        };
    }
}