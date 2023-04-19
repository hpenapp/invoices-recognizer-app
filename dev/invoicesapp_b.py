#Import constants.py
import sys
sys.path.insert(0, '../')
import constants
#import libraries
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from collections import defaultdict
import pandas as pd

#Create lists of fields
inv_fields = ["RemittanceAddressRecipient", "RemittanceAddress", "ServiceAddressRecipient",
        "ServiceAddress", "ServiceEndDate", "ServiceStartDate", "ShippingAddressRecipient",
        "ShippingAddress", "BillingAddressRecipient", "BillingAddress", "PurchaseOrder",
        "DueDate", "InvoiceDate", "InvoiceId", "CustomerAddressRecipient", "CustomerAddress",
        "CustomerId", "CustomerName", "VendorAddressRecipient", "VendorAddress", "VendorName"]
invAmount_fields = ["AmountDue", "PreviousUnpaidBalance", "TotalTax", "SubTotal", "InvoiceTotal"]
items_fields = ["Description", "Quantity", "Unit", "ProductCode","Date"]
itAmount_fields = ["UnitPrice", "TaxRate", "Amount"]

def analyze_invoice(document, idx):

    items_dict = defaultdict(dict)
    my_dict = defaultdict(dict)
    
    document_analysis_client = DocumentAnalysisClient(
        endpoint=constants.AZURE_ENDPOINT, credential=AzureKeyCredential(constants.AZURE_KEY)
    )

    poller = document_analysis_client.begin_analyze_document(
           "prebuilt-invoice", document=document)

    invoices = poller.result()
   
    for invoice in invoices.documents:
        my_dict[idx+1]['invoice_number'] = idx+1
        for field in inv_fields:
            try:
                my_dict[idx+1][field] = invoice.fields.get(field).value
            except Exception:
                my_dict[idx+1][field] = None
        for field in invAmount_fields:
            try:
                my_dict[idx+1][field] = invoice.fields.get(field).value.amount
            except Exception:
                my_dict[idx+1][field] = None

        for jdx, item in enumerate(invoice.fields.get("Items").value):
                items_dict[jdx+1]['invoice_number'] = idx+1
                for field in items_fields:
                    try: 
                        items_dict[jdx+1]['p_'+ field] = item.value.get(field).value  
                    except Exception:
                        items_dict[jdx+1]['p_'+ field] = None
                for field in itAmount_fields:
                    try:
                        items_dict[jdx+1]['p_'+ field] = item.value.get(field).value.amount  
                    except Exception:
                        items_dict[jdx+1]['p_'+ field] = None

    # general_df = pd.DataFrame(data=dict(my_dict)).T
    # items_df = pd.DataFrame(data=dict(items_dict)).T
    # idx += 1
    return (idx+1, pd.DataFrame(data=dict(my_dict)).T, pd.DataFrame(data=dict(items_dict)).T)