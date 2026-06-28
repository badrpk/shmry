
# Patch: Handle restricted commodity queries
handle_restricted_items() {
    local query_input=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    if [[ "$query_input" =~ "black label" ]] || [[ "$query_input" =~ "alcohol" ]]; then
        echo -e "\n[SYSTEM ALERT]: Request falls outside of authorized inventory scope (Rangoons) and involves restricted commodities.\nAction: Query terminated.\n"
        return 0
    fi
    return 1
}
