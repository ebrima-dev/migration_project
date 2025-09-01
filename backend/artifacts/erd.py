from graphviz import Digraph

# Initialize ERD diagram
erd = Digraph("LawFirmAccountingERD", format="png")
erd.attr(rankdir="LR", fontsize="10")

# Entities with attributes (simplified to fit diagram)
entities = {
    "Clients": ["client_id (PK)", "client_name", "client_type", "industry", "date_onboarded", "primary_contact"],
    "Matters": ["matter_id (PK)", "client_id (FK)", "matter_name", "practice_area", "responsible_partner", "open_date", "close_date"],
    "Attorneys": ["attorney_id (PK)", "name", "role", "hourly_rate", "hire_date"],
    "TimeEntries": ["entry_id (PK)", "matter_id (FK)", "attorney_id (FK)", "work_date", "hours_worked", "billing_rate", "description"],
    "Invoices": ["invoice_id (PK)", "client_id (FK)", "matter_id (FK)", "invoice_date", "due_date", "total_amount", "status"],
    "InvoiceLines": ["invoice_line_id (PK)", "invoice_id (FK)", "time_entry_id (FK)", "description", "qty", "rate", "line_total"],
    "Payments": ["payment_id (PK)", "invoice_id (FK)", "payment_date", "amount_paid", "payment_method"],
    "ChartOfAccounts": ["account_id (PK)", "account_name", "account_type"],
    "JournalEntries": ["journal_id (PK)", "entry_date", "description", "reference_type", "reference_id"],
    "JournalLines": ["line_id (PK)", "journal_id (FK)", "account_id (FK)", "debit_amount", "credit_amount"]
}

# Add nodes
for entity, fields in entities.items():
    label = f"{entity}|{{" + "|".join(fields) + "}}"
    erd.node(entity, shape="record", label=label)

# Relationships
relationships = [
    ("Clients", "Matters"),
    ("Clients", "Invoices"),
    ("Matters", "TimeEntries"),
    ("Matters", "Invoices"),
    ("Invoices", "InvoiceLines"),
    ("Invoices", "Payments"),
    ("TimeEntries", "InvoiceLines"),
    ("Attorneys", "TimeEntries"),
    ("JournalEntries", "JournalLines"),
    ("ChartOfAccounts", "JournalLines")
]

# Add edges
for parent, child in relationships:
    erd.edge(parent, child)

# Render ERD to file
erd.render("/mnt/data/LawFirmAccountingERD", cleanup=True)

"/mnt/data/LawFirmAccountingERD.png"
