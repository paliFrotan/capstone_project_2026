import re

# List of void elements in HTML5
void_elements = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr"
]

# Build a regex pattern to match <tag ... />
pattern = re.compile(
    r"<({})([^>]*)\s*/>".format("|".join(void_elements)), re.IGNORECASE
)

def convert_self_closing_tags(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace <tag ... /> with <tag ...>
    new_content = pattern.sub(r"<\1\2>", content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Converted self-closing tags in {file_path}")

# Example usage:
convert_self_closing_tags("templates/base.html")
#convert_self_closing_tags("templates/wallet/landing.html")
#convert_self_closing_tags("templates/wallet/dashboard.html")
#convert_self_closing_tags("templates/wallet/month_transactions.html")
#convert_self_closing_tags("templates/wallet/print_month_report.html")
#convert_self_closing_tags("templates/wallet/transaction_edit.html")
#convert_self_closing_tags("templates/wallet/transaction_delete.html")
