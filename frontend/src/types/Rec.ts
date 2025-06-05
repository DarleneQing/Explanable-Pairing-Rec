export class Rec {
    article_id: string;
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
        compatibility_score: number,
        color_importance: number,
        luminance_importance: number,
        appearance_importance: number,
        fabric_importance: number,
        neckline_importance: number,
        sleeve_importance: number,
        length_importance: number
    ) {
        this.article_id = article_id;
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
