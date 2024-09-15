import Web_Component from "../../core/Web_Component.mjs";
import API__Invoke   from "../../data/API__Invoke.mjs";
import A             from "../../core/A.mjs";
import B             from "../../core/B.mjs";
import Div           from "../../core/Div.mjs";
import HR            from "../../core/HR.mjs";
import Span          from "../../core/Span.mjs";
import Tag           from "../../core/Tag.mjs";


export default class WebC__S3_Browser__Server_Requests extends Web_Component {

    static url__api_list_files   = "/api/server/requests-in-s3/list-files?parent_folder=server-requests/cbr-website-dev-local/2024-09-13/16/api/server/docs"
    static url__api_list_folders = "/api/server/requests-in-s3/list-folders?parent_folder="

    constructor() {
        super();
    }

    async connectedCallback() {
        super.connectedCallback()
        this.setup()
        await this.build()

        //setTimeout(this.simulate_click,500)
    }

    simulate_click = () => {
        const folder_link = this.shadowRoot.querySelector(".folder-link");
        folder_link.click()
    }

    setup() {
        this.api_invoke  = new API__Invoke()
        this.api_invoke.mock_responses = JSON.parse(this.getAttribute('mock_responses'))
        this.current_paths = []
        this.current_folder = '/'
        this.current_path   = ''
        this.previous_path  = ''

        window.dd = this
    }

    async api_get_folders(parent_folder) {
        const api_path = WebC__S3_Browser__Server_Requests.url__api_list_folders + (parent_folder || '')
        const method   = 'GET'
        const data     = null
        return await this.api_invoke.invoke_api(api_path, method, data)
    }

    async build(current_path) {
        let folders  = await this.api_get_folders(current_path)
        let raw_html = await this.html(folders)
        this.set_inner_html(raw_html)
        this.set_event_listeners()
    }

    set_event_listeners() {
        const folder_links = this.shadowRoot.querySelectorAll(".folder-link");
        const parent_link = this.shadowRoot.querySelector(".parent-link");
        folder_links.forEach(link => {
            link.addEventListener('click', this.on_click__folder_link.bind(this));
        });
        parent_link.addEventListener('click', this.on_click__parent_link.bind(this));
    }

    async add_folder(folder_name) {
        this.current_folder = folder_name
        if (this.previous_path === '')  {
            this.previous_path = '/'
        }
        else {
            this.previous_path = this.current_path
        }
        this.current_path  += folder_name + '/'
        this.current_paths.push({folder_name: folder_name, folder_path: this.current_path })
        await this.build(this.current_path)
    }

    async on_click__folder_link(event) {
        event.preventDefault()
        const clicked_element = event.target;                           // Get the clicked element (the anchor tag)
        const target_folder = clicked_element.attributes.href.value
        //const folder_name = clicked_element.textContent.trim();     // Retrieve the folder path/name from the text content
        await this.add_folder(target_folder)
    }

    async on_click__parent_link(event) {
        event.preventDefault()
        const clicked_element = event.target;                           // Get the clicked element (the anchor tag)
        const target_folder = clicked_element.attributes.href.value
        if (target_folder === '/') {
            this.current_path = ''
            this.previous_path = ''
            this.current_folder = ''
        }
        else {
            this.current_path   = this.remove_last_path_element(this.current_path)
            this.previous_path  = this.remove_last_path_element(this.previous_path)
            this.current_folder = this.get_last_path_element   (target_folder     )
        }
        await this.build(target_folder)
    }
    async html(folders) {
        let div_root        = new Div({id:'api_to_table'    })
        let separator_slash = new Span({value:'/'})
        let separator_pipe  = new Span({value:'|'})
        let hr_separator    = new HR()

        div_root.add_element(hr_separator)
        let a_previous_path     = new A({class:'parent-link',  value:this.previous_path, attributes:{href:this.previous_path}})
        let b_current_folder    = new B({value: this.current_folder})
        div_root.add_elements(a_previous_path, b_current_folder)
        div_root.add_element(hr_separator)

        for (let folder of folders) {
            let a_folder_link = new A({class:'folder-link',  value:folder, attributes:{href:folder}})
            div_root.add_elements(separator_pipe, a_folder_link)
        }
        let div_current_paths = new Div({value:`${JSON.stringify(this.current_paths)}`})
        //div_root.add_element(div_current_paths)
        let html = div_root.html()
        return html
    }

    remove_last_path_element(path) {
        let pathElements = path.split('/').filter(element => element !== '');   // Split the path into elements and filter out empty strings
        pathElements.pop();                                                     // Remove the last element from the array
        return pathElements.join('/') + '/';                                    // Join the remaining elements back into a string with '/' and add a trailing '/'
    }
    get_last_path_element(path) {
        let pathElements = path.split('/').filter(element => element !== '');       // Split the path into elements and filter out empty strings
        return pathElements.pop() || ''; // Get the last element from the array or return an empty string if the array is empty
    }
}


WebC__S3_Browser__Server_Requests.define()