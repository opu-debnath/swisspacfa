import streamlit as st

# Page configuration
st.set_page_config(page_title="Contact Developer", layout="wide")
# Page title
st.title("Contact the Developer")

# Interactive button to reveal contact details
if st.button("Show Contact Details"):
    st.write("**Name**: *Opu Debnath*") 
    st.write("**Designation**: Freelance Data Scientist")  
    st.write("**Email**: [odfreelancer01@gmail.com](mailto:odfreelancer01@gmail.com)") 
