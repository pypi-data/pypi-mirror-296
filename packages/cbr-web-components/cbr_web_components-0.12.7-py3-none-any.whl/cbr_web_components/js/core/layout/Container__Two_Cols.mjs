import Div  from "../Div.mjs";
import Span from "../Span.mjs";

export default class Container__Two_Cols extends Div {

    constructor({...kwargs}={}) {
        super({...kwargs})
        this.setup()
    }

    setup() {
        this.div_root   = new Div({ class: 'container' });
        this.row_1  = new Div({ class: 'row'});
        this.col_1  = new Div({ class: 'col'});
        this.col_2  = new Div({ class: 'col'});
        this.div_root.add_element (this.row_1            )
        this.row_1   .add_elements(this.col_1, this.col_2)
    }

    html() {
        return this.div_root.html();
    }

    css_rules() {
        return {
            ".container": {
                "display": "flex",
                "flex-direction": "column",
                "width": "100%",
                "height": "100%",
                "border": "2px black solid",
                "box-sizing": "border-box"              // Ensures padding and border are included in the element's total width and height
            },
            ".row": {
                "display": "flex",
                "flex": "1",                            // Each row takes equal space within the container
                "width": "100%",
                "align-items": "top",                   // Vertically centers the items in the row
                "justify-content": "center"             // Horizontally centers the items in the row
            },
            ".col": {
                "flex"           : "1",                 // Each column takes equal space within the row
                "display"        : "flex",
                "align-items"    : "top",               // Centers content vertically
                "justify-content": "center",            // Centers content horizontally
                "height"         : "100%",              // Ensures columns stretch to fill the row height
                "overflow-wrap"  : "break-word;"
                //"width": "50%"
            }
        };
    }

}