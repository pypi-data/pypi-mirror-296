import WebC__S3_Browser__Server_Requests from "../../../js/elements/ui/WebC__S3_Browser__Server_Requests.mjs";
import WebC__Target_Div                  from "../../../js/utils/WebC__Target_Div.mjs";
import WebC__API_To_Json                 from "../../../js/elements/api/WebC__API_To_Json.mjs";
import Web_Component                     from "../../../js/core/Web_Component.mjs";
import API__Invoke                       from "../../../js/data/API__Invoke.mjs";


QUnit.module('WebC__S3_Browser__Server_Requests', function(hooks) {
    let target_div
    let webc_s3_browser_server_requests
    let mock_responses
    let api_path
    let api_data

    hooks.beforeEach(async (assert) => {
        api_path            = '/an/path/to/load'
        mock_responses      = JSON.stringify(api_mock_data())
        //console.log(mock_responses)
        target_div          = WebC__Target_Div.add_to_body().build()
        let attributes      = { mock_responses: mock_responses, api_path: api_path}
        webc_s3_browser_server_requests   = await target_div.append_child(WebC__S3_Browser__Server_Requests, attributes)
        //await webc_s3_browser_server_requests.wait_for_event('build-complete')
    })

    function api_mock_data() {
        let api__list_folders = WebC__S3_Browser__Server_Requests.url__api_list_folders
        return {
                 [api__list_folders                    ]: ["server-requests"],
                 [api__list_folders + "server-requests"]: ["qunit-server", 'another-server'],
                }
    }

    hooks.afterEach(() => {
        webc_s3_browser_server_requests.remove()
        target_div.remove()
    })

    QUnit.test ('.constructor', (assert) => {
        assert.deepEqual(WebC__S3_Browser__Server_Requests.name, 'WebC__S3_Browser__Server_Requests')
        assert.ok(WebC__S3_Browser__Server_Requests.prototype instanceof Web_Component)
        assert.ok(webc_s3_browser_server_requests instanceof Web_Component)
        assert.ok(webc_s3_browser_server_requests instanceof HTMLElement)
        assert.ok(webc_s3_browser_server_requests.api_invoke instanceof API__Invoke)
        assert.deepEqual(webc_s3_browser_server_requests.getAttributeNames(), ['mock_responses', 'api_path'])

        assert.deepEqual(webc_s3_browser_server_requests.api_invoke.mock_responses, JSON.parse(mock_responses))
    })

    QUnit.test ('.api_get_folders', async (assert) => {
        let result = await webc_s3_browser_server_requests.api_get_folders()
        assert.deepEqual(result, ['server-requests'])
    })

    QUnit.test ('.html', async (assert) => {
        const expected_html = '<div id="api_to_table">\n' +
                              '    <hr>\n' +
                              '    \n' +
                              '    <a class="parent-link" href=""></a>\n' +
                              '    <b>/</b>\n' +
                              '    <hr>\n' +
                              '    \n' +
                              '    <span>|</span>\n' +
                              '    <a class="folder-link" href="server-requests">server-requests</a>\n' +
                              '</div>\n' +
                              ''
        assert.deepEqual(webc_s3_browser_server_requests.inner_html(), expected_html)
    })

})

