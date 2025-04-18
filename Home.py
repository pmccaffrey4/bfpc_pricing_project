import streamlit as st

st.set_page_config(page_title="Best Friends Pet Care Center Pricing Portal", layout="wide")
st.image("bf_logo.png", width=120)
st.title("Best Friends Pet Care Center Pricing Portal")

st.markdown("""
## Project Overview

Welcome to the Best Friends Pet Care Center Pricing Portal!  
This interactive web application is designed to standardize, collect, and review pricing for all pet care services across our locations. By using this tool, District Managers and Center Managers can easily input, update, and review pricing for Boarding and Day Camp services, ensuring consistency and transparency across our network.

**Why are we doing this?**  
- To streamline the process of collecting and managing service pricing.
- To provide a single source of truth for all center pricing data.
- To enable quick updates and reduce manual errors.
- To empower managers to review and compare offerings.

---

## How to Use This App

### 1. Select Your Center
At the top of each page, select your **District Manager** and **Center Name** from the dropdown menus.  
*Your selection will persist as you navigate between pages.*

---

### 2. Fill Out Each Pricing Page

#### A. Boarding Pricing
- **Daily Rates & Suite Options:**  
  Enter the daily rates for each type of boarding suite (e.g., Standard, Deluxe, Luxury).
- **Add-Ons:**  
  Include any additional services (e.g., extra walks, grooming).
- **Packages:**  
  If you offer multi-day or bundled packages, enter details and pricing.

**Example:**  
- Standard Suite: $45/night  
- Deluxe Suite: $60/night  
- Add-On: Extra Walk $10  
- 5-Night Package: $200 (with 1 free bath)

#### B. Day Camp Pricing
- **Daily Options:**  
  Enter prices for Daily Drop-In, Half-Day, and Weekends.
- **Daycamp Packages:**  
  Add packages (e.g., 10 days for $100, 30-day expiration).

**Example:**  
- Daily Drop-In: $28  
- Half-Day: $14  
- Weekends: $14  
- 10-Day Package: $100, 30-day expiration

---

### 3. Review & Submit
- After entering your data, review the summary cards at the bottom of each page.
- You may update your entries at any time; changes are saved automatically for your session.
- If you need to make changes for another center, simply select a different District Manager or Center Name.

---

## Tips & Best Practices
- Double-check all rates and package details before moving to the next page.
- Use clear expiration policies (e.g., “30-day expiration”).
- For questions or technical issues, contact your system administrator.

---

## Ready to Begin?
Use the sidebar to select either **Boarding Pricing** or **Day Camp Pricing** and start entering your center’s information!

""")
#     st.session_state.boarding_products = []

# # --- Mock Data and Constants ---
# MOCK_LOCATIONS = [
#     "Best Friends - Boston",
#     "Best Friends - Dallas",
#     "Best Friends - Chicago",
#     "Best Friends - Miami",
#     "Best Friends - LA",
#     "Best Friends - New York",
#     "Best Friends - Atlanta",
# ]

# # Kennel type options
# KENNEL_TYPES = [
#     "Standard Suite",
#     "Luxury Suite",
#     "Deluxe Suite",
#     "Executive Suite",
#     "Themed Suite",
#     "Indoor/Outdoor Suite",
#     "Multi-pet Suite",
#     "Wire crates",
#     "Plastic crates",
#     "Soft-sided crates",
#     "Custom built-in kennels",
#     "Other"
# ]

# # Dog size categories with weight ranges
# DOG_SIZES = [
#     "Small (0-25 lbs)", 
#     "Medium (26-50 lbs)", 
#     "Large (51-90 lbs)", 
#     "XL (91+ lbs)",
#     "All Sizes"
# ]

# # Expanded animal types and categories
# ANIMAL_CATEGORIES = {
#     "Dogs": ["Small breeds", "Medium breeds", "Large breeds", "XL breeds", "All sizes"],
#     "Cats": ["Kittens", "Adults", "All ages"],
#     "Small Pets": ["Hamster", "Guinea pig", "Rabbit", "Ferret", "Gerbil", "Mouse/Rat", "Other small pet"],
#     "Birds": ["Small birds", "Medium birds", "Large birds", "Other bird"],
#     "Reptiles": ["Lizard", "Snake", "Turtle/Tortoise", "Other reptile"],
#     "Other Animals": ["Fish", "Amphibian", "Farm animal", "Exotic pet", "Other"]
# }

# # --- Page title ---
# st.set_page_config(page_title="BFPC Pricing Intake", page_icon="💰", layout="wide")

# st.title("Best Friends Pricing & Offers Intake")
# st.write("Please fill out all required fields. You can add multiple services per location.")

# # Create tabs for different sections of the form
# tab1, tab2, tab3 = st.tabs(["📋 Basic Info", "💲 Services & Pricing", "🔍 Additional Details"])

# # --- Section 1: Location Info (Tab 1) ---
# with tab1:
#     st.header("Location Information")
#     location_name = st.selectbox(
#         "Select your location", 
#         MOCK_LOCATIONS,
#         help="Choose the location you're submitting pricing information for"
#     )
    
#     # Animal services section with expandable categories
#     st.subheader("Animal Types Served")
#     st.write("Select all the types of animals your location provides services for.")
    
#     # Dogs are assumed by default
#     st.info("🐶 **Dogs** are included by default for all locations.")
#     dog_sizes = st.multiselect(
#         "Which dog sizes do you accommodate?",
#         ANIMAL_CATEGORIES["Dogs"],
#         default=["All sizes"],
#         help="Select all dog sizes you can accommodate"
#     )
    
#     # Other animal types with expandable details
#     st.write("")
#     animal_types = st.multiselect(
#         "What other animals do you offer services for?",
#         list(ANIMAL_CATEGORIES.keys())[1:],  # All except Dogs
#         help="Select all types of animals your location serves"
#     )
    
#     # For storing detailed animal selections
#     animal_details = {"Dogs": dog_sizes}
#     habitat_requirements = {}
#     special_care_notes = {}
    
#     # Create a consolidated list of animal species for service selection
#     species_list = ['Dog']  # Dogs are always included
    
#     # Add Cats if selected
#     if "Cats" in animal_types:
#         species_list.append("Cat")
        
#     # Add other animal types with more specific naming
#     for animal_type in animal_types:
#         if animal_type != "Cats":  # Cats already handled above
#             if animal_type == "Small Pets":
#                 species_list.append("Small Pet")
#             elif animal_type == "Other Animals":
#                 species_list.append("Other Animal")
#             else:
#                 # Birds -> Bird, Reptiles -> Reptile (singular form)
#                 species_list.append(animal_type[:-1] if animal_type.endswith('s') else animal_type)
    
#     # Store in session state for use in service entries
#     st.session_state.selected_animal_types = {
#         'Dogs': dog_sizes,
#         'selected_types': animal_types,
#         'species_list': species_list
#     }
    
#     # Show detailed options for each selected animal type
#     for animal_type in animal_types:
#         st.write(f"")
#         st.write(f"**{animal_type} Details**")
#         animal_details[animal_type] = st.multiselect(
#             f"Which {animal_type.lower()} do you accommodate?",
#             ANIMAL_CATEGORIES[animal_type],
#             help=f"Select all {animal_type.lower()} types your location serves"
#         )
        
#         # Habitat requirements for small pets, birds, reptiles
#         if animal_type in ["Small Pets", "Birds", "Reptiles"]:
#             habitat_requirements[animal_type] = st.radio(
#                 f"Do owners need to provide habitats for {animal_type.lower()}?",
#                 ["Yes, owner must provide habitat", "No, we provide habitats", "It depends on the animal"],
#                 key=f"habitat_{animal_type}"
#             )
            
#             if habitat_requirements[animal_type] == "It depends on the animal":
#                 special_care_notes[animal_type] = st.text_area(
#                     f"Please explain habitat requirements for {animal_type.lower()}",
#                     key=f"habitat_note_{animal_type}"
#                 )

# # --- Section 2: Service Entries (Tab 2) ---
# with tab2:
#     st.header("Services & Pricing")
#     st.write("Enter all service options and pricing details below.")
    
#     service_entries = []
#     num_services = st.number_input("How many service types would you like to enter?", 
#                                 min_value=1, max_value=20, value=1,
#                                 help="For each service category (boarding, grooming, etc.) add a separate entry")
    
#     for i in range(int(num_services)):
#         with st.expander(f"Service Entry #{i+1}"):
#             service = {}
#             service["id"] = str(uuid.uuid4())  # Unique ID for each service
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 # Service category with special handling for Boarding
#                 service["category"] = st.selectbox(
#                     f"Service Category", 
#                     ["Boarding", "Day Camp", "Grooming", "Training", "Other"], 
#                     key=f"cat_{i}"
#                 )
                
#                 # Special handling for Boarding service to capture product matrix
#                 if service["category"] == "Boarding":
#                     st.info("💡 Please use the Boarding Product Matrix below to specify all combinations of kennel types, pricing, and dog size compatibility offered at this location.")
#                 # Get dynamically generated animal species list from session state
#                 service["applies_to"] = st.multiselect(
#                     f"Applies to", 
#                     st.session_state.selected_animal_types['species_list'],
#                     default=["Dog"],  # Default to Dog
#                     key=f"applies_{i}"
#                 )
#                 service["is_package"] = st.radio(
#                     f"Is this a Package?", 
#                     ["No", "Yes"], 
#                     key=f"pkg_{i}"
#                 )
            
#             with col2:
#                 service["description"] = st.text_input(
#                     f"Service Description", 
#                     key=f"desc_{i}", 
#                     help="Brief description of this service")
#                 service["base_price"] = st.number_input(
#                     f"Base Price ($)", 
#                     min_value=0.0, 
#                     format="%.2f", 
#                     key=f"price_{i}"
#                 )
#                 service["is_bundled"] = st.radio(
#                     f"Bundled with Another Service?", 
#                     ["No", "Yes"], 
#                     key=f"bundled_{i}"
#                 )
            
#             # Boarding-specific Product Matrix
#             if service["category"] == "Boarding":
#                 st.write("")
#                 st.subheader("🛏️ Boarding Product Matrix")
#                 st.write("Please add each kennel type, price point, and compatible dog size combination offered at this location.")
#                 st.caption("For example, if you offer Standard Suites at $30 for small dogs and $40 for large dogs, add those as two separate entries.")
                
#                 # Initialize or retrieve boarding products for this service
#                 if f"boarding_products_{i}" not in st.session_state:
#                     st.session_state[f"boarding_products_{i}"] = []
                
#                 # Display existing boarding products in a table if any
#                 if st.session_state[f"boarding_products_{i}"]:
#                     st.write("**Current Boarding Products:**")
#                     product_data = []
#                     for idx, product in enumerate(st.session_state[f"boarding_products_{i}"]):
#                         dog_sizes_str = ", ".join(product["dog_sizes"])
#                         product_data.append([idx+1, product["kennel_type"], f"${product['price_per_night']:.2f}", dog_sizes_str])
                    
#                     st.table({
#                         "#": [p[0] for p in product_data],
#                         "Kennel Type": [p[1] for p in product_data],
#                         "Price Per Night": [p[2] for p in product_data],
#                         "Compatible Dog Sizes": [p[3] for p in product_data]
#                     })
                
#                 # Add new boarding product (using container instead of expander to avoid nesting issues)
#                 st.write("")
#                 st.write("**Add New Boarding Product**")
#                 add_product_container = st.container()
                
#                 with add_product_container:
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         new_kennel_type = st.selectbox(
#                             "Kennel Type",
#                             KENNEL_TYPES,
#                             key=f"new_kennel_type_{i}"
#                         )
                        
#                         if new_kennel_type == "Other":
#                             new_kennel_other = st.text_input(
#                                 "Describe Other Kennel Type",
#                                 key=f"new_kennel_other_{i}"
#                             )
                    
#                     with col2:
#                         new_price = st.number_input(
#                             "Price Per Night ($)",
#                             min_value=0.0,
#                             step=5.0,
#                             format="%.2f",
#                             key=f"new_price_{i}"
#                         )
                    
#                     new_dog_sizes = st.multiselect(
#                         "Compatible Dog Sizes",
#                         DOG_SIZES,
#                         default=[],
#                         help="Select all dog sizes that can use this kennel type at this price point",
#                         key=f"new_dog_sizes_{i}"
#                     )
                    
#                     # Option to add custom dog size if needed
#                     if st.checkbox("Add custom dog size category", key=f"custom_size_check_{i}"):
#                         custom_size = st.text_input(
#                             "Enter custom dog size category",
#                             placeholder="e.g., Toy breeds, Giant breeds, etc.",
#                             key=f"custom_size_{i}"
#                         )
#                         if custom_size and st.button("Add Custom Size", key=f"add_custom_size_{i}"):
#                             if custom_size not in new_dog_sizes:
#                                 new_dog_sizes.append(custom_size)
#                                 st.success(f"Added '{custom_size}' to compatible sizes")
                    
#                     # Button to add the boarding product
#                     if st.button("Add to Matrix", key=f"add_product_{i}"):
#                         if new_kennel_type and new_price > 0 and new_dog_sizes:
#                             new_product = {
#                                 "kennel_type": new_kennel_type if new_kennel_type != "Other" else f"Other: {new_kennel_other}",
#                                 "price_per_night": new_price,
#                                 "dog_sizes": new_dog_sizes
#                             }
#                             st.session_state[f"boarding_products_{i}"].append(new_product)
#                             st.success("Boarding product added!")
#                             # Force a rerun to show the updated table
#                             st.rerun()
#                         else:
#                             st.error("Please fill in all fields.")
                
#                 # Option to remove products if needed
#                 if st.session_state[f"boarding_products_{i}"]:
#                     st.write("")
#                     st.write("**Remove Boarding Products**")
#                     remove_container = st.container()
                    
#                     with remove_container:
#                         remove_index = st.number_input(
#                             "Select product number to remove",
#                             min_value=1,
#                             max_value=len(st.session_state[f"boarding_products_{i}"]),
#                             key=f"remove_idx_{i}"
#                         )
                        
#                         if st.button("Remove Selected Product", key=f"remove_btn_{i}"):
#                             if remove_index <= len(st.session_state[f"boarding_products_{i}"]):
#                                 st.session_state[f"boarding_products_{i}"].pop(int(remove_index) - 1)
#                                 st.success("Product removed!")
#                                 st.rerun()
                
#                 # Save the boarding products to the service
#                 service["boarding_products"] = st.session_state[f"boarding_products_{i}"]                
            
#             # Regular kennel type selection for non-boarding services
#             elif service["category"] == "Grooming":
#                 st.write("")
#                 service["kennel_types"] = st.multiselect(
#                     f"What kennel types do you use for this service?",
#                     KENNEL_TYPES,
#                     help="Select all applicable kennel or housing types used for this service",
#                     key=f"kennel_{i}"
#                 )
                
#                 # If Other is selected, show a text field for details
#                 if "Other" in service.get("kennel_types", []):
#                     service["other_kennel_description"] = st.text_input(
#                         "Please describe your other kennel type",
#                         key=f"other_kennel_{i}"
#                     )
            
#             # Conditional fields based on package/bundle selection
#             if service["is_package"] == "Yes":
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     service["package_qty"] = st.number_input(
#                         f"Quantity in Package", 
#                         min_value=1, 
#                         key=f"qty_{i}"
#                     )
#                 with col2:
#                     service["expiration_policy"] = st.text_input(
#                         f"Expiration Policy", 
#                         placeholder="e.g., Expires in 30 days",
#                         key=f"exp_{i}"
#                     )
                    
#             if service["is_bundled"] == "Yes":
#                 service["bundle_desc"] = st.text_area(
#                     f"Describe the bundle", 
#                     placeholder="What services are included in this bundle?",
#                     key=f"bundle_desc_{i}"
#                 )
            
#             # Add-ons section - FIX: No nested expanders
#             service["add_ons"] = []
#             add_addons = st.checkbox(f"This service has add-ons", key=f"add_on_chk_{i}")
            
#             if add_addons:
#                 st.write("---")
#                 st.subheader("Add-ons for this service")
#                 num_addons = st.number_input(
#                     f"Number of add-ons", 
#                     min_value=1, max_value=10, value=1, 
#                     key=f"addon_num_{i}"
#                 )
                
#                 for j in range(int(num_addons)):
#                     st.write(f"##### Add-on #{j+1}")
#                     # Use columns instead of nested expanders
#                     col1, col2 = st.columns(2)
#                     addon = {}
                    
#                     with col1:
#                         addon["desc"] = st.text_input(
#                             f"Description", 
#                             placeholder="e.g., Extra walking, Special food",
#                             key=f"addon_desc_{i}_{j}"
#                         )
                    
#                     with col2:
#                         addon["price_impact"] = st.text_input(
#                             f"Price Impact", 
#                             placeholder="e.g., +$10 or +15%",
#                             key=f"addon_impact_{i}_{j}"
#                         )
                    
#                     addon["conditions"] = st.text_input(
#                         f"Conditions/Restrictions", 
#                         placeholder="e.g., Only for dogs over 50lbs",
#                         key=f"addon_cond_{i}_{j}"
#                     )
                    
#                     service["add_ons"].append(addon)
#                     st.write("---")
            
#             service_entries.append(service)

# # --- Section 3 & 4: Additional Questions (Tab 3) ---
# with tab3:
#     st.header("Additional Details")
    
#     # File upload section
#     st.subheader("Optional Document Upload")
#     doc_upload = st.file_uploader(
#         "Do you have any pricing or service docs you'd like to attach?", 
#         type=["pdf", "doc", "docx", "xls", "xlsx", "csv", "txt"],
#         help="Upload existing pricing sheets, brochures, or other relevant documents"
#     )
    
#     if doc_upload is not None:
#         st.success(f"Successfully uploaded: {doc_upload.name}")
    
#     # Final questions section
#     st.subheader("Final Questions")
    
#     pricing_scenarios = st.text_area(
#         "Do you have pricing for these scenarios?", 
#         placeholder="e.g., Boarding + Exit Groom, Daycare + Training",
#         help="Describe any combined service scenarios you offer"
#     )
    
#     discounts = st.text_area(
#         "Do you offer any discounts?", 
#         placeholder="e.g., Multi-dog, recurring packages, senior pets",
#         help="Describe any discount structures you have"
#     )
    
#     unique_structures = st.text_area(
#         "Are there any unique pricing structures or promotions?",
#         placeholder="e.g., Seasonal pricing, member benefits, etc.",
#         help="Any other pricing models not covered above"
#     )

# # --- Submission ---
# st.divider()
# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:
#     if st.button("Submit Form", use_container_width=True, type="primary"):
#         # Enhanced validation
#         validation_errors = []
        
#         if not location_name:
#             validation_errors.append("Please select a location")
        
#         if not service_entries:
#             validation_errors.append("Please add at least one service")
#         else:
#             # Validate each service entry has required fields
#             for i, service in enumerate(service_entries):
#                 if not service.get("category"):
#                     validation_errors.append(f"Service #{i+1}: Category is required")
#                 if not service.get("description"):
#                     validation_errors.append(f"Service #{i+1}: Description is required")
#                 if not service.get("applies_to"):
#                     validation_errors.append(f"Service #{i+1}: Must select at least one animal type")
#                 if service.get("base_price") is None:
#                     validation_errors.append(f"Service #{i+1}: Base price is required")
                    
#         if validation_errors:
#             for error in validation_errors:
#                 st.error(error)
#         else:
#             # Additional validation for kennel types and boarding products
#             for i, service in enumerate(service_entries):
#                 if service.get("category") == "Boarding":
#                     if not service.get("boarding_products"):
#                         st.warning(f"Service #{i+1}: No boarding products added. Please complete the Boarding Product Matrix.")
#                     elif len(service.get("boarding_products", [])) < 2:
#                         st.info(f"Service #{i+1}: Consider adding more boarding product combinations if you offer different prices by dog size or kennel type.")
#                 elif service.get("category") == "Grooming" and not service.get("kennel_types"):
#                     st.warning(f"Service #{i+1}: No kennel types selected. This is recommended information.")
                    
#                 if service.get("category") == "Grooming" and "Other" in service.get("kennel_types", []) and not service.get("other_kennel_description"):
#                     st.warning(f"Service #{i+1}: Please describe your 'Other' kennel type.")
            
#             # Continue with submission if there are only warnings
#             # Prepare collected data
#             intake_data = {
#                 "location_name": location_name,
#                 "animal_types": {
#                     "Dogs": dog_sizes,
#                     **{k: animal_details.get(k, []) for k in animal_types}
#                 },
#                 "habitat_requirements": habitat_requirements,
#                 "special_care_notes": special_care_notes,
#                 "submitted_at": datetime.utcnow().isoformat(),
#                 "service_entries": service_entries,
#                 "pricing_scenarios": pricing_scenarios,
#                 "discounts": discounts,
#                 "unique_structures": unique_structures,
#                 "doc_upload_name": doc_upload.name if doc_upload else None
#             }
            
#             # Save to session state for persistence
#             st.session_state.form_data = intake_data
#             st.session_state.form_data['submitted'] = True
            
#             # Show success message and summary
#             st.balloons()
#             st.success("Submission received! Thank you for your input.")
            
#             with st.expander("View Submission Details", expanded=True):
#                 st.markdown("### Submission Summary")
#                 st.json(intake_data)
                
#                 st.download_button(
#                     label="📥 Download Submission as JSON",
#                     data=json.dumps(intake_data, indent=2),
#                     file_name=f"pricing_intake_{location_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
#                     mime="application/json",
#                     use_container_width=True
#                 )

# # Show a footer
# st.divider()
# st.markdown("""<div style='text-align: center; color: gray; font-size: small;'>
#             Best Friends Pet Care - Pricing Intake Form © 2025
#             </div>""", unsafe_allow_html=True)
