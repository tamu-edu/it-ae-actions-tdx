# it-ae-actions-servicenow

This composite action is used to modify a TDx request (via an iPaaS flow)

## Example usages


- Close a Request
```yaml
steps:
  - name: Close TDx Request
    uses: tamu-edu/it-ae-actions-tdx@v1.0
    with:
      tdx-base-url: ${{ vars.TDX_BASE_URL }}
      tdx-account-id: ${{ secrets.TDX_ACCOUNT_ID }}
      tdx-secret: ${{ secrets.TDX_SECRET }}
      action-version: v1.0
      tdx-request-id: 111
      tdx-flow-id: 253422cd-fa19-4362-86ef-983fab35eb53
      tdx-action: close_request
      tdx-input1: ""
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

- Update a Request variable called 'resource_url' and close the request:
```yaml
steps:
  - name: Update TDx Request and Close
    uses: tamu-edu/it-ae-actions-tdx@v1.0
    with:
      tdx-base-url: ${{ vars.TDX_BASE_URL }}
      tdx-account-id: ${{ secrets.TDX_ACCOUNT_ID }}
      tdx-secret: ${{ secrets.TDX_SECRET }}
      action-version: v1.0
      tdx-request-id: 112
      tdx-flow-id: 253422cd-fa19-4362-86ef-983fab35eb53
      tdx-action: update_request_variable_and_close_request
      tdx-input1: resource_url
      tdx-input2: http://some.resource.url
      github-token: ${{ secrets.GITHUB_TOKEN }}
```