import streamlit as st
import json
from datetime import datetime

# --- Mock locations list ---
MOCK_LOCATIONS = [
    "Best Friends - Boston",
    "Best Friends - Dallas",
    "Best Friends - Chicago",
    "Best Friends - Miami",
    "Best Friends - LA",
    "Best Friends - New York",
    "Best Friends - Atlanta",
]

# --- Page title ---
st.title("Best Friends Pricing & Offers Intake (Mock)")
st.write("Please fill out all required fields. You can add multiple services per location. This version uses mock data only.")

# --- Section 1: Location Info ---
location_name = st.selectbox("Select your location", MOCK_LOCATIONS)
other_animals = st.multiselect(
    "Do you offer services for any animals other than dogs?",
    ["Cat", "Bird", "Hamster", "Reptile", "Other"]
)

# --- Section 2: Service Entries (Repeatable) ---
st.subheader("Service Entries")
service_entries = []
num_services = st.number_input("How many services would you like to enter?", min_value=1, max_value=20, value=1)
for i in range(int(num_services)):
    with st.expander(f"Service Entry #{i+1}"):
        service = {}
        service["category"] = st.selectbox(f"Service Category #{i+1}", ["Boarding", "Day Camp", "Grooming", "Training", "Other"], key=f"cat_{i}")
        service["description"] = st.text_input(f"Service Description #{i+1}", key=f"desc_{i}")
        service["applies_to"] = st.multiselect(f"Applies to (#{i+1})", ["Dog", "Cat", "Other"], key=f"applies_{i}")
        service["base_price"] = st.number_input(f"Base Price #{i+1}", min_value=0.0, format="%.2f", key=f"price_{i}")
        service["is_package"] = st.radio(f"Is this a Package? #{i+1}", ["Yes", "No"], key=f"pkg_{i}")
        if service["is_package"] == "Yes":
            service["package_qty"] = st.number_input(f"Quantity in Package #{i+1}", min_value=1, key=f"qty_{i}")
            service["expiration_policy"] = st.text_input(f"Expiration Policy #{i+1}", key=f"exp_{i}")
        service["is_bundled"] = st.radio(f"Is it Bundled with Another Service? #{i+1}", ["Yes", "No"], key=f"bundled_{i}")
        if service["is_bundled"] == "Yes":
            service["bundle_desc"] = st.text_input(f"Describe the bundle #{i+1}", key=f"bundle_desc_{i}")
        # Add-ons (conditional)
        service["add_ons"] = []
        if st.checkbox(f"Add Add-ons for Service #{i+1}?", key=f"add_on_chk_{i}"):
            num_addons = st.number_input(f"How many add-ons? (#{i+1})", min_value=1, max_value=10, value=1, key=f"addon_num_{i}")
            for j in range(int(num_addons)):
                with st.expander(f"Add-on #{j+1} for Service #{i+1}"):
                    addon = {}
                    addon["desc"] = st.text_input(f"Add-on Description #{j+1}", key=f"addon_desc_{i}_{j}")
                    addon["price_impact"] = st.text_input(f"Price Impact (flat or %) #{j+1}", key=f"addon_impact_{i}_{j}")
                    addon["conditions"] = st.text_input(f"Conditions #{j+1}", key=f"addon_cond_{i}_{j}")
                    service["add_ons"].append(addon)
        service_entries.append(service)

# --- Section 3: Optional Upload ---
st.subheader("Optional Document Upload")
doc_upload = st.file_uploader("Do you have any pricing or service docs you'd like to attach? (PDF, Excel, etc.)")

# --- Section 4: Final Questions ---
st.subheader("Final Questions")
pricing_scenarios = st.text_area("Do you have pricing for these scenarios? (e.g., Boarding + Exit Groom, Daycare + Training)")
discounts = st.text_area("Do you offer any discounts (multi-dog, recurring packages, etc.)?")
unique_structures = st.text_area("Are there any unique pricing structures or promotions?")

# --- Submission ---
if st.button("Submit"):
    # Validate required fields
    if not location_name or not service_entries:
        st.error("Location and at least one service entry are required.")
    else:
        # Prepare collected data
        intake_data = {
            "location_name": location_name,
            "other_animals": other_animals,
            "submitted_at": datetime.utcnow().isoformat(),
            "service_entries": service_entries,
            "pricing_scenarios": pricing_scenarios,
            "discounts": discounts,
            "unique_structures": unique_structures,
            "doc_upload_name": doc_upload.name if doc_upload else None
        }
        st.success("Submission received! (Mock mode)")
        st.markdown("### Submission Summary (JSON)")
        st.code(json.dumps(intake_data, indent=2), language="json")
        st.download_button(
            label="Download Submission JSON",
            data=json.dumps(intake_data, indent=2),
            file_name="pricing_intake_submission.json",
            mime="application/json"
        )
