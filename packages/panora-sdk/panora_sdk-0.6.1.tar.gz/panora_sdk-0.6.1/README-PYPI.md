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

* [SDK Installation](https://github.com/panoratech/python-sdk/blob/master/#sdk-installation)
* [IDE Support](https://github.com/panoratech/python-sdk/blob/master/#ide-support)
* [SDK Example Usage](https://github.com/panoratech/python-sdk/blob/master/#sdk-example-usage)
* [Available Resources and Operations](https://github.com/panoratech/python-sdk/blob/master/#available-resources-and-operations)
* [Pagination](https://github.com/panoratech/python-sdk/blob/master/#pagination)
* [Retries](https://github.com/panoratech/python-sdk/blob/master/#retries)
* [Error Handling](https://github.com/panoratech/python-sdk/blob/master/#error-handling)
* [Server Selection](https://github.com/panoratech/python-sdk/blob/master/#server-selection)
* [Custom HTTP Client](https://github.com/panoratech/python-sdk/blob/master/#custom-http-client)
* [Authentication](https://github.com/panoratech/python-sdk/blob/master/#authentication)
* [Debugging](https://github.com/panoratech/python-sdk/blob/master/#debugging)
<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install panora-sdk
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

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

<details open>
<summary>Available methods</summary>

### [accounting](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/accounting/README.md)


#### [accounting.accounts](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccounts/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccounts/README.md#list) - List  Accounts
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccounts/README.md#create) - Create Accounts
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccounts/README.md#retrieve) - Retrieve Accounts

#### [accounting.addresses](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/addresses/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/addresses/README.md#list) - List  Addresss
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/addresses/README.md#retrieve) - Retrieve Addresses

#### [accounting.attachments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraattachments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraattachments/README.md#list) - List  Attachments
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraattachments/README.md#create) - Create Attachments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraattachments/README.md#retrieve) - Retrieve Attachments

#### [accounting.balancesheets](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/balancesheets/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/balancesheets/README.md#list) - List  BalanceSheets
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/balancesheets/README.md#retrieve) - Retrieve BalanceSheets

#### [accounting.cashflowstatements](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/cashflowstatements/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/cashflowstatements/README.md#list) - List  CashflowStatements
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/cashflowstatements/README.md#retrieve) - Retrieve Cashflow Statements

#### [accounting.companyinfos](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/companyinfos/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/companyinfos/README.md#list) - List  CompanyInfos
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/companyinfos/README.md#retrieve) - Retrieve Company Infos

#### [accounting.contacts](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccountingcontacts/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccountingcontacts/README.md#list) - List  Contacts
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccountingcontacts/README.md#create) - Create Contacts
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraaccountingcontacts/README.md#retrieve) - Retrieve Contacts

#### [accounting.creditnotes](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/creditnotes/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/creditnotes/README.md#list) - List  CreditNotes
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/creditnotes/README.md#retrieve) - Retrieve Credit Notes

#### [accounting.expenses](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/expenses/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/expenses/README.md#list) - List  Expenses
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/expenses/README.md#create) - Create Expenses
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/expenses/README.md#retrieve) - Retrieve Expenses

#### [accounting.incomestatements](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/incomestatements/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/incomestatements/README.md#list) - List  IncomeStatements
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/incomestatements/README.md#retrieve) - Retrieve Income Statements

#### [accounting.invoices](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/invoices/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/invoices/README.md#list) - List  Invoices
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/invoices/README.md#create) - Create Invoices
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/invoices/README.md#retrieve) - Retrieve Invoices

#### [accounting.items](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/items/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/items/README.md#list) - List  Items
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/items/README.md#retrieve) - Retrieve Items

#### [accounting.journalentries](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/journalentries/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/journalentries/README.md#list) - List  JournalEntrys
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/journalentries/README.md#create) - Create Journal Entries
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/journalentries/README.md#retrieve) - Retrieve Journal Entries

#### [accounting.payments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/payments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/payments/README.md#list) - List  Payments
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/payments/README.md#create) - Create Payments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/payments/README.md#retrieve) - Retrieve Payments

#### [accounting.phonenumbers](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/phonenumbers/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/phonenumbers/README.md#list) - List  PhoneNumbers
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/phonenumbers/README.md#retrieve) - Retrieve Phone Numbers

#### [accounting.purchaseorders](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/purchaseorders/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/purchaseorders/README.md#list) - List  PurchaseOrders
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/purchaseorders/README.md#create) - Create Purchase Orders
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/purchaseorders/README.md#retrieve) - Retrieve Purchase Orders

#### [accounting.taxrates](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/taxrates/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/taxrates/README.md#list) - List  TaxRates
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/taxrates/README.md#retrieve) - Retrieve Tax Rates

#### [accounting.trackingcategories](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/trackingcategories/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/trackingcategories/README.md#list) - List  TrackingCategorys
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/trackingcategories/README.md#retrieve) - Retrieve Tracking Categories

#### [accounting.transactions](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/transactions/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/transactions/README.md#list) - List  Transactions
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/transactions/README.md#retrieve) - Retrieve Transactions

#### [accounting.vendorcredits](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/vendorcredits/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/vendorcredits/README.md#list) - List  VendorCredits
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/vendorcredits/README.md#retrieve) - Retrieve Vendor Credits

### [ats](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/ats/README.md)


#### [ats.activities](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/activities/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/activities/README.md#list) - List  Activities
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/activities/README.md#create) - Create Activities
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/activities/README.md#retrieve) - Retrieve Activities

#### [ats.applications](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/applications/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/applications/README.md#list) - List  Applications
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/applications/README.md#create) - Create Applications
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/applications/README.md#retrieve) - Retrieve Applications

#### [ats.attachments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/attachments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/attachments/README.md#list) - List  Attachments
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/attachments/README.md#create) - Create Attachments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/attachments/README.md#retrieve) - Retrieve Attachments

#### [ats.candidates](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/candidates/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/candidates/README.md#list) - List  Candidates
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/candidates/README.md#create) - Create Candidates
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/candidates/README.md#retrieve) - Retrieve Candidates

#### [ats.departments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/departments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/departments/README.md#list) - List  Departments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/departments/README.md#retrieve) - Retrieve Departments

#### [ats.eeocs](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/eeocs/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/eeocs/README.md#list) - List  Eeocss
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/eeocs/README.md#retrieve) - Retrieve Eeocs

#### [ats.interviews](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/interviews/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/interviews/README.md#list) - List  Interviews
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/interviews/README.md#create) - Create Interviews
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/interviews/README.md#retrieve) - Retrieve Interviews

#### [ats.jobinterviewstages](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/jobinterviewstages/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/jobinterviewstages/README.md#list) - List  JobInterviewStages
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/jobinterviewstages/README.md#retrieve) - Retrieve Job Interview Stages

#### [ats.jobs](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/jobs/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/jobs/README.md#list) - List  Jobs
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/jobs/README.md#retrieve) - Retrieve Jobs

#### [ats.offers](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/offers/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/offers/README.md#list) - List  Offers
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/offers/README.md#retrieve) - Retrieve Offers

#### [ats.offices](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/offices/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/offices/README.md#list) - List Offices
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/offices/README.md#retrieve) - Retrieve Offices

#### [ats.rejectreasons](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/rejectreasons/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/rejectreasons/README.md#list) - List  RejectReasons
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/rejectreasons/README.md#retrieve) - Retrieve Reject Reasons

#### [ats.scorecards](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/scorecards/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/scorecards/README.md#list) - List  ScoreCards
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/scorecards/README.md#retrieve) - Retrieve Score Cards

#### [ats.tags](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoratags/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoratags/README.md#list) - List  Tags
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoratags/README.md#retrieve) - Retrieve Tags

#### [ats.users](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraatsusers/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraatsusers/README.md#list) - List  Users
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraatsusers/README.md#retrieve) - Retrieve Users

### [auth](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/auth/README.md)


#### [auth.login](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/login/README.md)

* [sign_in](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/login/README.md#sign_in) - Log In

### [connections](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/connections/README.md)

* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/connections/README.md#retrieve) - List Connections

### [crm](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/crm/README.md)


#### [crm.companies](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/companies/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/companies/README.md#list) - List Companies
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/companies/README.md#create) - Create Companies
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/companies/README.md#retrieve) - Retrieve Companies

#### [crm.contacts](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoracontacts/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoracontacts/README.md#list) - List CRM Contacts
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoracontacts/README.md#create) - Create Contacts
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoracontacts/README.md#retrieve) - Retrieve Contacts

#### [crm.deals](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/deals/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/deals/README.md#list) - List Deals
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/deals/README.md#create) - Create Deals
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/deals/README.md#retrieve) - Retrieve Deals

#### [crm.engagements](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/engagements/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/engagements/README.md#list) - List Engagements
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/engagements/README.md#create) - Create Engagements
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/engagements/README.md#retrieve) - Retrieve Engagements

#### [crm.notes](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/notes/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/notes/README.md#list) - List Notes
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/notes/README.md#create) - Create Notes
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/notes/README.md#retrieve) - Retrieve Notes

#### [crm.stages](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/stages/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/stages/README.md#list) - List  Stages
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/stages/README.md#retrieve) - Retrieve Stages

#### [crm.tasks](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tasks/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tasks/README.md#list) - List Tasks
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tasks/README.md#create) - Create Tasks
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tasks/README.md#retrieve) - Retrieve Tasks

#### [crm.users](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panorausers/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panorausers/README.md#list) - List  Users
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panorausers/README.md#retrieve) - Retrieve Users

### [ecommerce](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/ecommerce/README.md)


#### [ecommerce.customers](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/customers/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/customers/README.md#list) - List Customers
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/customers/README.md#retrieve) - Retrieve Customers

#### [ecommerce.fulfillments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fulfillments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fulfillments/README.md#list) - List Fulfillments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fulfillments/README.md#retrieve) - Retrieve Fulfillments

#### [ecommerce.orders](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/orders/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/orders/README.md#list) - List Orders
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/orders/README.md#create) - Create Orders
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/orders/README.md#retrieve) - Retrieve Orders

#### [ecommerce.products](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/products/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/products/README.md#list) - List Products
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/products/README.md#create) - Create Products
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/products/README.md#retrieve) - Retrieve Products

### [events](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/events/README.md)

* [get_panora_core_events](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/events/README.md#get_panora_core_events) - List Events

### [field_mappings](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fieldmappings/README.md)

* [get_field_mapping_values](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fieldmappings/README.md#get_field_mapping_values) - Retrieve field mappings values
* [get_field_mappings_entities](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fieldmappings/README.md#get_field_mappings_entities) - Retrieve field mapping entities
* [get_field_mappings](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fieldmappings/README.md#get_field_mappings) - Retrieve field mappings
* [definitions](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fieldmappings/README.md#definitions) - Define target Field
* [define_custom_field](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fieldmappings/README.md#define_custom_field) - Create Custom Field
* [map](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/fieldmappings/README.md#map) - Map Custom Field

### [filestorage](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/filestorage/README.md)


#### [filestorage.files](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/files/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/files/README.md#list) - List  Files
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/files/README.md#create) - Create Files
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/files/README.md#retrieve) - Retrieve Files

#### [filestorage.folders](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/folders/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/folders/README.md#list) - List  Folders
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/folders/README.md#create) - Create Folders
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/folders/README.md#retrieve) - Retrieve Folders

#### [filestorage.groups](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoragroups/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoragroups/README.md#list) - List  Groups
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoragroups/README.md#retrieve) - Retrieve Groups

#### [filestorage.users](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panorafilestorageusers/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panorafilestorageusers/README.md#list) - List Users
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panorafilestorageusers/README.md#retrieve) - Retrieve Users

### [hris](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/hris/README.md)


#### [hris.bankinfos](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/bankinfos/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/bankinfos/README.md#list) - List Bank Info
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/bankinfos/README.md#retrieve) - Retrieve Bank Info

#### [hris.benefits](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/benefits/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/benefits/README.md#list) - List Benefits
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/benefits/README.md#retrieve) - Retrieve Benefit

#### [hris.companies](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoracompanies/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoracompanies/README.md#list) - List Companies
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoracompanies/README.md#retrieve) - Retrieve Company

#### [hris.dependents](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/dependents/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/dependents/README.md#list) - List Dependents
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/dependents/README.md#retrieve) - Retrieve Dependent

#### [hris.employeepayrollruns](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employeepayrollruns/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employeepayrollruns/README.md#list) - List Employee Payroll Runs
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employeepayrollruns/README.md#retrieve) - Retrieve Employee Payroll Run

#### [hris.employees](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employees/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employees/README.md#list) - List Employees
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employees/README.md#create) - Create Employees
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employees/README.md#retrieve) - Retrieve Employee

#### [hris.employerbenefits](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employerbenefits/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employerbenefits/README.md#list) - List Employer Benefits
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employerbenefits/README.md#retrieve) - Retrieve Employer Benefit

#### [hris.employments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employments/README.md#list) - List Employments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/employments/README.md#retrieve) - Retrieve Employment

#### [hris.groups](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/groups/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/groups/README.md#list) - List Groups
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/groups/README.md#retrieve) - Retrieve Group

#### [hris.locations](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/locations/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/locations/README.md#list) - List Locations
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/locations/README.md#retrieve) - Retrieve Location

#### [hris.paygroups](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/paygroups/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/paygroups/README.md#list) - List Pay Groups
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/paygroups/README.md#retrieve) - Retrieve Pay Group

#### [hris.payrollruns](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/payrollruns/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/payrollruns/README.md#list) - List Payroll Runs
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/payrollruns/README.md#retrieve) - Retrieve Payroll Run

#### [hris.timeoffbalances](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timeoffbalances/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timeoffbalances/README.md#list) - List  TimeoffBalances
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timeoffbalances/README.md#retrieve) - Retrieve Time off Balances

#### [hris.timeoffs](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timeoffs/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timeoffs/README.md#list) - List Time Offs
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timeoffs/README.md#create) - Create Timeoffs
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timeoffs/README.md#retrieve) - Retrieve Time Off

#### [hris.timesheetentries](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timesheetentries/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timesheetentries/README.md#list) - List Timesheetentries
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timesheetentries/README.md#create) - Create Timesheetentrys
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/timesheetentries/README.md#retrieve) - Retrieve Timesheetentry

### [linked_users](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/linkedusers/README.md)

* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/linkedusers/README.md#create) - Create Linked Users
* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/linkedusers/README.md#list) - List Linked Users
* [import_batch](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/linkedusers/README.md#import_batch) - Add Batch Linked Users
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/linkedusers/README.md#retrieve) - Retrieve Linked Users
* [remote_id](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/linkedusers/README.md#remote_id) - Retrieve a Linked User From A Remote Id

### [marketingautomation](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/marketingautomation/README.md)


#### [marketingautomation.actions](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/actions/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/actions/README.md#list) - List Actions
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/actions/README.md#create) - Create Action
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/actions/README.md#retrieve) - Retrieve Actions

#### [marketingautomation.automations](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/automations/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/automations/README.md#list) - List Automations
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/automations/README.md#create) - Create Automation
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/automations/README.md#retrieve) - Retrieve Automation

#### [marketingautomation.campaigns](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/campaigns/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/campaigns/README.md#list) - List Campaigns
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/campaigns/README.md#create) - Create Campaign
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/campaigns/README.md#retrieve) - Retrieve Campaign

#### [marketingautomation.contacts](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoramarketingautomationcontacts/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoramarketingautomationcontacts/README.md#list) - List  Contacts
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoramarketingautomationcontacts/README.md#create) - Create Contact
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoramarketingautomationcontacts/README.md#retrieve) - Retrieve Contacts

#### [marketingautomation.emails](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/emails/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/emails/README.md#list) - List Emails
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/emails/README.md#retrieve) - Retrieve Email

#### [marketingautomation.events](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraevents/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraevents/README.md#list) - List Events
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraevents/README.md#retrieve) - Retrieve Event

#### [marketingautomation.lists](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/lists/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/lists/README.md#list) - List Lists
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/lists/README.md#create) - Create Lists
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/lists/README.md#retrieve) - Retrieve List

#### [marketingautomation.messages](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/messages/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/messages/README.md#list) - List Messages
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/messages/README.md#retrieve) - Retrieve Messages

#### [marketingautomation.templates](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/templates/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/templates/README.md#list) - List Templates
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/templates/README.md#create) - Create Template
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/templates/README.md#retrieve) - Retrieve Template

#### [marketingautomation.users](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoramarketingautomationusers/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoramarketingautomationusers/README.md#list) - List  Users
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoramarketingautomationusers/README.md#retrieve) - Retrieve Users

### [Panora SDK](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panora/README.md)

* [hello](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panora/README.md#hello)
* [health](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panora/README.md#health)

### [passthrough](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/passthrough/README.md)

* [request](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/passthrough/README.md#request) - Make a passthrough request

#### [passthrough.retryid](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/retryid/README.md)

* [get_retried_request_response](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/retryid/README.md#get_retried_request_response) - Retrieve response of a failed passthrough request due to rate limits

### [projects](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/projects/README.md)

* [get_projects](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/projects/README.md#get_projects) - Retrieve projects
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/projects/README.md#create) - Create a project

### [rag](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/rag/README.md)


#### [rag.query](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/query/README.md)

* [rag_controller_query_embeddings](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/query/README.md#rag_controller_query_embeddings)

### [sync](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/sync/README.md)

* [status](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/sync/README.md#status) - Retrieve sync status of a certain vertical
* [resync](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/sync/README.md#resync) - Resync common objects across a vertical
* [update_pull_frequency](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/sync/README.md#update_pull_frequency) - Update pull frequency for verticals
* [get_pull_frequency](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/sync/README.md#get_pull_frequency) - Get pull frequency for verticals

### [ticketing](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/ticketing/README.md)


#### [ticketing.accounts](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/accounts/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/accounts/README.md#list) - List  Accounts
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/accounts/README.md#retrieve) - Retrieve Accounts

#### [ticketing.attachments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraticketingattachments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraticketingattachments/README.md#list) - List  Attachments
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraticketingattachments/README.md#create) - Create Attachments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/panoraticketingattachments/README.md#retrieve) - Retrieve Attachments

#### [ticketing.collections](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/collections/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/collections/README.md#list) - List Collections
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/collections/README.md#retrieve) - Retrieve Collections

#### [ticketing.comments](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/comments/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/comments/README.md#list) - List Comments
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/comments/README.md#create) - Create Comments
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/comments/README.md#retrieve) - Retrieve Comment

#### [ticketing.contacts](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/contacts/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/contacts/README.md#list) - List Contacts
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/contacts/README.md#retrieve) - Retrieve Contact

#### [ticketing.tags](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tags/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tags/README.md#list) - List Tags
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tags/README.md#retrieve) - Retrieve Tag

#### [ticketing.teams](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/teams/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/teams/README.md#list) - List  Teams
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/teams/README.md#retrieve) - Retrieve Teams

#### [ticketing.tickets](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tickets/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tickets/README.md#list) - List  Tickets
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tickets/README.md#create) - Create Tickets
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/tickets/README.md#retrieve) - Retrieve Tickets

#### [ticketing.users](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/users/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/users/README.md#list) - List Users
* [retrieve](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/users/README.md#retrieve) - Retrieve User

### [webhooks](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/webhooks/README.md)

* [list](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/webhooks/README.md#list) - List webhooks
* [create](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/webhooks/README.md#create) - Create webhook
* [delete](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/webhooks/README.md#delete) - Delete Webhook
* [update_status](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/webhooks/README.md#update_status) - Update webhook status
* [verify_event](https://github.com/panoratech/python-sdk/blob/master/docs/sdks/webhooks/README.md#verify_event) - Verify payload signature of the webhook

</details>
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

    if res is not None:
        # handle response
        pass

except models.SDKError as e:
    # handle exception
    raise(e)
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

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
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

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
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

        res = res.next()
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
