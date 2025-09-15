#!/bin/bash

# Script to delete directories not in the keep list
# Usage: ./delete_not_used_modules.sh [directory_path]

# Define the list of directories to keep
to_keep_list=("account" "account_cosmetics" "account_edi_ubl_cii" "account_parent" "account_payment" "account_reconcile_model_oca" "account_reconcile_oca" "account_statement_base" "accounting_pdf_reports" "allow_time_off_cancelation_for_officer" "analytic" "app_notifications" "approval_stages" "approvals_for_multiple_things" "attachment_indexation" "attendance_advanced" "auth_signup" "auth_totp" "auth_totp_mail" "auth_totp_portal" "auto_database_backup" "barcodes" "barcodes_gs1_nomenclature" "base" "base_automation" "base_geolocalize" "base_import" "base_import_module" "base_install_request" "base_setup" "base_sparse_field" "base_user_role" "board" "booking_request_payment" "bulma_lib" "bus" "calendar" "calendar_sms" "chatter_rtl" "client_introduction_letter" "construction_updates_wizard" "contacts" "contract_management" "contract_payments_cheques" "contract_unit_change_request" "crm" "crm_sms" "dbfilter_from_header" "delivery" "digest" "dynamic_accounts_report" "employee_appraisal" "event" "event_crm" "event_crm_sale" "event_sale" "event_sms" "finance" "finance_add_remove_unit" "finance_advanced" "finance_replace_plan" "finance_variant" "fix_allocation_number_of_hours_bug" "flow_ai" "gamification" "gamification_sale_crm" "general_visits_booking" "generic_contract" "google_gmail" "google_recaptcha" "helpdesk_cosmatics" "helpdesk_mgmt" "helpdesk_mgmt_project" "helpdesk_rotational" "helpdesk_ticket_configuration" "hide_menu_user" "hr" "hr_advanced" "hr_advanced_validation" "hr_attendance" "hr_batch_payslip_action" "hr_bulk_time_off_cosmetics" "hr_contract" "hr_contract_types" "hr_custom_contract" "hr_employee_transfer" "hr_employee_updation" "hr_expense" "hr_extra_attendance_compensation" "hr_gamification" "hr_holidays" "hr_holidays_attendance" "hr_hourly_cost" "hr_leave_request_aliasing" "hr_multi_company" "hr_org_chart" "hr_payroll_community" "hr_raw_zte_attendance" "hr_recruitment" "hr_recruitment_skills" "hr_recruitment_survey" "hr_reminder" "hr_responsible_field_show" "hr_reward_warning" "hr_skills" "hr_skills_survey" "hr_time_off_cosmetics" "hr_timesheet" "hr_timesheet_attendance" "hr_work_entry" "hr_work_entry_contract" "hr_work_entry_holidays" "http_routing" "iap" "iap_crm" "iap_mail" "image_preview_zoom" "international_phone_widget" "ir_attachment_chatter" "jodit_editor" "js_front_utils" "ks_dashboard_ninja" "link_tracker" "lock_helpdesk_ticket_description_button" "login_as_any_user" "mail" "mail_bot" "mail_bot_hr" "mass_mailing" "mass_mailing_crm" "mass_mailing_event" "mass_mailing_sale" "mass_mailing_themes" "muk_web_appsbar" "muk_web_chatter" "muk_web_colors" "muk_web_dialog" "muk_web_theme" "multi_level_approval" "oca_bank_reconciliation_cosmatics" "odoo_deeplink" "odoo_graphql" "oh_employee_documents_expiry" "ohrms_core" "ohrms_loan" "ohrms_loan_accounting" "ohrms_salary_advance" "om_account_accountant" "om_account_asset" "om_account_bank_statement_import" "om_account_budget" "om_account_daily_reports" "om_account_followup" "om_fiscal_year" "om_recurring_payments" "onboarding" "operations_team" "otp" "owner_app" "owner_chatter" "owner_crm" "owner_group" "owner_news" "owner_profile" "owner_requests" "owner_signup" "owner_units" "owner_visit_invitation" "partner_age" "partner_autocomplete" "partner_statement" "payment" "pdc_account" "pdc_cheque_management" "pdc_real_estate" "phone_validation" "portal" "portal_rating" "privacy_lookup" "product" "project" "project_account" "project_hr_expense" "project_price_breakdown" "project_purchase" "project_sale_expense" "project_sms" "project_timesheet_holidays" "project_todo" "ps_m2m_field_attachment_preview" "purchase" "purchase_stock" "rating" "real_estate_booking" "real_estate_broker" "real_estate_call_center" "real_estate_crm" "real_estate_eoi" "real_estate_helpdesk" "real_estate_helpdesk_visits" "real_estate_inventory" "real_estate_inventory_installments_search" "real_estate_inventory_website_ui" "real_estate_pricelist" "real_estate_quotation" "recursive_views" "remove_units_from_purchase" "report_templates" "report_xlsx" "report_xlsx_helper" "resource" "rfq_validations" "safe_view" "sale" "sale_crm" "sale_expense" "sale_management" "sale_pdf_quote_builder" "sale_product_configurator" "sale_project" "sale_project_stock" "sale_purchase" "sale_purchase_stock" "sale_service" "sale_sms" "sale_stock" "sale_timesheet" "sales_team" "sales_team_leader_restrict_access" "sms" "sms_egypt" "sms_egypt_helpdesk" "snailmail" "snailmail_account" "social_media" "spreadsheet" "spreadsheet_account" "spreadsheet_dashboard" "spreadsheet_dashboard_event_sale" "spreadsheet_dashboard_purchase" "spreadsheet_dashboard_purchase_stock" "spreadsheet_dashboard_stock_account" "stock" "stock_account" "stock_delivery" "stock_sms" "structure_comparison" "survey" "time_off_assistant" "time_off_report_fix" "token_authentication" "unit_follow_report" "uom" "utm" "validation_mixin" "visits_web_form" "web" "web_editor" "web_hierarchy" "web_tour" "web_unsplash" "website" "website_crm" "website_crm_sms" "website_event" "website_event_crm" "website_event_sale" "website_form_project" "website_hr_recruitment" "website_links" "website_mail" "website_mass_mailing" "website_partner" "website_payment" "website_sale" "website_sale_product_configurator" "website_sale_stock" "website_sms" "zaky_integration")
# Function to display usage
usage() {
    echo "Usage: $0 <directory_path>"
    echo "This script deletes all directories in the specified path that are not in the to_keep_list"
    echo "Example: $0 /path/to/modules"
    exit 1
}

# Function to check if directory is in keep list
is_in_keep_list() {
    local dir_name="$1"
    for keep_dir in "${to_keep_list[@]}"; do
        if [[ "$dir_name" == "$keep_dir" ]]; then
            return 0
        fi
    done
    return 1
}


# Ask user for directory path if not provided as argument
if [ $# -eq 0 ]; then
    read -p "Enter the directory path: " target_directory
else
    target_directory="$1"
fi

# Check if the target directory exists
if [ ! -d "$target_directory" ]; then
    echo "Error: Directory '$target_directory' does not exist"
    exit 1
fi

echo "Target directory: $target_directory"
echo "Directories to keep: ${to_keep_list[*]}"
echo ""

# Get list of directories to delete
directories_to_delete=()
deleted_count=0
kept_count=0

echo "Scanning directories..."

# Arrays to store directories for reporting
directories_to_keep=()
directories_skipped=()

# Loop through all directories in the target path
for dir in "$target_directory"/*; do
    if [ -d "$dir" ]; then
        dir_name=$(basename "$dir")
        
        # Check if directory contains both __manifest__.py and __init__.py
        if [ ! -f "$dir/__manifest__.py" ] || [ ! -f "$dir/__init__.py" ]; then
            directories_skipped+=("$dir_name")
            continue
        fi
        
        if is_in_keep_list "$dir_name"; then
            directories_to_keep+=("$dir_name")
            ((kept_count++))
        else
            directories_to_delete+=("$dir")
        fi
    fi
done

echo ""
echo "Summary:"
echo "- Directories to keep: $kept_count"

if [ ${#directories_skipped[@]} -gt 0 ]; then
    echo ""
    echo "Skipped directories (not Odoo modules):"
    for dir_name in "${directories_skipped[@]}"; do
        echo "  ⚠ $dir_name (missing __manifest__.py or __init__.py)"
    done
fi

if [ ${#directories_to_keep[@]} -gt 0 ]; then
    echo ""
    echo "Directories to keep:"
    for dir_name in "${directories_to_keep[@]}"; do
        echo "  ✓ $dir_name"
    done
fi

if [ ${#directories_to_delete[@]} -gt 0 ]; then
    echo ""
    echo "Directories to delete:"
    for dir in "${directories_to_delete[@]}"; do
        echo "  ✗ $(basename "$dir")"
    done
fi

# If there are directories to delete, ask for confirmation
if [ ${#directories_to_delete[@]} -gt 0 ]; then
    echo ""
    echo "WARNING: This will permanently delete the following directories:"
    for dir in "${directories_to_delete[@]}"; do
        echo "  - $(basename "$dir")"
    done
    echo ""
    read -p "Are you sure you want to delete these directories? (y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo ""
        echo "Deleting directories..."
        
        for dir in "${directories_to_delete[@]}"; do
            dir_name=$(basename "$dir")
            echo "Deleting: $dir_name"
            
            if rm -rf "$dir"; then
                echo "✓ Successfully deleted: $dir_name"
                ((deleted_count++))
            else
                echo "✗ Failed to delete: $dir_name"
            fi
        done
        
        echo ""
        echo "Operation completed!"
        echo "- Successfully deleted: $deleted_count directories"
        echo "- Kept: $kept_count directories"
    else
        echo "Operation cancelled by user"
        exit 0
    fi
else
    echo ""
    echo "No directories to delete. All existing directories are in the keep list."
fi

echo ""
echo "Script completed successfully!"
