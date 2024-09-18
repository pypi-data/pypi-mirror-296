# panora

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=<no value>&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


## 🏗 **Welcome to your new SDK!** 🏗

It has been generated successfully based on your OpenAPI spec. However, it is not yet ready for production use. Here are some next steps:
- [ ] 🛠 Make your SDK feel handcrafted by [customizing it](https://www.speakeasy.com/docs/customize-sdks)
- [ ] ♻️ Refine your SDK quickly by iterating locally with the [Speakeasy CLI](https://github.com/speakeasy-api/speakeasy)
- [ ] 🎁 Publish your SDK to package managers by [configuring automatic publishing](https://www.speakeasy.com/docs/advanced-setup/publish-sdks)
- [ ] ✨ When ready to productionize, delete this section from the README

<!-- Start Summary [summary] -->
## Summary

Panora API: A unified API to ship integrations
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents

* [SDK Installation](#sdk-installation)
* [IDE Support](#ide-support)
* [SDK Example Usage](#sdk-example-usage)
* [Available Resources and Operations](#available-resources-and-operations)
* [Pagination](#pagination)
* [Retries](#retries)
* [Error Handling](#error-handling)
* [Server Selection](#server-selection)
* [Custom HTTP Client](#custom-http-client)
* [Authentication](#authentication)
* [Debugging](#debugging)
<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

PIP
```bash
pip install panora-sdk
```

Poetry
```bash
poetry add panora-sdk
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from panora_sdk import Panora

s = Panora(
    api_key="<YOUR_API_KEY_HERE>",
)


res = s.hello()

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from panora_sdk import Panora

async def main():
    s = Panora(
        api_key="<YOUR_API_KEY_HERE>",
    )
    res = await s.hello_async()
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

### [Panora SDK](docs/sdks/panora/README.md)

* [hello](docs/sdks/panora/README.md#hello)
* [health](docs/sdks/panora/README.md#health)


### [rag.query](docs/sdks/query/README.md)

* [query](docs/sdks/query/README.md#query) - Query using RAG Search


### [filestorage.files](docs/sdks/files/README.md)

* [list](docs/sdks/files/README.md#list) - List  Files
* [create](docs/sdks/files/README.md#create) - Create Files
* [retrieve](docs/sdks/files/README.md#retrieve) - Retrieve Files

### [filestorage.folders](docs/sdks/folders/README.md)

* [list](docs/sdks/folders/README.md#list) - List  Folders
* [create](docs/sdks/folders/README.md#create) - Create Folders
* [retrieve](docs/sdks/folders/README.md#retrieve) - Retrieve Folders

### [filestorage.groups](docs/sdks/panoragroups/README.md)

* [list](docs/sdks/panoragroups/README.md#list) - List  Groups
* [retrieve](docs/sdks/panoragroups/README.md#retrieve) - Retrieve Groups

### [filestorage.users](docs/sdks/panorafilestorageusers/README.md)

* [list](docs/sdks/panorafilestorageusers/README.md#list) - List Users
* [retrieve](docs/sdks/panorafilestorageusers/README.md#retrieve) - Retrieve Users


### [auth.login](docs/sdks/login/README.md)

* [sign_in](docs/sdks/login/README.md#sign_in) - Log In

### [connections](docs/sdks/connections/README.md)

* [list](docs/sdks/connections/README.md#list) - List Connections

### [webhooks](docs/sdks/webhooks/README.md)

* [list](docs/sdks/webhooks/README.md#list) - List webhooks
* [create](docs/sdks/webhooks/README.md#create) - Create webhook
* [delete](docs/sdks/webhooks/README.md#delete) - Delete Webhook
* [update_status](docs/sdks/webhooks/README.md#update_status) - Update webhook status
* [verify_event](docs/sdks/webhooks/README.md#verify_event) - Verify payload signature of the webhook


### [ticketing.tickets](docs/sdks/tickets/README.md)

* [list](docs/sdks/tickets/README.md#list) - List  Tickets
* [create](docs/sdks/tickets/README.md#create) - Create Tickets
* [retrieve](docs/sdks/tickets/README.md#retrieve) - Retrieve Tickets

### [ticketing.users](docs/sdks/users/README.md)

* [list](docs/sdks/users/README.md#list) - List Users
* [retrieve](docs/sdks/users/README.md#retrieve) - Retrieve User

### [ticketing.accounts](docs/sdks/accounts/README.md)

* [list](docs/sdks/accounts/README.md#list) - List  Accounts
* [retrieve](docs/sdks/accounts/README.md#retrieve) - Retrieve Accounts

### [ticketing.contacts](docs/sdks/contacts/README.md)

* [list](docs/sdks/contacts/README.md#list) - List Contacts
* [retrieve](docs/sdks/contacts/README.md#retrieve) - Retrieve Contact

### [ticketing.collections](docs/sdks/collections/README.md)

* [list](docs/sdks/collections/README.md#list) - List Collections
* [retrieve](docs/sdks/collections/README.md#retrieve) - Retrieve Collections

### [ticketing.comments](docs/sdks/comments/README.md)

* [list](docs/sdks/comments/README.md#list) - List Comments
* [create](docs/sdks/comments/README.md#create) - Create Comments
* [retrieve](docs/sdks/comments/README.md#retrieve) - Retrieve Comment

### [ticketing.tags](docs/sdks/tags/README.md)

* [list](docs/sdks/tags/README.md#list) - List Tags
* [retrieve](docs/sdks/tags/README.md#retrieve) - Retrieve Tag

### [ticketing.teams](docs/sdks/teams/README.md)

* [list](docs/sdks/teams/README.md#list) - List  Teams
* [retrieve](docs/sdks/teams/README.md#retrieve) - Retrieve Teams

### [ticketing.attachments](docs/sdks/panoraticketingattachments/README.md)

* [list](docs/sdks/panoraticketingattachments/README.md#list) - List  Attachments
* [create](docs/sdks/panoraticketingattachments/README.md#create) - Create Attachments
* [retrieve](docs/sdks/panoraticketingattachments/README.md#retrieve) - Retrieve Attachments

### [sync](docs/sdks/sync/README.md)

* [status](docs/sdks/sync/README.md#status) - Retrieve sync status of a certain vertical
* [resync](docs/sdks/sync/README.md#resync) - Resync common objects across a vertical
* [update_pull_frequency](docs/sdks/sync/README.md#update_pull_frequency) - Update pull frequency for verticals
* [get_pull_frequency](docs/sdks/sync/README.md#get_pull_frequency) - Get pull frequency for verticals


### [crm.companies](docs/sdks/companies/README.md)

* [list](docs/sdks/companies/README.md#list) - List Companies
* [create](docs/sdks/companies/README.md#create) - Create Companies
* [retrieve](docs/sdks/companies/README.md#retrieve) - Retrieve Companies

### [crm.contacts](docs/sdks/panoracontacts/README.md)

* [list](docs/sdks/panoracontacts/README.md#list) - List CRM Contacts
* [create](docs/sdks/panoracontacts/README.md#create) - Create Contacts
* [retrieve](docs/sdks/panoracontacts/README.md#retrieve) - Retrieve Contacts

### [crm.deals](docs/sdks/deals/README.md)

* [list](docs/sdks/deals/README.md#list) - List Deals
* [create](docs/sdks/deals/README.md#create) - Create Deals
* [retrieve](docs/sdks/deals/README.md#retrieve) - Retrieve Deals

### [crm.engagements](docs/sdks/engagements/README.md)

* [list](docs/sdks/engagements/README.md#list) - List Engagements
* [create](docs/sdks/engagements/README.md#create) - Create Engagements
* [retrieve](docs/sdks/engagements/README.md#retrieve) - Retrieve Engagements

### [crm.notes](docs/sdks/notes/README.md)

* [list](docs/sdks/notes/README.md#list) - List Notes
* [create](docs/sdks/notes/README.md#create) - Create Notes
* [retrieve](docs/sdks/notes/README.md#retrieve) - Retrieve Notes

### [crm.stages](docs/sdks/stages/README.md)

* [list](docs/sdks/stages/README.md#list) - List  Stages
* [retrieve](docs/sdks/stages/README.md#retrieve) - Retrieve Stages

### [crm.tasks](docs/sdks/tasks/README.md)

* [list](docs/sdks/tasks/README.md#list) - List Tasks
* [create](docs/sdks/tasks/README.md#create) - Create Tasks
* [retrieve](docs/sdks/tasks/README.md#retrieve) - Retrieve Tasks

### [crm.users](docs/sdks/panorausers/README.md)

* [list](docs/sdks/panorausers/README.md#list) - List  Users
* [retrieve](docs/sdks/panorausers/README.md#retrieve) - Retrieve Users

### [linked_users](docs/sdks/linkedusers/README.md)

* [create](docs/sdks/linkedusers/README.md#create) - Create Linked Users
* [list](docs/sdks/linkedusers/README.md#list) - List Linked Users
* [import_batch](docs/sdks/linkedusers/README.md#import_batch) - Add Batch Linked Users
* [retrieve](docs/sdks/linkedusers/README.md#retrieve) - Retrieve Linked Users
* [remote_id](docs/sdks/linkedusers/README.md#remote_id) - Retrieve a Linked User From A Remote Id

### [projects](docs/sdks/projects/README.md)

* [get_projects](docs/sdks/projects/README.md#get_projects) - Retrieve projects
* [create](docs/sdks/projects/README.md#create) - Create a project

### [field_mappings](docs/sdks/fieldmappings/README.md)

* [get_field_mapping_values](docs/sdks/fieldmappings/README.md#get_field_mapping_values) - Retrieve field mappings values
* [get_field_mappings_entities](docs/sdks/fieldmappings/README.md#get_field_mappings_entities) - Retrieve field mapping entities
* [get_field_mappings](docs/sdks/fieldmappings/README.md#get_field_mappings) - Retrieve field mappings
* [definitions](docs/sdks/fieldmappings/README.md#definitions) - Define target Field
* [define_custom_field](docs/sdks/fieldmappings/README.md#define_custom_field) - Create Custom Field
* [map](docs/sdks/fieldmappings/README.md#map) - Map Custom Field

### [events](docs/sdks/events/README.md)

* [get_panora_core_events](docs/sdks/events/README.md#get_panora_core_events) - List Events

### [passthrough](docs/sdks/passthrough/README.md)

* [request](docs/sdks/passthrough/README.md#request) - Make a passthrough request

### [passthrough.retryid](docs/sdks/retryid/README.md)

* [get_retried_request_response](docs/sdks/retryid/README.md#get_retried_request_response) - Retrieve response of a failed passthrough request due to rate limits


### [hris.bankinfos](docs/sdks/bankinfos/README.md)

* [list](docs/sdks/bankinfos/README.md#list) - List Bank Info
* [retrieve](docs/sdks/bankinfos/README.md#retrieve) - Retrieve Bank Info

### [hris.benefits](docs/sdks/benefits/README.md)

* [list](docs/sdks/benefits/README.md#list) - List Benefits
* [retrieve](docs/sdks/benefits/README.md#retrieve) - Retrieve Benefit

### [hris.companies](docs/sdks/panoracompanies/README.md)

* [list](docs/sdks/panoracompanies/README.md#list) - List Companies
* [retrieve](docs/sdks/panoracompanies/README.md#retrieve) - Retrieve Company

### [hris.dependents](docs/sdks/dependents/README.md)

* [list](docs/sdks/dependents/README.md#list) - List Dependents
* [retrieve](docs/sdks/dependents/README.md#retrieve) - Retrieve Dependent

### [hris.employeepayrollruns](docs/sdks/employeepayrollruns/README.md)

* [list](docs/sdks/employeepayrollruns/README.md#list) - List Employee Payroll Runs
* [retrieve](docs/sdks/employeepayrollruns/README.md#retrieve) - Retrieve Employee Payroll Run

### [hris.employees](docs/sdks/employees/README.md)

* [list](docs/sdks/employees/README.md#list) - List Employees
* [create](docs/sdks/employees/README.md#create) - Create Employees
* [retrieve](docs/sdks/employees/README.md#retrieve) - Retrieve Employee

### [hris.employerbenefits](docs/sdks/employerbenefits/README.md)

* [list](docs/sdks/employerbenefits/README.md#list) - List Employer Benefits
* [retrieve](docs/sdks/employerbenefits/README.md#retrieve) - Retrieve Employer Benefit

### [hris.employments](docs/sdks/employments/README.md)

* [list](docs/sdks/employments/README.md#list) - List Employments
* [retrieve](docs/sdks/employments/README.md#retrieve) - Retrieve Employment

### [hris.groups](docs/sdks/groups/README.md)

* [list](docs/sdks/groups/README.md#list) - List Groups
* [retrieve](docs/sdks/groups/README.md#retrieve) - Retrieve Group

### [hris.locations](docs/sdks/locations/README.md)

* [list](docs/sdks/locations/README.md#list) - List Locations
* [retrieve](docs/sdks/locations/README.md#retrieve) - Retrieve Location

### [hris.paygroups](docs/sdks/paygroups/README.md)

* [list](docs/sdks/paygroups/README.md#list) - List Pay Groups
* [retrieve](docs/sdks/paygroups/README.md#retrieve) - Retrieve Pay Group

### [hris.payrollruns](docs/sdks/payrollruns/README.md)

* [list](docs/sdks/payrollruns/README.md#list) - List Payroll Runs
* [retrieve](docs/sdks/payrollruns/README.md#retrieve) - Retrieve Payroll Run

### [hris.timeoffs](docs/sdks/timeoffs/README.md)

* [list](docs/sdks/timeoffs/README.md#list) - List Time Offs
* [create](docs/sdks/timeoffs/README.md#create) - Create Timeoffs
* [retrieve](docs/sdks/timeoffs/README.md#retrieve) - Retrieve Time Off

### [hris.timeoffbalances](docs/sdks/timeoffbalances/README.md)

* [list](docs/sdks/timeoffbalances/README.md#list) - List  TimeoffBalances
* [retrieve](docs/sdks/timeoffbalances/README.md#retrieve) - Retrieve Time off Balances

### [hris.timesheetentries](docs/sdks/timesheetentries/README.md)

* [list](docs/sdks/timesheetentries/README.md#list) - List Timesheetentries
* [create](docs/sdks/timesheetentries/README.md#create) - Create Timesheetentrys
* [retrieve](docs/sdks/timesheetentries/README.md#retrieve) - Retrieve Timesheetentry


### [marketingautomation.actions](docs/sdks/actions/README.md)

* [list](docs/sdks/actions/README.md#list) - List Actions
* [create](docs/sdks/actions/README.md#create) - Create Action
* [retrieve](docs/sdks/actions/README.md#retrieve) - Retrieve Actions

### [marketingautomation.automations](docs/sdks/automations/README.md)

* [list](docs/sdks/automations/README.md#list) - List Automations
* [create](docs/sdks/automations/README.md#create) - Create Automation
* [retrieve](docs/sdks/automations/README.md#retrieve) - Retrieve Automation

### [marketingautomation.campaigns](docs/sdks/campaigns/README.md)

* [list](docs/sdks/campaigns/README.md#list) - List Campaigns
* [create](docs/sdks/campaigns/README.md#create) - Create Campaign
* [retrieve](docs/sdks/campaigns/README.md#retrieve) - Retrieve Campaign

### [marketingautomation.contacts](docs/sdks/panoramarketingautomationcontacts/README.md)

* [list](docs/sdks/panoramarketingautomationcontacts/README.md#list) - List  Contacts
* [create](docs/sdks/panoramarketingautomationcontacts/README.md#create) - Create Contact
* [retrieve](docs/sdks/panoramarketingautomationcontacts/README.md#retrieve) - Retrieve Contacts

### [marketingautomation.emails](docs/sdks/emails/README.md)

* [list](docs/sdks/emails/README.md#list) - List Emails
* [retrieve](docs/sdks/emails/README.md#retrieve) - Retrieve Email

### [marketingautomation.events](docs/sdks/panoraevents/README.md)

* [list](docs/sdks/panoraevents/README.md#list) - List Events
* [retrieve](docs/sdks/panoraevents/README.md#retrieve) - Retrieve Event

### [marketingautomation.lists](docs/sdks/lists/README.md)

* [list](docs/sdks/lists/README.md#list) - List Lists
* [create](docs/sdks/lists/README.md#create) - Create Lists
* [retrieve](docs/sdks/lists/README.md#retrieve) - Retrieve List

### [marketingautomation.messages](docs/sdks/messages/README.md)

* [list](docs/sdks/messages/README.md#list) - List Messages
* [retrieve](docs/sdks/messages/README.md#retrieve) - Retrieve Messages

### [marketingautomation.templates](docs/sdks/templates/README.md)

* [list](docs/sdks/templates/README.md#list) - List Templates
* [create](docs/sdks/templates/README.md#create) - Create Template
* [retrieve](docs/sdks/templates/README.md#retrieve) - Retrieve Template

### [marketingautomation.users](docs/sdks/panoramarketingautomationusers/README.md)

* [list](docs/sdks/panoramarketingautomationusers/README.md#list) - List  Users
* [retrieve](docs/sdks/panoramarketingautomationusers/README.md#retrieve) - Retrieve Users


### [ats.activities](docs/sdks/activities/README.md)

* [list](docs/sdks/activities/README.md#list) - List  Activities
* [create](docs/sdks/activities/README.md#create) - Create Activities
* [retrieve](docs/sdks/activities/README.md#retrieve) - Retrieve Activities

### [ats.applications](docs/sdks/applications/README.md)

* [list](docs/sdks/applications/README.md#list) - List  Applications
* [create](docs/sdks/applications/README.md#create) - Create Applications
* [retrieve](docs/sdks/applications/README.md#retrieve) - Retrieve Applications

### [ats.attachments](docs/sdks/attachments/README.md)

* [list](docs/sdks/attachments/README.md#list) - List  Attachments
* [create](docs/sdks/attachments/README.md#create) - Create Attachments
* [retrieve](docs/sdks/attachments/README.md#retrieve) - Retrieve Attachments

### [ats.candidates](docs/sdks/candidates/README.md)

* [list](docs/sdks/candidates/README.md#list) - List  Candidates
* [create](docs/sdks/candidates/README.md#create) - Create Candidates
* [retrieve](docs/sdks/candidates/README.md#retrieve) - Retrieve Candidates

### [ats.departments](docs/sdks/departments/README.md)

* [list](docs/sdks/departments/README.md#list) - List  Departments
* [retrieve](docs/sdks/departments/README.md#retrieve) - Retrieve Departments

### [ats.interviews](docs/sdks/interviews/README.md)

* [list](docs/sdks/interviews/README.md#list) - List  Interviews
* [create](docs/sdks/interviews/README.md#create) - Create Interviews
* [retrieve](docs/sdks/interviews/README.md#retrieve) - Retrieve Interviews

### [ats.jobinterviewstages](docs/sdks/jobinterviewstages/README.md)

* [list](docs/sdks/jobinterviewstages/README.md#list) - List  JobInterviewStages
* [retrieve](docs/sdks/jobinterviewstages/README.md#retrieve) - Retrieve Job Interview Stages

### [ats.jobs](docs/sdks/jobs/README.md)

* [list](docs/sdks/jobs/README.md#list) - List  Jobs
* [retrieve](docs/sdks/jobs/README.md#retrieve) - Retrieve Jobs

### [ats.offers](docs/sdks/offers/README.md)

* [list](docs/sdks/offers/README.md#list) - List  Offers
* [retrieve](docs/sdks/offers/README.md#retrieve) - Retrieve Offers

### [ats.offices](docs/sdks/offices/README.md)

* [list](docs/sdks/offices/README.md#list) - List Offices
* [retrieve](docs/sdks/offices/README.md#retrieve) - Retrieve Offices

### [ats.rejectreasons](docs/sdks/rejectreasons/README.md)

* [list](docs/sdks/rejectreasons/README.md#list) - List  RejectReasons
* [retrieve](docs/sdks/rejectreasons/README.md#retrieve) - Retrieve Reject Reasons

### [ats.scorecards](docs/sdks/scorecards/README.md)

* [list](docs/sdks/scorecards/README.md#list) - List  ScoreCards
* [retrieve](docs/sdks/scorecards/README.md#retrieve) - Retrieve Score Cards

### [ats.tags](docs/sdks/panoratags/README.md)

* [list](docs/sdks/panoratags/README.md#list) - List  Tags
* [retrieve](docs/sdks/panoratags/README.md#retrieve) - Retrieve Tags

### [ats.users](docs/sdks/panoraatsusers/README.md)

* [list](docs/sdks/panoraatsusers/README.md#list) - List  Users
* [retrieve](docs/sdks/panoraatsusers/README.md#retrieve) - Retrieve Users

### [ats.eeocs](docs/sdks/eeocs/README.md)

* [list](docs/sdks/eeocs/README.md#list) - List  Eeocss
* [retrieve](docs/sdks/eeocs/README.md#retrieve) - Retrieve Eeocs


### [accounting.accounts](docs/sdks/panoraaccounts/README.md)

* [list](docs/sdks/panoraaccounts/README.md#list) - List  Accounts
* [create](docs/sdks/panoraaccounts/README.md#create) - Create Accounts
* [retrieve](docs/sdks/panoraaccounts/README.md#retrieve) - Retrieve Accounts

### [accounting.addresses](docs/sdks/addresses/README.md)

* [list](docs/sdks/addresses/README.md#list) - List  Addresss
* [retrieve](docs/sdks/addresses/README.md#retrieve) - Retrieve Addresses

### [accounting.attachments](docs/sdks/panoraattachments/README.md)

* [list](docs/sdks/panoraattachments/README.md#list) - List  Attachments
* [create](docs/sdks/panoraattachments/README.md#create) - Create Attachments
* [retrieve](docs/sdks/panoraattachments/README.md#retrieve) - Retrieve Attachments

### [accounting.balancesheets](docs/sdks/balancesheets/README.md)

* [list](docs/sdks/balancesheets/README.md#list) - List  BalanceSheets
* [retrieve](docs/sdks/balancesheets/README.md#retrieve) - Retrieve BalanceSheets

### [accounting.cashflowstatements](docs/sdks/cashflowstatements/README.md)

* [list](docs/sdks/cashflowstatements/README.md#list) - List  CashflowStatements
* [retrieve](docs/sdks/cashflowstatements/README.md#retrieve) - Retrieve Cashflow Statements

### [accounting.companyinfos](docs/sdks/companyinfos/README.md)

* [list](docs/sdks/companyinfos/README.md#list) - List  CompanyInfos
* [retrieve](docs/sdks/companyinfos/README.md#retrieve) - Retrieve Company Infos

### [accounting.contacts](docs/sdks/panoraaccountingcontacts/README.md)

* [list](docs/sdks/panoraaccountingcontacts/README.md#list) - List  Contacts
* [create](docs/sdks/panoraaccountingcontacts/README.md#create) - Create Contacts
* [retrieve](docs/sdks/panoraaccountingcontacts/README.md#retrieve) - Retrieve Contacts

### [accounting.creditnotes](docs/sdks/creditnotes/README.md)

* [list](docs/sdks/creditnotes/README.md#list) - List  CreditNotes
* [retrieve](docs/sdks/creditnotes/README.md#retrieve) - Retrieve Credit Notes

### [accounting.expenses](docs/sdks/expenses/README.md)

* [list](docs/sdks/expenses/README.md#list) - List  Expenses
* [create](docs/sdks/expenses/README.md#create) - Create Expenses
* [retrieve](docs/sdks/expenses/README.md#retrieve) - Retrieve Expenses

### [accounting.incomestatements](docs/sdks/incomestatements/README.md)

* [list](docs/sdks/incomestatements/README.md#list) - List  IncomeStatements
* [retrieve](docs/sdks/incomestatements/README.md#retrieve) - Retrieve Income Statements

### [accounting.invoices](docs/sdks/invoices/README.md)

* [list](docs/sdks/invoices/README.md#list) - List  Invoices
* [create](docs/sdks/invoices/README.md#create) - Create Invoices
* [retrieve](docs/sdks/invoices/README.md#retrieve) - Retrieve Invoices

### [accounting.items](docs/sdks/items/README.md)

* [list](docs/sdks/items/README.md#list) - List  Items
* [retrieve](docs/sdks/items/README.md#retrieve) - Retrieve Items

### [accounting.journalentries](docs/sdks/journalentries/README.md)

* [list](docs/sdks/journalentries/README.md#list) - List  JournalEntrys
* [create](docs/sdks/journalentries/README.md#create) - Create Journal Entries
* [retrieve](docs/sdks/journalentries/README.md#retrieve) - Retrieve Journal Entries

### [accounting.payments](docs/sdks/payments/README.md)

* [list](docs/sdks/payments/README.md#list) - List  Payments
* [create](docs/sdks/payments/README.md#create) - Create Payments
* [retrieve](docs/sdks/payments/README.md#retrieve) - Retrieve Payments

### [accounting.phonenumbers](docs/sdks/phonenumbers/README.md)

* [list](docs/sdks/phonenumbers/README.md#list) - List  PhoneNumbers
* [retrieve](docs/sdks/phonenumbers/README.md#retrieve) - Retrieve Phone Numbers

### [accounting.purchaseorders](docs/sdks/purchaseorders/README.md)

* [list](docs/sdks/purchaseorders/README.md#list) - List  PurchaseOrders
* [create](docs/sdks/purchaseorders/README.md#create) - Create Purchase Orders
* [retrieve](docs/sdks/purchaseorders/README.md#retrieve) - Retrieve Purchase Orders

### [accounting.taxrates](docs/sdks/taxrates/README.md)

* [list](docs/sdks/taxrates/README.md#list) - List  TaxRates
* [retrieve](docs/sdks/taxrates/README.md#retrieve) - Retrieve Tax Rates

### [accounting.trackingcategories](docs/sdks/trackingcategories/README.md)

* [list](docs/sdks/trackingcategories/README.md#list) - List  TrackingCategorys
* [retrieve](docs/sdks/trackingcategories/README.md#retrieve) - Retrieve Tracking Categories

### [accounting.transactions](docs/sdks/transactions/README.md)

* [list](docs/sdks/transactions/README.md#list) - List  Transactions
* [retrieve](docs/sdks/transactions/README.md#retrieve) - Retrieve Transactions

### [accounting.vendorcredits](docs/sdks/vendorcredits/README.md)

* [list](docs/sdks/vendorcredits/README.md#list) - List  VendorCredits
* [retrieve](docs/sdks/vendorcredits/README.md#retrieve) - Retrieve Vendor Credits


### [ecommerce.products](docs/sdks/products/README.md)

* [list](docs/sdks/products/README.md#list) - List Products
* [create](docs/sdks/products/README.md#create) - Create Products
* [retrieve](docs/sdks/products/README.md#retrieve) - Retrieve Products

### [ecommerce.orders](docs/sdks/orders/README.md)

* [list](docs/sdks/orders/README.md#list) - List Orders
* [create](docs/sdks/orders/README.md#create) - Create Orders
* [retrieve](docs/sdks/orders/README.md#retrieve) - Retrieve Orders

### [ecommerce.customers](docs/sdks/customers/README.md)

* [list](docs/sdks/customers/README.md#list) - List Customers
* [retrieve](docs/sdks/customers/README.md#retrieve) - Retrieve Customers

### [ecommerce.fulfillments](docs/sdks/fulfillments/README.md)

* [list](docs/sdks/fulfillments/README.md#list) - List Fulfillments
* [retrieve](docs/sdks/fulfillments/README.md#retrieve) - Retrieve Fulfillments
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from panora.utils import BackoffStrategy, RetryConfig
from panora_sdk import Panora

s = Panora(
    api_key="<YOUR_API_KEY_HERE>",
)


res = s.hello(,
    RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

if res is not None:
    # handle response
    pass

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from panora.utils import BackoffStrategy, RetryConfig
from panora_sdk import Panora

s = Panora(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key="<YOUR_API_KEY_HERE>",
)


res = s.hello()

if res is not None:
    # handle response
    pass

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations.  All operations return a response object or raise an error.  If Error objects are specified in your OpenAPI Spec, the SDK will raise the appropriate Error type.

| Error Object    | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4xx-5xx         | */*             |

### Example

```python
from panora_sdk import Panora, models

s = Panora(
    api_key="<YOUR_API_KEY_HERE>",
)

res = None
try:
    res = s.hello()

except models.SDKError as e:
    # handle exception
    raise(e)

if res is not None:
    # handle response
    pass

```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| # | Server | Variables |
| - | ------ | --------- |
| 0 | `https://api.panora.dev` | None |
| 1 | `https://api-sandbox.panora.dev` | None |
| 2 | `https://api-dev.panora.dev` | None |

#### Example

```python
from panora_sdk import Panora

s = Panora(
    server_idx=2,
    api_key="<YOUR_API_KEY_HERE>",
)


res = s.hello()

if res is not None:
    # handle response
    pass

```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from panora_sdk import Panora

s = Panora(
    server_url="https://api.panora.dev",
    api_key="<YOUR_API_KEY_HERE>",
)


res = s.hello()

if res is not None:
    # handle response
    pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from panora_sdk import Panora
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Panora(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from panora_sdk import Panora
from panora_sdk.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Panora(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Debugging [debug] -->
## Debugging

To emit debug logs for SDK requests and responses you can pass a logger object directly into your SDK object.

```python
from panora_sdk import Panora
import logging

logging.basicConfig(level=logging.DEBUG)
s = Panora(debug_logger=logging.getLogger("panora_sdk"))
```
<!-- End Debugging [debug] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type      | Scheme    |
| --------- | --------- | --------- |
| `api_key` | apiKey    | API key   |

To authenticate with the API the `null` parameter must be set when initializing the SDK client instance. For example:
```python
from panora_sdk import Panora

s = Panora(
    api_key="<YOUR_API_KEY_HERE>",
)


res = s.hello()

if res is not None:
    # handle response
    pass

```
<!-- End Authentication [security] -->

<!-- Start Pagination [pagination] -->
## Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
```python
from panora_sdk import Panora

s = Panora(
    api_key="<YOUR_API_KEY_HERE>",
)


res = s.filestorage.files.list(x_connection_token="<value>", remote_data=True, limit=10, cursor="1b8b05bb-5273-4012-b520-8657b0b90874")

if res is not None:
    while True:
        # handle items

        res = res.Next()
        if res is None:
            break


```
<!-- End Pagination [pagination] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=<no value>&utm_campaign=python)
