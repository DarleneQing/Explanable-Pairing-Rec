export class Item {
    public article_id: string;
    public prod_name: string;
    public product_type_no: number;
    public product_type_name: string;
    public product_group_name: string;
    public graphical_appearance_no: number;
    public graphical_appearance_name: string;
    public colour_group_code: number;
    public colour_group_name: string;
    public perceived_colour_value_id: number;
    public perceived_colour_value_name: string;
    public perceived_colour_master_id: number;
    public perceived_colour_master_name: string;
    public department_no: number;
    public department_name: string;
    public index_code: string;
    public index_name: string;
    public index_group_no: number;
    public index_group_name: string;
    public section_no: number;
    public section_name: string;
    public garment_group_no: number;
    public garment_group_name: string;
    public detail_desc: string;
    public sleeve_prediction: string;
    public length_prediction: string;
    public neckline_prediction: string;
    public detected_fabrics: string;

    constructor(
        article_id: string,
        prod_name: string,
        product_type_no: number,
        product_type_name: string,
        product_group_name: string,
        graphical_appearance_no: number,
        graphical_appearance_name: string,
        colour_group_code: number,
        colour_group_name: string,
        perceived_colour_value_id: number,
        perceived_colour_value_name: string,
        perceived_colour_master_id: number,
        perceived_colour_master_name: string,
        department_no: number,
        department_name: string,
        index_code: string,
        index_name: string,
        index_group_no: number,
        index_group_name: string,
        section_no: number,
        section_name: string,
        garment_group_no: number,
        garment_group_name: string,
        detail_desc: string,
        sleeve_prediction: string,
        length_prediction: string,
        neckline_prediction: string,
        detected_fabrics: string
    ) {
        this.article_id = article_id;
        this.prod_name = prod_name;
        this.product_type_no = product_type_no;
        this.product_type_name = product_type_name;
        this.product_group_name = product_group_name;
        this.graphical_appearance_no = graphical_appearance_no;
        this.graphical_appearance_name = graphical_appearance_name;
        this.colour_group_code = colour_group_code;
        this.colour_group_name = colour_group_name;
        this.perceived_colour_value_id = perceived_colour_value_id;
        this.perceived_colour_value_name = perceived_colour_value_name;
        this.perceived_colour_master_id = perceived_colour_master_id;
        this.perceived_colour_master_name = perceived_colour_master_name;
        this.department_no = department_no;
        this.department_name = department_name;
        this.index_code = index_code;
        this.index_name = index_name;
        this.index_group_no = index_group_no;
        this.index_group_name = index_group_name;
        this.section_no = section_no;
        this.section_name = section_name;
        this.garment_group_no = garment_group_no;
        this.garment_group_name = garment_group_name;
        this.detail_desc = detail_desc;
        this.sleeve_prediction = sleeve_prediction;
        this.length_prediction = length_prediction;
        this.neckline_prediction = neckline_prediction;
        this.detected_fabrics = detected_fabrics;
    }

    // Static instances with actual data from CSV
    public static readonly ITEM_529180002 = new Item(
        "529180002",
        "CARTER CHECKED",
        259,
        "Shirt",
        "Garment Upper body",
        1010004,
        "Check",
        43,
        "Dark Red",
        4,
        "Dark",
        18,
        "Red",
        1543,
        "Tops Woven",
        "D",
        "Divided",
        2,
        "Divided",
        53,
        "Divided Collection",
        1010,
        "Blouses",
        "Slightly shorter, straight-cut shirt in checked cotton with a chest pocket, classic collar and a rounded hem. Long sleeves with a cuff at the back and short slits in the sides.",
        "long_sleeve",
        "no_dress",
        "crew_neckline",
        "None detected"
    );

    public static readonly ITEM_830185001 = new Item(
        "830185001",
        "Polly Jean PU",
        275,
        "Skirt",
        "Garment Lower body",
        1010016,
        "Solid",
        9,
        "Black",
        4,
        "Dark",
        5,
        "Black",
        1444,
        "Skirts",
        "D",
        "Divided",
        2,
        "Divided",
        53,
        "Divided Collection",
        1012,
        "Skirts",
        "Short skirt in grained imitation leather. High waist with a zip and hook-and-eye fastener at the back. Front pockets with a zip at the top. Lined.",
        "sleeveless",
        "no_dress",
        "no_neckline",
        "leather"
    );
}