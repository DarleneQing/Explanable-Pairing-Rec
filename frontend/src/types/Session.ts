import { Item } from "./item";

export class Session {
    session_id: string;
    created_at: Date;
    is_active: boolean;
    name: string;
    section: string;
    garment_group: string;
    product_type: string;
    color: string;
    graphic_appearance: string;


    constructor(session_id: string, created_at: Date | string, is_active: boolean, name: string, section: string, garment_group: string, product_type: string, color: string, graphic_appearance: string) {
        this.session_id = session_id;
        this.created_at = created_at instanceof Date ? created_at : new Date(created_at);
        this.is_active = is_active;
        this.name = name;
        this.section = section;
        this.garment_group = garment_group;
        this.product_type = product_type;
        this.color = color;
        this.graphic_appearance = graphic_appearance;
    }

    // Static factory method to create Session from API response
    static fromApiResponse(apiData: any): Session {
        return new Session(
            apiData.session_id,
            apiData.created_at,
            apiData.is_active,
            apiData.name,
            apiData.section,
            apiData.garment_group,
            apiData.product_type,
            apiData.color,
            apiData.graphic_appearance
        );
    }

    // Method to convert back to plain object for API calls
    toApiData(): object {
        return {
            session_id: this.session_id,
            created_at: this.created_at.toISOString(),
            is_active: this.is_active,
            name: this.name,
            section: this.section,
            garment_group: this.garment_group,
            product_type: this.product_type,
            color: this.color,
            graphic_appearance: this.graphic_appearance
        };
    }
}