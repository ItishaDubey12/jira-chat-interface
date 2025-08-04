import streamlit as st
import pandas as pd
from io import BytesIO
from sprinttickets import create_sprint_tickets
from subtaskcreation import create_subtasks

# Streamlit config
st.set_page_config(page_title="Jira Assistant", layout="centered")

# Title and greeting
st.title("🗨️ Jira Assistant Chat")
st.markdown("Hi there! 👋")
st.markdown("How can I help you today?")
st.markdown("You can either:\n\n- 🧾 **Create Sprint Tickets**\n- 📌 **Create Subtasks under your Stories**")

# User choice
choice = st.radio("Please choose an option:", ("Create Sprint Tickets", "Create Subtasks"))

# === 📥 Download Format Section ===
def get_template_df(choice):
    if choice == "Create Sprint Tickets":
        return pd.DataFrame({
            "Summary": ["Sample Ticket 1", "Sample Ticket 2"],
            "Description": ["Description 1", "Description 2"],
            "Issue Type": ["Task", "Story"],
            "Labels": ["automation", "backend"],
            "Assignee Email": ["user1@example.com", "user2@example.com"],
            "Sprint Name": ["Sprint 30", "Sprint 30"]
        })
    elif choice == "Create Subtasks":
        return pd.DataFrame({
            "Parent": ["TECH-123", "TECH-456"],
            "Summary": ["Subtask A", "Subtask B"]
        })

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Template")
    return output.getvalue()

template_df = get_template_df(choice)
excel_bytes = convert_df_to_excel(template_df)

st.download_button(
    label=f"📥 Download {choice} Format",
    data=excel_bytes,
    file_name="sprint_ticket_template.xlsx" if choice == "Create Sprint Tickets" else "subtask_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
# ✅ Instructional text below the download button
st.markdown(
    "ℹ️ **Please upload the file in `.xlsx` format only.** You can create the format in Google Sheets and use `File → Download → Microsoft Excel (.xlsx).` **Make sure the format is same as the sample format given above.**"
)
# === 📤 Upload Excel Sheet ===
uploaded_file = st.file_uploader("📤 Upload your Excel Sheet", type=["xlsx"])

# After file is uploaded
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # Clean headers

    st.success("✅ File uploaded successfully!")
    st.markdown("**📋 Columns detected in the file:**")
    st.write(df.columns.tolist())
    st.dataframe(df.head())

    if choice == "Create Sprint Tickets":
        if st.button("🚀 Create Sprint Tickets"):
            try:
                result = create_sprint_tickets(df)
                st.success(result)
            except KeyError as e:
                st.error(f"❌ Column not found in file: {e}")
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

    elif choice == "Create Subtasks":
        if st.button("📌 Create Subtasks"):
            try:
                result = create_subtasks(df)
                st.success(result)
            except KeyError as e:
                st.error(f"❌ Column not found in file: {e}")
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
