from PyQt5.QtWidgets import QApplication, QInputDialog, QDialog, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton
import sys
from dnac_api import get_auth_token, get_device_detail, get_device_enrichment_details, load_dnac_config

def get_ap_info_dynamically(ap_name):
    # Load DNAC configuration
    dnac_config = load_dnac_config()

    # Get x-auth-token
    token = get_auth_token(dnac_config)

    # Retrieve nwDeviceId using AP name
    nwDeviceId = get_device_detail(ap_name, token, dnac_config)

    # Retrieve AP information using nwDeviceId
    ap_info = get_device_enrichment_details(nwDeviceId, token, dnac_config)

    return ap_info

def get_ap_name():
    # Show input dialog to get AP name
    ap_name, ok = QInputDialog.getText(None, "AP Name Input", "请输入 AP 名称:")

    # Check if input was accepted
    if ok and ap_name:
        return ap_name
    return None

def show_ap_info_dialog(ap_info):
    # Create a QDialog to display AP information
    dialog = QDialog()
    dialog.setWindowTitle("AP 信息")

    # Format AP information for readability
    formatted_info = (
        f"AP 名称: {ap_info['ap_name']}\n"
        f"交换机名称: {ap_info['switch_name']}\n"
        f"交换机 IP: {ap_info['switch_ip']}\n"
        f"连接端口: {ap_info['connect_port']}"
    )

    # Create a QTextEdit widget to display the formatted AP info, with copy capability
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)  # Make it read-only but selectable
    text_edit.setText(formatted_info)

    # Create Next AP and Exit buttons
    next_button = QPushButton("Next AP")
    exit_button = QPushButton("Exit")

    # Connect buttons to actions
    next_button.clicked.connect(dialog.accept)  # Close dialog for the next AP input
    exit_button.clicked.connect(dialog.reject)  # Reject to exit the program

    # Arrange buttons in a horizontal layout
    button_layout = QHBoxLayout()
    button_layout.addWidget(next_button)
    button_layout.addWidget(exit_button)

    # Arrange text and buttons in a vertical layout
    layout = QVBoxLayout()
    layout.addWidget(text_edit)
    layout.addLayout(button_layout)
    dialog.setLayout(layout)

    # Display the dialog and return the result
    return dialog.exec_()

if __name__ == "__main__":
    # Initialize QApplication before any QWidget
    app = QApplication(sys.argv)

    while True:
        ap_name = get_ap_name()  # Prompt user for AP name

        if ap_name:
            try:
                # Fetch AP information dynamically
                ap_info = get_ap_info_dynamically(ap_name)
                # Display AP information in a custom dialog
                result = show_ap_info_dialog(ap_info)
                if result == QDialog.Rejected:  # Exit if the Exit button was clicked
                    break
            except Exception as e:
                # Display error message if retrieval fails
                result = show_ap_info_dialog({"ap_name": "Error", "switch_name": str(e), "switch_ip": "", "connect_port": ""})
                if result == QDialog.Rejected:
                    break
        else:
            print("未输入 AP 名称.")
            break  # Exit if no AP name was entered

    sys.exit(app.exec_())  # Ensure application exits properly
