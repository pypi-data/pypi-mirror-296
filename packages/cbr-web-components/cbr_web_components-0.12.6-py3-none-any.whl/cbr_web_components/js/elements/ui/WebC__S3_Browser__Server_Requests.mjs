import Web_Component from "../../core/Web_Component.mjs";
import API__Invoke   from "../../data/API__Invoke.mjs";
import A             from "../../core/A.mjs";
import B             from "../../core/B.mjs";
import BR            from "../../core/BR.mjs";
import Div           from "../../core/Div.mjs";
import HR            from "../../core/HR.mjs";
import Span          from "../../core/Span.mjs";
import Tag           from "../../core/Tag.mjs";
import Table from "../../core/Table.mjs";


export default class WebC__S3_Browser__Server_Requests extends Web_Component {

    static url__api_list_file_contents   = "/api/server/requests-in-s3/file_contents?file_path="
    static url__api_list_files           = "/api/server/requests-in-s3/list-files?parent_folder="
    static url__api_list_files_metadata  = "/api/server/requests-in-s3/list-files-metadata?parent_folder="
    static url__api_list_folders         = "/api/server/requests-in-s3/list-folders?parent_folder="


    constructor() {
        super();
    }

    async connectedCallback() {
        super.connectedCallback()
        this.setup()
        await this.build()
        this.raise_event('build-complete')
        //setTimeout(this.simulate_click,500)
    }

    // simulate_click = () => {
    //     const folder_link = this.shadowRoot.querySelector(".folder-link");
    //     folder_link.click()
    // }

    setup() {
        this.api_invoke  = new API__Invoke()
        this.api_invoke.mock_responses = JSON.parse(this.getAttribute('mock_responses'))
        this.current_paths = []
        this.current_folder = '/'
        this.current_path   = ''
        this.previous_path  = ''
        this.target_path   = ''

        // this.current_folder = 'list-folders'
        // this.current_path   = 'server-requests/cbr-website-dev-local/2024-09-16/00/api/server/requests-in-s3/list-folders'
        // this.previous_path  = 'server-requests/cbr-website-dev-local/2024-09-16/00/api/server/requests-in-s3'
        // this.target_path    = 'server-requests/cbr-website-dev-local/2024-09-15/23/api/server/requests-in-s3/list-folders'
    }

    async api_get_files(parent_folder) {
        const api_path = WebC__S3_Browser__Server_Requests.url__api_list_files + (parent_folder || '')
        const method   = 'GET'
        const data     = null
        return await this.api_invoke.invoke_api(api_path, method, data)
    }

    async api_get_files_metadata(parent_folder) {
        const api_path = WebC__S3_Browser__Server_Requests.url__api_list_files_metadata + (parent_folder || '')
        const method   = 'GET'
        const data     = null
        return await this.api_invoke.invoke_api(api_path, method, data)
    }

    async api_get_folders(parent_folder) {
        const api_path = WebC__S3_Browser__Server_Requests.url__api_list_folders + (parent_folder || '')
        const method   = 'GET'
        const data     = null
        return await this.api_invoke.invoke_api(api_path, method, data)
    }

    async build() {
        let folders        = await this.api_get_folders(this.target_path)
        //
        // let files          = await this.api_get_files  (this.target_path)
        let files_metadata = await this.api_get_files_metadata  (this.target_path)
        let raw_html       = await this.html(folders, files_metadata)
        this.set_inner_html(raw_html)
        this.set_event_listeners()
    }

    set_event_listeners() {
        const file_links   = this.shadowRoot.querySelectorAll(".file-link"  );
        const folder_links = this.shadowRoot.querySelectorAll(".folder-link");
        const parent_link  = this.shadowRoot.querySelector   (".parent-link");
        const reload_link  = this.shadowRoot.querySelector   (".reload-link");

        parent_link.addEventListener('click', this.on_click__parent_link.bind(this));
        reload_link.addEventListener('click', this.on_click__reload_link.bind(this));

        file_links  .forEach(link => { link.addEventListener('click', this.on_click__file_link  .bind(this)); });
        folder_links.forEach(link => { link.addEventListener('click', this.on_click__folder_link.bind(this)); });

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
        this.target_path = this.current_path
        await this.build()
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
        this.target_path = target_folder
        await this.build()
    }

    async on_click__reload_link(event) {
        event.preventDefault()
        await this.build()
    }

    async on_click__file_link(event) {
        event.preventDefault()
        console.log('on on_click__file_link')
    }


    async html(folders, files_metadata) {
        console.log(files_metadata)
        let files_text          = `Files: ${files_metadata.file_count} in ${files_metadata.duration.seconds} secs`
        let div_root            = new Div({id:'api_to_table'    })
        let separator_pipe      = new Span({value:'|'})
        let hr_separator        = new HR()

        let span_text_path      = new Span({ value: 'Path:'    })
        let span_text_folders   = new Span({ value: 'Folders:' })
        let span_text_files     = new Span({ value: files_text })
        let a_reload            = new A({class:'reload-link',  value:'reload', attributes:{href: '#'}})
        let a_previous_path     = new A({class:'parent-link',  value:this.previous_path, attributes:{href:this.previous_path}})
        let b_current_folder    = new B({value: this.current_folder})

        div_root.add_elements(a_reload, hr_separator)
        div_root.add_elements(span_text_path, a_previous_path, b_current_folder)
        div_root.add_elements(hr_separator, span_text_folders)

        for (let folder of folders) {
            let a_folder_link = new A({class:'folder-link',  value:folder, attributes:{href:folder}})
            div_root.add_elements(a_folder_link, separator_pipe)
        }
        div_root.add_element(hr_separator)
        let table_rows    = []
        let table_headers = ['req id', 'method', 'path','duration', 'status_code','time']

        for (let file_metadata of files_metadata.files_metadata) {
            const metadata      = file_metadata.metadata
            let file_name       = file_metadata.file_name
            let file_name_short = file_name.substring(0,5)
            let a_file     = new A({class:'file-link',  value:file_name_short, attributes:{href:file_name}})
            const table_row = [a_file.html(),
                               metadata.method       ,
                               metadata.request_path ,
                               metadata.duration     ,
                               metadata.status_code  ,
                               metadata.time         ]
            table_rows.push(table_row)
        }

        let table    = new Table()
            table.headers = table_headers
            table.rows    = table_rows
        div_root.add_elements(span_text_files, hr_separator, table)

        let html = div_root.html()

        this.add_css_rules(table.table_css__simple())
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