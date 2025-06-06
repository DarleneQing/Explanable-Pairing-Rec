import { Item } from './item';

export class Rec extends Item {
    compatibility_score: number;
    color_importance: number;
    luminance_importance: number;
    appearance_importance: number;
    fabric_importance: number;
    neckline_importance: number;
    sleeve_importance: number;
    length_importance: number;

    constructor(
        article_id: string,
        prod_name: string,
        product_type_name: string,
        product_group_name: string,
        graphical_appearance_name: string,
        colour_group_name: string,
        perceived_colour_value_name: string,
        perceived_colour_master_name: string,
        index_group_name: string,
        garment_group_name: string,
        detail_desc: string,
        sleeve_prediction: string,
        length_prediction: string,
        neckline_prediction: string,
        detected_fabrics: string,
        compatibility_score: number,
        color_importance: number,
        luminance_importance: number,
        appearance_importance: number,
        fabric_importance: number,
        neckline_importance: number,
        sleeve_importance: number,
        length_importance: number
    ) {
        super(
            article_id,
            prod_name,
            product_type_name,
            product_group_name,
            graphical_appearance_name,
            colour_group_name,
            perceived_colour_value_name,
            perceived_colour_master_name,
            index_group_name,
            garment_group_name,
            detail_desc,
            sleeve_prediction,
            length_prediction,
            neckline_prediction,
            detected_fabrics
        );
        this.compatibility_score = compatibility_score;
        this.color_importance = color_importance;
        this.luminance_importance = luminance_importance;
        this.appearance_importance = appearance_importance;
        this.fabric_importance = fabric_importance;
        this.neckline_importance = neckline_importance;
        this.sleeve_importance = sleeve_importance;
        this.length_importance = length_importance;
    }

    public static readonly RECS1 = new Rec(
        "830185001",
        "Polly Jean PU",
        "Skirt",
        "Garment Lower body",
        "Solid",
        "Black",
        "Dark",
        "Black",
        "Divided",
        "Skirts",
        "Short skirt in grained imitation leather. High waist with a zip and hook-and-eye fastener at the back. Front pockets with a zip at the top. Lined.",
        "sleeveless",
        "no_dress",
        "no_neckline",
        "leather",
        0.905,
        0.145,
        0.114,
        0.140,
        0.116,
        0.175,
        0.097,
        0.213,
    );
}
