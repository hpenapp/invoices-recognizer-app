#import libraries
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
from collections import defaultdict

endpoint = ""
key = ""

def analyze_invoice(document, idx):

    items_dict = defaultdict(dict)
    my_dict = defaultdict(dict)
    
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document(
           "prebuilt-invoice", document=document)

    invoices = poller.result()
   
    for invoice in invoices.documents:
        try:
            my_dict[idx+1]['invoice_number'] = idx+1
        except Exception:
            my_dict[idx+1]['invoice_number'] = None
        try:
            my_dict[idx+1]['remittance_address_recipient'] = invoice.fields.get("RemittanceAddressRecipient").value
        except Exception:
            my_dict[idx+1]['remittance_address_recipient'] = None
        try:
            my_dict[idx+1]['remittance_address'] = invoice.fields.get("RemittanceAddress").value
        except Exception:
            my_dict[idx+1]['remittance_address'] = None
        try:
            my_dict[idx+1]['service_address_recipient'] = invoice.fields.get("ServiceAddressRecipient").value
        except Exception:
            my_dict[idx+1]['service_address_recipient'] = None
        try:
            my_dict[idx+1]['service_address'] = invoice.fields.get("ServiceAddress").value
        except Exception:
            my_dict[idx+1]['service_address'] = None
        try:
            my_dict[idx+1]['service_end_date'] = invoice.fields.get("ServiceEndDate").value
        except Exception:
            my_dict[idx+1]['service_end_date'] = None
        try:
            my_dict[idx+1]['service_start_date'] = invoice.fields.get("ServiceStartDate").value
        except Exception:
            my_dict[idx+1]['service_start_date'] = None
        try:
            my_dict[idx+1]['amount_due'] = invoice.fields.get("AmountDue").value.amount
        except Exception:
            my_dict[idx+1]['amount_due'] = None
        try:
            my_dict[idx+1]['previous_unpaid_balance'] = invoice.fields.get("PreviousUnpaidBalance").value.amount
        except Exception:
            my_dict[idx+1]['previous_unpaid_balance'] = None
        try:
            my_dict[idx+1]['total_tax'] = invoice.fields.get("TotalTax").value.amount
        except Exception:
            my_dict[idx+1]['total_tax'] = None
        try:
            my_dict[idx+1]['subtotal'] = invoice.fields.get("SubTotal").value.amount
        except Exception:
            my_dict[idx+1]['subtotal'] = None
        try:
            my_dict[idx+1]['shipping_address_recipient'] = invoice.fields.get("ShippingAddressRecipient").value
        except Exception:
            my_dict[idx+1]['shipping_address_recipient'] = None
        try:
            my_dict[idx+1]['shipping_address'] = invoice.fields.get("ShippingAddress").value
        except Exception:
            my_dict[idx+1]['shipping_address'] = None
        try:
            my_dict[idx+1]['billing_address_recipient'] = invoice.fields.get("BillingAddressRecipient").value
        except Exception:
            my_dict[idx+1]['billing_address_recipient'] = None
        try:
            my_dict[idx+1]['billing_address'] = invoice.fields.get("BillingAddress").value
        except Exception:
            my_dict[idx+1]['billing_address'] = None
        try:
            my_dict[idx+1]['purchase_order'] = invoice.fields.get("PurchaseOrder").value
        except Exception:
            my_dict[idx+1]['purchase_order'] = None
        try:
            my_dict[idx+1]['due_date'] = invoice.fields.get("DueDate").value
        except Exception:
            my_dict[idx+1]['due_date'] = None
        try:
            my_dict[idx+1]['invoice_total'] = invoice.fields.get("InvoiceTotal").value.amount
        except Exception:
            my_dict[idx+1]['invoice_total'] = None
        try:
            my_dict[idx+1]['invoice_date'] = invoice.fields.get("InvoiceDate").value  
        except Exception:
            my_dict[idx+1]['invoice_date'] = None
        try:
            my_dict[idx+1]['invoice_id'] = invoice.fields.get("InvoiceId").value
        except Exception:
            my_dict[idx+1]['invoice_id'] = None
        try:
            my_dict[idx+1]['customer_address_recipient'] = invoice.fields.get("CustomerAddressRecipient").value
        except Exception:
            my_dict[idx+1]['customer_address_recipient'] = None
        try:
            my_dict[idx+1]['customer_address'] = invoice.fields.get("CustomerAddress").value
        except Exception:
            my_dict[idx+1]['customer_address'] = None
        try:
            my_dict[idx+1]['customer_id'] = invoice.fields.get("CustomerId").value
        except Exception:
            my_dict[idx+1]['customer_id'] = None
        try:
            my_dict[idx+1]['customer_name'] = invoice.fields.get("CustomerName").value
        except Exception:
            my_dict[idx+1]['customer_name'] = None
        try:
            my_dict[idx+1]['vendor_address_recipient'] = invoice.fields.get("VendorAddressRecipient").value
        except Exception:
            my_dict[idx+1]['vendor_address_recipient'] = None
        try:
            my_dict[idx+1]['vendor_address'] = invoice.fields.get("VendorAddress").value
        except Exception:
            my_dict[idx+1]['vendor_address'] = None
        try:
            my_dict[idx+1]['vendor_name'] = invoice.fields.get("VendorName").value       
        except Exception:
            my_dict[idx+1]['vendor_name'] = None
        try:
            for jdx, item in enumerate(invoice.fields.get("Items").value):
                items_dict[jdx+1]['invoice_number'] = idx+1
                try: 
                    items_dict[jdx+1]['p_description'] = item.value.get("Description").value  
                except Exception:
                    items_dict[jdx+1]['p_description'] = None
                try:
                    items_dict[jdx+1]['p_quantity'] = item.value.get("Quantity").value  
                except Exception:
                    items_dict[jdx+1]['p_quantity'] = None
                try:
                    items_dict[jdx+1]['p_unit'] = item.value.get("Unit").value  
                except Exception:
                    items_dict[jdx+1]['p_unit'] = None
                try:
                    items_dict[jdx+1]['p_unit_price'] = item.value.get("UnitPrice").value.amount    
                except Exception:
                    items_dict[jdx+1]['p_unit_price'] = None
                try:
                    items_dict[jdx+1]['p_product_code'] = item.value.get("ProductCode").value 
                except Exception:
                    items_dict[jdx+1]['p_product_code'] = None
                try:
                    items_dict[jdx+1]['p_item_date'] = item.value.get("Date").value  
                except Exception:
                    items_dict[jdx+1]['p_item_date'] = None
                try:
                    items_dict[jdx+1]['p_tax'] = item.value.get("TaxRate").value.amount
                except Exception:
                    items_dict[jdx+1]['p_tax'] = None
                try:
                    items_dict[jdx+1]['p_amount'] = item.value.get("Amount").value.amount
                except Exception:
                    items_dict[jdx+1]['p_amount'] = None
        except Exception:
            pass

    general_df = pd.DataFrame(data=dict(my_dict)).T
    items_df = pd.DataFrame(data=dict(items_dict)).T
    idx += 1
    return (idx, general_df, items_df)